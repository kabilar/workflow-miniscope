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

# # [WIP] DataJoint U24 Workflow Imaging
# This notebook will describe the steps for interacting with the data ingested into `workflow-miniscope`.  
#
# Prior to using this notebook, please refer to the [README](https://github.com/datajoint/workflow-imaging) for the topics listed below.  
#     + Installation instructions  
#     + Directory structure and file naming convention  
#     + Running the workflow  

# Change into the parent directory to find the `dj_local_conf.json` file. 
# When you type `import datajoint as dj` the credentials from `dj_local_conf.json` will be used to log into the database.
import os
os.chdir('..')

from workflow_imaging.pipeline import *

# ## Workflow architecture

dj.Diagram(lab)

dj.Diagram(subject)

dj.Diagram(scan)

dj.Diagram(imaging)

subject.Subject()

Session()

scan.ScanInfo()

scan.ScanInfo.Field()

imaging.ProcessingParamSet()

imaging.ProcessingTask()


