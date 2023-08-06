"""
CVR Quantiphyse plugin - Processes

Author: Martin Craig <martin.craig@nottingham.ac.uk>
Copyright (c) 2021 University of Nottingham, Martin Craig
"""
import io
import logging
import sys
import os

import numpy as np

# Silence Tensorflow random messages
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel(logging.ERROR)

from quantiphyse.utils import QpException
from quantiphyse.utils.enums import Boundary
from quantiphyse.processes import Process

MAX_LOG_SIZE=100000

def _get_progress_cb(worker_id, queue, n_voxels):
    def _progress(frac):
        queue.put((worker_id, frac * n_voxels))
    return _progress

def _run_glm(worker_id, queue, data, mask, regressors, regressor_types, regressor_trs, tr, baseline, data_start_time, delay_min, delay_max, delay_step):
    try:
        from vaby.data import DataModel
        from vaby_models_cvr.petco2 import CvrPetCo2Model

        options = {
            "regressors" : regressors,
            "regressor_trs" : regressor_trs,
            "regressor_types" : regressor_types,
            "tr" : tr,
            "baseline" : baseline,
            "data_start_time" : data_start_time,
        }

        # Set up log to go to string buffer
        log = io.StringIO()
        handler = logging.StreamHandler(log)
        handler.setFormatter(logging.Formatter('%(levelname)s : %(message)s'))
        logging.getLogger().handlers.clear()
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.INFO)

        data_model = DataModel(data, mask=mask)
        fwd_model = CvrPetCo2Model(data_model, **options)
        glmdata = fwd_model.fit_glm(delay_min=delay_min, delay_max=delay_max, delay_step=delay_step, progress_cb=_get_progress_cb(worker_id, queue, data_model.data_space.size))
        regressor_types = [s.strip() for s in regressor_types.split(",")]
        ret = {}
        for idx, regressor_type in enumerate(regressor_types):
            if regressor_type in ("co2", "petco2"):
                ret["cvr%i" % (idx+1)] = glmdata[idx]
            else:
                ret["beta%i" % (idx+1)] = glmdata[idx]
        ret["delay"] = glmdata[-3]
        ret["sig0"] = glmdata[-2]
        ret["modelfit"] = glmdata[-1]
        for name in list(ret.keys()):
            data = ret[name]
            shape = data_model.data_space.shape
            if data.ndim > 1:
                shape = list(shape) + [data.shape[1]]
            ndata = np.zeros(shape, dtype=np.float32)
            ndata[mask > 0] = data
            ret[name] = ndata
        queue.put((worker_id, data_model.data_space.size))

        ret = (ret, log.getvalue())
        return worker_id, True, ret
    except:
        import traceback
        traceback.print_exc()
        return worker_id, False, sys.exc_info()[1]

