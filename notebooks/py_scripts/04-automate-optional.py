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

# # [WIP] Automated workflow
# ### Method for inserting entries
#
# Modify `user_data/subjects.csv` and `user_data/sessions.csv`, and run the following commands
#
# or with the `ingest` method and accompanying `csv` files.

# Change into the parent directory to find the `dj_local_conf.json` file. 
# When you type `import datajoint as dj` the credentials from `dj_local_conf.json` will be used to log into the database.
import os
os.chdir('..')

from workflow_miniscope.pipeline import *
from workflow_miniscope.ingest import ingest_subjects, ingest_sessions

ingest_subjects()

ingest_sessions()

# +
import pathlib
from workflow_miniscope.paths import get_imaging_root_data_dir

root_dir = pathlib.Path(get_imaging_root_data_dir())

for scan_key in (scan.Scan & scan.ScanInfo - imaging.ProcessingTask).fetch('KEY'):
    scan_file = root_dir / (scan.ScanInfo.ScanFile & scan_key).fetch('file_path')[0]
    recording_dir = scan_file.parent

    miniscope_analysis_dir = recording_dir / 'miniscope_analysis'
    if miniscope_analysis_dir.exists():
        imaging.ProcessingTask.insert1({**scan_key,
                                        'paramset_idx': 0,
                                        'processing_output_dir': miniscope_analysis_dir.as_posix()})
# -



# + To this end, we make use of a convenient function `imaging.Curation().create1_from_processing_task()`

for key in (imaging.ProcessingTask - imaging.Curation).fetch('KEY'):
    imaging.Curation().create1_from_processing_task(key)

# ### Method for populating tables

from workflow_miniscope.populate import populate
populate(display_progress=False)
