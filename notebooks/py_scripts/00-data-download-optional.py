# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: venv-nwb
#     language: python
#     name: venv-nwb
# ---

# # DataJoint U24 - Workflow Miniscope
#
# ## Download example dataset
#
# `Coming soon: example data via djarchive`
#
# ## Install `djarchive-client`
#
# + The example dataset is hosted on `djarchive`, an AWS storage.
# + We provide a client package, [djarchive-client](https://github.com/datajoint/djarchive-client), to download the data which can be installed with pip:

pip install git+https://github.com/datajoint/djarchive-client.git

# ## Download miniscope dataset

import djarchive_client
client = djarchive_client.client()

# Browse the datasets that are available on `djarchive`:

list(client.datasets())

# Each of the datasets have different versions associated with the version of the `workflow-miniscope` package. Browse the revisions:

list(client.revisions())

# To download the dataset, let's prepare a root directory, for example in `/tmp`:

# mkdir /tmp/example_data

# Get the dataset revision with the current version of `workflow-miniscope`:

from workflow_miniscope import version
revision = version.__version__.replace('.', '_')
revision

# Run download for a given dataset and revision:

client.download('workflow-miniscope-test-set', target_directory='/tmp/example_data', 
                revision=revision)

# ## Directory structure
#
# After downloading, the directory will be organized as follows:
#
# ```
#     COMING SOON
# ```
#
# We will use the dataset for subject `X` as an example for the rest of the notebooks. If you use your own dataset for the workflow, change the path accordingly.
#
# ## Next step
#
# In the next notebook ([01-configure](01-configure.ipynb)) we will set up the configuration file for the workflow.