class CvrPetCo2GlmProcess(Process):
    """
    CVR-PETCO2 modelling using a GLM
    """
    
    PROCESS_NAME = "CvrPetCo2Glm"
    
    def __init__(self, ivm, **kwargs):
        Process.__init__(self, ivm, worker_fn=_run_glm, **kwargs)

    def run(self, options):
        data = self.get_data(options)
        if data.ndim != 4: 
            raise QpException("Data must be 4D for DCE PK modelling")

        roi = self.get_roi(options, data.grid)
    
        self.suffix = options.pop('output-suffix', '')
        if self.suffix != "" and self.suffix[0] != "_": 
            self.suffix = "_" + self.suffix

        regressors = options.pop('regressors', None)
        regressor_trs = options.pop('regressor_trs', None)
        regressor_types = options.pop('regressor_types', None)
        if regressors is None or regressor_types is None or regressor_trs is None:
            raise QpException("Regressors, regressor type and regressor TR options must be given")
        if isinstance(regressors, str):
            regressors = regressors.split()
            new_regressors = []
            for r in regressors:
                if not os.path.isabs(r):
                    r = os.path.join(self.indir, r)
                new_regressors.append(r)
            regressors = ",".join(new_regressors)

        if isinstance(regressor_trs, str):
            try:
                regressor_trs = [float(v) for v in regressor_trs.split(",")]
            except ValueError:
                raise QpException("Regressor TRs should be comma separated list of numbers")
        elif isinstance(regressor_trs, (int, float)):
            regressor_trs = [regressor_trs]
        self.n_regressors = len(regressor_trs)

        tr = options.pop("tr", None)
        if tr is None:
            raise QpException("TR must be given")

        # Non-compulsary options
        baseline = options.pop("baseline", 60)
        data_start_time = options.pop("data-start-time", None)
        delay_min = options.pop("delay-min", 0)
        delay_max = options.pop("delay-max", 0)
        delay_step = options.pop("delay-step", 1)
        
        # Use smallest sub-array of the data which contains all unmasked voxels
        self.grid = data.grid
        self.bb_slices = roi.get_bounding_box()
        self.debug("Using bounding box: %s", self.bb_slices)
        data_bb = data.raw()[tuple(self.bb_slices)]
        mask_bb = roi.raw()[tuple(self.bb_slices)]
        #n_workers = data_bb.shape[0]
        n_workers = 1

        args = [data_bb, mask_bb, regressors, regressor_types, regressor_trs, tr, baseline, data_start_time, delay_min, delay_max, delay_step]
        self.voxels_done = [0] * n_workers
        self.total_voxels = np.count_nonzero(roi.raw())
        self.start_bg(args, n_workers=n_workers)

    def timeout(self, queue):
        if queue.empty(): return
        while not queue.empty():
            worker_id, voxels_done = queue.get()
            self.voxels_done[worker_id] = voxels_done
        progress = float(sum(self.voxels_done)) / self.total_voxels
        self.sig_progress.emit(progress)

    def finished(self, worker_output):
        """
        Add output data to the IVM
        """
        if self.status == Process.SUCCEEDED:
            # Only include log from first process to avoid multiple repetitions
            for data, log in worker_output:
                data_keys = data.keys()
                if log:
                    # If there was a problem the log could be huge and full of
                    # nan messages. So chop it off at some 'reasonable' point
                    self.log(log[:MAX_LOG_SIZE])
                    if len(log) > MAX_LOG_SIZE:
                        self.log("WARNING: Log was too large - truncated at %i chars" % MAX_LOG_SIZE)
                    break

            first = True
            self.data_items = []
            for key in data_keys:
                self.debug(key)
                recombined_data = self.recombine_data([o.get(key, None) for o, l in worker_output])
                name = key + self.suffix
                if key is not None:
                    self.data_items.append(name)
                    if recombined_data.ndim == 2:
                        recombined_data = np.expand_dims(recombined_data, 2)

                    # The processed data was chopped out of the full data set to just include the
                    # ROI - so now we need to put it back into a full size data set which is otherwise
                    # zero.
                    if recombined_data.ndim == 4:
                        shape4d = list(self.grid.shape) + [recombined_data.shape[3],]
                        full_data = np.zeros(shape4d, dtype=np.float32)
                    else:
                        full_data = np.zeros(self.grid.shape, dtype=np.float32)
                    full_data[self.bb_slices] = recombined_data.reshape(full_data[self.bb_slices].shape)
                    self.ivm.add(full_data, grid=self.grid, name=name, make_current=first, roi=False)

                    # Set some view defaults because we know what range these should be in
                    self.ivm.data[name].view.boundary = Boundary.CLAMP
                    if "cvr" in key:
                        self.ivm.data[name].view.cmap_range = (0, 1)
                    if "delay" in key:
                        self.ivm.data[name].view.cmap_range = (-15, 15)
                    first = False
        else:
            # Include the log of the first failed process
            for out in worker_output:
                if out and isinstance(out, Exception) and hasattr(out, "log") and len(out.log) > 0:
                    self.log(out.log)
                    break

    def output_data_items(self):
        """
        :return: a sequence of data item names that may be output
        """
        data_items = ["cvr", "delay", "sig0"]
        for idx in range(self.n_regressors):
            data_items.append("cvr%i" % (idx+1))
            data_items.append("beta%i" % (idx+1))

        return [key + self.suffix for key in data_items]

