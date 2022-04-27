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
# To run `workflow-miniscope`, we need to properly set up the DataJoint configuration. The configuration will be saved in a file called `dj_local_conf.json` on each machine.
#
# The configuration only needs to be set up once.  If you have gone through the configuration before, directly go to [02-workflow-structure](02-workflow-structure-optional.ipynb).
#
# As a convention, we set the configuration up in the root directory of the `workflow-miniscope` package and always start importing DataJoint and pipeline modules from there.

import os
# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='workflow-miniscope', (
    "Please move to the workflow directory")
import datajoint as dj

# ## Configure database
#
# Now let's set up the host, user and password in the `dj.config` global variable

import getpass
dj.config['database.host'] = '{YOUR_HOST}'
dj.config['database.user'] = '{YOUR_USERNAME}'
dj.config['database.password'] = getpass.getpass() # enter the password securily

# You should be able to connect to the database at this stage.

dj.conn()

# ## Configure the `custom` field
#
# Each example workflow relies on requires certain information in the `custom` field of `dj.config`, including:
# - a database prefix
# - root directory information
#
# ### Database prefix
#
# A prefix helps you configure server settings, including user privileges. With the prefix `neuro_`, every schema created with the current workflow will start with `neuro_`, e.g. `neuro_lab`, `neuro_subject`, `neuro_imaging` etc. We can set this prefix within python:

dj.config['custom'] = {'database.prefix': 'neuro_'}

# ### Root directory
#
# `miniscope_root_data_dir` field indicates the root directory for the miniscope raw data. 
# In future updates to `element-miniscope` users will be able to specify multiple possible root directories as a list.
#
# From DataJoint's perspective, all files are relative to the root, so users could work on different machines, or data could be transferred from one machine to the next.
#
# Paths should be saved following the POSIX standards (Unix/Linux), with `/`. The path conversion for machines of any operating system is taken care of inside the elements.
#
# If using our example dataset, downloaded with this notebook [00-data-download](00-data-download-optional.ipynb), the root directory will be:

# If there is only one root path:
dj.config['custom']['miniscope_root_data_dir'] = '/tmp/example_data'
# If there are multiple possible root paths:
dj.config['custom']['miniscope_root_data_dir'] = ['/tmp/example_data']

dj.config

# ## Save the config as a json
#
# With the proper configurations, we could save this as a file, either as a local json file, or a global file.

dj.config.save_local()

# ls

# Local configuration file is saved as `dj_local_conf.json` in the root directory of this package `workflow-miniscope`. Next time you load DataJoint from this directory, these settings will also be loaded.
#
# If saved globally, there will be a hidden configuration file saved in your machine's root directory. The configuration will be loaded no matter where the directory is.

# +
# dj.config.save_global()
# -

# ## Next Step
#
# After the configuration, we will be able to run through the workflow with the [02-workflow-structure](02-workflow-structure-optional.ipynb) notebook.
