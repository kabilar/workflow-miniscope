# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # DataJoint U24 - Workflow Miniscope

# ## Setup
#
# Move to the parent directory for access to the `dj_local_conf.json` saved in [01-configure](./01-configure.ipynb).

import os
# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='workflow-miniscope', (
    "Please move to the workflow directory")
import datajoint as dj

# ## Processing Parameters
#
# Before processing the data itself, we should set up the parameters in Insert an entry into `miniscope.MotionCorrectionParamSet`. These will be referenced by the analysis package, and can be referenced for multiple datasets.

import numpy as np
from workflow_miniscope.pipeline import miniscope

# Define the parameters:

params = dict(pars_envs = ['memory_size_to_use', 12, 'memory_size_per_patch', 0.6, 
                           'patch_dims', [64, 64]],
              include_residual = False,
              gSig = 3,           
              gSiz = 15,
              ssub = 1,
              with_dendrites = True,
              updateA_search_method = 'dilate',
              updateA_bSiz = 5,
              updateA_dist = None,
              spatial_constraints = ['connected', True, 'circular', False],
              spatial_algorithm = 'hals_thresh',
              Fs = 30,
              tsub = 5,
              deconv_flag = True,
              deconv_options = ['type', 'ar1', 'method', 'constrained', 'smin', -5, 
                                'optimize_pars', True, 'optimize_b', True, 
                                'max_tau', 100],
              nk = 3,
              detrend_method = 'spline',
              bg_model = 'ring',
              nb = 1,
              ring_radius = 23,
              num_neighbors = [],
              show_merge = False,
              merge_thr = 0.65,
              method_dist = 'max',
              dmin = 5,
              dmin_only = 2,
              merge_thr_spatial = [0.8, 0.4, -float('inf')],
              K = [],
              min_corr = 0.9,
              min_pnr = 15,
              min_pixel = None,
              bd = 0,
              frame_range = [],
              save_initialization = False,
              use_parallel = True,
              show_init = False,
              choose_params = False,
              center_psf = True,
              min_corr_res = 0.7,
              min_pnr_res = 8,
              seed_method_res = 'auto',
              update_sn = True,
              with_manual_intervention = False)

# To insert the parameters, use the following function:
#
# `NOTE: THIS FUNCTION IS STILL UNDER DEVELOPMENT AND MAY NOT BE FUNCTIONAL`

miniscope.MotionCorrectionParamSet.insert_new_params(
    processing_method='mcgill_miniscope_analysis', 
    paramset_idx=0, 
    paramset_desc=('Calcium imaging analysis with Miniscope Analysis' 
                   + 'using default parameters'), 
    params=params)

# ## Data Ingestion
#
# The following steps outline ingestion of UCLA Miniscope data, as well as acquired metadata and processed data, into `workflow-miniscope`. To automate ingestion, see [03-automate](03-automate-optional.ipynb).

# ### Insert into `subject.Subject`

subject.Subject.insert1(dict(subject='subject1', 
                             sex='F', 
                             subject_birth_date='2019-01-01 00:00:01', 
                             subject_description='no description'))

# ### Insert into `lab.Equipment`

Equipment.insert1(dict(scanner='Miniscope-DAQ-V3'))

# ### Insert into `session.Session`

session.Session.insert1(dict(subject='subject1', 
                             session_datetime='2021-01-01 00:00:01'))

# ### Insert into `session.SessionDirectory`

session.SessionDirectory.insert1(dict(subject='subject1', 
                                      session_datetime='2021-01-01 00:00:01', 
                                      session_dir='/subject1/session0'))

# ### Insert into `miniscope.Recording`
#
# `ELEMENT STILL UNDER DEVELOPMENT. FOLLOWING NOT FULLY FUNCTIONAL`

scan.Scan.insert1(dict(subject='subject1', 
                       session_datetime='2021-01-01 00:00:01', 
                       scan_id=0, 
                       scanner='Miniscope-DAQ-V3', 
                       acq_software='Miniscope-DAQ-V3',
                       scan_notes=''))

# ### Populate `miniscope.RecordingInfo`
#
# + This imported table stores information about the acquired image (e.g. image dimensions, file paths, etc.).
# + `populate` automatically calls `make` for every key for which the auto-populated table is missing data.
# + `populate_settings` passes arguments to the `populate` method.
# + `display_progress=True` reports the progress bar

populate_settings = {'display_progress': True}

scan.ScanInfo.populate(**populate_settings)

# ---
# # CONTINUE EDITING HERE
# ---

# ## Insert an entry into `imaging.ProcessingTask`
#
# + This entry will trigger ingestion of the processed results (i.e. motion correction, segmentation, and traces)
#
# + The `paramset_idx` is the parameter set stored in `imaging.ProcessingParamSet` that is used for the image processing.
#
# + The `processing_output_dir` attribute contains the output directory of the processed results (relative the the imaging root data directory).

# ## Populate `imaging.Processing`
#
# + For the `task_mode=load` specified above in `imaging.ProcessingTask`, this step ensures that the output directory contains the valid processed outputs.
#
# + In the future, this step will provide for the option to `trigger` the analysis within this workflow (if the `task_mode=trigger`).

imaging.Processing.populate(**populate_settings)

# ## Populate `imaging.MotionCorrection`
#
# + This table contains the rigid or non-rigid motion correction data including the shifts and summary images.
#

imaging.MotionCorrection.populate(**populate_settings)

# ## Insert an entry into `imaging.Curation`
#
# + The next step in the pipeline is the curation of segmentation results. If a manual curation was implemented, an entry needs to be manually inserted into the table Curation, which specifies the directory to the curated results in curation_output_dir. If we would like to process the processed outcome directly, an entry is also needed in Curation. A method create1_from_processing_task was provided to help this insertion. It copies the processing_output_dir in ProcessingTask to the field curation_output_dir in the table Curation with a new curation_id.
#
# + In this example, we create/insert one `imaging.Curation` for each `imaging.ProcessingTask`, specifying the same output directory.

imaging.Curation(dict(subject='subject1', 
                      session_datetime='2021-01-01 00:00:01', 
                      scan_id=0,
                      paramset_idx=0,
                      curation_id=0,
                      curation_time='2021-01-01 00:00:01', 
                      curation_output_dir='<imaging_root_data_dir>/subject1/session0/miniscope_analysis',
                      manual_curation=False,
                      curation_note=''})

# ## Populate `imaging.Segmentation`
#
# + This table contains the mask coordinates, weights, and centers.

imaging.Segmentation.populate(**populate_settings)

# ## Populate `imaging.MaskClassification`
#
# + This table is currently not implemented.

imaging.MaskClassification.populate(**populate_settings)

# ## Populate `imaging.Fluorescence`
#
# + This table contains the fluorescence traces prior filtering and spike extraction

imaging.Fluorescence.populate(**populate_settings)

# ## Populate `imaging.Activity`
# + This table contains the inferred neural activity from the fluorescence traces.

imaging.Activity.populate(**populate_settings)

# ## Proceed to the `02explore.ipynb` Jupyter Notebook
#
# + This notebook describes the steps to query, fetch, and visualize the imaging data.