def _run_vb(worker_id, queue, data, mask, voxel_sizes, regressors, regressor_types, regressor_trs, tr, infer_sig0, infer_delay, allow_neg_cvr, baseline, data_start_time, spatial, maxits, output_var):
    try:
        from vaby import run

        # Set up log to go to string buffer
        log = io.StringIO()
        options = {
            "method" : "avb",
            "voxel_sizes" : voxel_sizes,
            "regressors" : regressors,
            "regressor_trs" : regressor_trs,
            "regressor_types" : regressor_types,
            "tr" : tr,
            "baseline" : baseline,
            "data_start_time" : data_start_time,
            "infer_sig0" : infer_sig0,
            "infer_delay" : infer_delay,
            "allow_neg_cvr" : allow_neg_cvr,
            "max_iterations" : maxits,
            "save_mean" : True,
            "save_var" : output_var,
            "save_model_fit" : True,
            "log_stream" : log,
            "log_level" : "INFO", # FIXME debugging output
        }
        if spatial:
            options["param_overrides"] = {}
            for param in ("cvr", "delay", "sig0"):
                options["param_overrides"][param] = {"prior_type" : "M"}

        outdict = {}
        _runtime, _state = run(data, "cvr_petco2", mask=mask, outdict=outdict, **options)

        ret = {}
        for name, nii in outdict.items():
            ret[name] = nii.get_fdata()
        ret = (ret, log.getvalue())

        queue.put((worker_id, np.count_nonzero(mask)))
        return worker_id, True, ret
    except:
        import traceback
        traceback.print_exc()
        return worker_id, False, sys.exc_info()[1]

class CvrPetCo2VbProcess(Process):
    """
    CVR-PETCO2 modelling using VB
    """

    PROCESS_NAME = "CvrPetCo2Vb"

    def __init__(self, ivm, **kwargs):
        Process.__init__(self, ivm, worker_fn=_run_vb, **kwargs)

    def run(self, options):
        data = self.get_data(options)
        if data.ndim != 4:
            raise QpException("Data must be 4D for CVR modelling")

        roi = self.get_roi(options, data.grid)
    
        self.suffix = options.pop('output-suffix', '')
        if self.suffix != "" and self.suffix[0] != "_": 
            self.suffix = "_" + self.suffix

        regressors = options.pop('regressors', None)
        regressor_trs = options.pop('regressor_trs', None)
        regressor_types = options.pop('regressor_types', None)
        if regressors is None or regressor_types is None or regressor_trs is None:
            raise QpException("Regressors, regressor type and regressor TR options must be given")

        if isinstance(regressors, str):
            regressors = regressors.split()
            new_regressors = []
            for r in regressors:
                if not os.path.isabs(r):
                    r = os.path.join(self.indir, r)
                new_regressors.append(r)
            regressors = ",".join(new_regressors)

        if isinstance(regressor_trs, str):
            try:
                regressor_trs = [float(v) for v in regressor_trs.split(",")]
            except ValueError:
                raise QpException("Regressor TRs should be comma separated list of numbers")
        elif isinstance(regressor_trs, (int, float)):
            regressor_trs = [regressor_trs]
        self.n_regressors = len(regressor_trs)

        tr = options.pop("tr", None)
        if tr is None:
            raise QpException("TR must be given")

        # Non-compulsary options
        baseline = options.pop("baseline", 60)
        data_start_time = options.pop("data-start-time", None)
        spatial = options.pop("spatial", False)
        maxits = options.pop("max-iterations", 10)
        self.output_var = options.pop("output-var", False)

        infer_sig0 = options.pop("infer-sig0", True)
        infer_delay = options.pop("infer-delay", True)
        allow_neg_cvr = options.pop("allow-neg-cvr", False)
        
        # Use smallest sub-array of the data which contains all unmasked voxels
        self.grid = data.grid
        self.bb_slices = roi.get_bounding_box()
        self.debug("Using bounding box: %s", self.bb_slices)
        data_bb = data.raw()[tuple(self.bb_slices)]
        mask_bb = roi.raw()[tuple(self.bb_slices)]
        voxel_sizes = self.grid.spacing
        #n_workers = data_bb.shape[0]
        n_workers = 1

        args = [data_bb, mask_bb, voxel_sizes, regressors, regressor_types, regressor_trs, tr, infer_sig0, infer_delay, allow_neg_cvr, baseline, data_start_time, spatial, maxits, self.output_var]
        self.voxels_done = [0] * n_workers
        self.total_voxels = np.count_nonzero(roi.raw())
        self.start_bg(args, n_workers=n_workers)

    def timeout(self, queue):
        if queue.empty(): return
        while not queue.empty():
            worker_id, voxels_done = queue.get()
            self.voxels_done[worker_id] = voxels_done
        progress = float(sum(self.voxels_done)) / self.total_voxels
        self.sig_progress.emit(progress)

    def finished(self, worker_output):
        """
        Add output data to the IVM
        """
        if self.status == Process.SUCCEEDED:
            # Only include log from first process to avoid multiple repetitions
            for data, log in worker_output:
                data_keys = data.keys()
                if log:
                    # If there was a problem the log could be huge and full of 
                    # nan messages. So chop it off at some 'reasonable' point
                    self.log(log[:MAX_LOG_SIZE])
                    if len(log) > MAX_LOG_SIZE:
                        self.log("WARNING: Log was too large - truncated at %i chars" % MAX_LOG_SIZE)
                    break
            first = True
            self.data_items = []
            for key in data_keys:
                self.debug(key)
                recombined_data = self.recombine_data([o.get(key, None) for o, l in worker_output])
                name = key + self.suffix
                if key is not None:
                    self.data_items.append(name)
                    if recombined_data.ndim == 2:
                        recombined_data = np.expand_dims(recombined_data, 2)

                    # The processed data was chopped out of the full data set to just include the
                    # ROI - so now we need to put it back into a full size data set which is otherwise
                    # zero.
                    if recombined_data.ndim == 4:
                        shape4d = list(self.grid.shape) + [recombined_data.shape[3],]
                        full_data = np.zeros(shape4d, dtype=np.float32)
                    else:
                        full_data = np.zeros(self.grid.shape, dtype=np.float32)
                    full_data[self.bb_slices] = recombined_data.reshape(full_data[self.bb_slices].shape)
                    self.ivm.add(full_data, grid=self.grid, name=name, make_current=first, roi=False)

                    # Set some view defaults because we know what range these should be in
                    self.ivm.data[name].view.boundary = Boundary.CLAMP
                    if "cvr" in key:
                        self.ivm.data[name].view.cmap_range = (0, 1)
                    if "delay" in key:
                        self.ivm.data[name].view.cmap_range = (-15, 15)
                    first = False
        else:
            # Include the log of the first failed process
            for out in worker_output:
                if out and isinstance(out, Exception) and hasattr(out, "log") and len(out.log) > 0:
                    self.log(out.log)
                    break

    def logfile_name(self):
        return "logfile" + self.suffix

    def output_data_items(self):
        """
        :return: a sequence of data item names that may be output
        """
        data_items = ["cvr", "delay", "sig0"]
        for idx in range(self.n_regressors):
            data_items.append("cvr%i" % (idx+1))
            data_items.append("beta%i" % (idx+1))

        data_items += ["mean_" + k for k in data_items]
        if self.output_var:
            data_items += ["var_" + k for k in data_items]
        return [key + self.suffix for key in data_items]
