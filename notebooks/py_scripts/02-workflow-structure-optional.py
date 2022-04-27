# -*- coding: utf-8 -*-
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

# ## Workflow structure
#
# ### Setup
#
# This notebook gives a brief overview of the workflow structure and introduces some useful DataJoint tools to facilitate the exploration.
#
# + DataJoint needs to be configured before running this notebook, see [01-configure](01-configure.ipynb).
#
# + If you are familiar with DataJoint and the workflow structure, proceed to [03-process](03-process.ipynb).
#
# + For a more thorough introduction of DataJoint, please visit our [general tutorial site](https://playground.datajoint.io)
#
# To load the local config, we will change the directory to the package root.

import os
# change to the upper level folder to detect dj_local_conf.json
if os.path.basename(os.getcwd())=='notebooks': os.chdir('..')
assert os.path.basename(os.getcwd())=='workflow-miniscope', (
    "Please move to the workflow directory")
import datajoint as dj

# ### Schemas and tables

import datajoint as dj
from workflow_miniscope.pipeline import lab, subject, session, miniscope

# Each module contains a schema object that enables interaction with the schema in the database.

# + Each module imported above corresponds to one schema inside the database. For example, `ephys` corresponds to `neuro_ephys` schema in the database.
miniscope.schema

# + The table classes in the module corresponds to a table in the schema in the database.

# + Each datajoint table class inside the module corresponds to a table inside the schema. For example, the class `ephys.EphysRecording` correponds to the table `_ephys_recording` in the schema `neuro_ephys` in the database.
# preview columns and contents in a table
miniscope.Activity()

# + The first time importing the modules, empty schemas and tables will be created in the database. [markdown]
# # + By importing the modules for the first time, the schemas and tables will be created inside the database.
#
# # + Once created, importing modules will not create schemas and tables again, but the existing schemas/tables can be accessed and manipulated by the modules.
# + The schemas and tables will not be re-created when importing modules if they have existed. [markdown]
# ### Tools to explore
#
# # + `dj.list_schemas()`: list all schemas a user has access to in the current database
# + `dj.list_schemas()`: list all schemas a user could access.
dj.list_schemas()

# + `dj.Diagram()`: plot tables and dependencies in a schema. 

# + `dj.Diagram()`: plot tables and dependencies
# plot diagram for all tables in a schema
dj.Diagram(miniscope)
# -

# **Table tiers**: 
#
# - Manual table: green box, manually inserted table, expect new entries daily (e.g. `Recording`, `Recording`).  
# - Lookup table: gray box, pre-inserted table, commonly used for general facts or parameters (e.g., `ActivityExtractionMethod`).  
# - Imported table: blue oval, auto-processing table, the processing depends on the importing of external files (e.g., `MotionCorrection` depends on CaImAn files).  
# - Computed table: red circle, auto-processing table, the processing does not depend on files external to the database, commonly used for using scripts within the dataframe to process data. - Part table: plain text, as an appendix to the master table, all the part entries of a given master entry represent a intact set of the master entry (e.g., an activity trace under `Activity`).
#
# **Dependencies**:  
#
# - One-to-one primary: thick solid line, share the exact same primary key, meaning the child table inherits all the primary key fields from the parent table as its own primary key.     
# - One-to-many primary: thin solid line, inherit the primary key from the parent table, but have additional field(s) as part of the primary key as well
# - Secondary dependency: dashed line, the child table inherits the primary key fields from parent table as its own secondary attribute.

# + `dj.Diagram()`: plot the diagram of the tables and dependencies. It could be used to plot tables in a schema or selected tables.
# plot diagram of tables in multiple schemas
dj.Diagram(subject) + dj.Diagram(session) + dj.Diagram(miniscope)
# -

# plot diagram of selected tables and schemas
dj.Diagram(subject.Subject) + dj.Diagram(session.Session) + dj.Diagram(miniscope)

# + `heading`: [markdown]
# # + `describe()`: show table definition with foreign key references.
# -
miniscope.Activity.describe();

# + `heading`: show attribute definitions regardless of foreign key references

# + `heading`: show table attributes regardless of foreign key references.
miniscope.Activity.heading

# + ephys [markdown]
# ### Supporting Elements
#
# # + [Lab](https://github.com/datajoint/element-lab): lab management related information, such as Lab, User, Project, Protocol, Source.
# -

dj.Diagram(lab)

# + [Subject](https://github.com/datajoint/element-animal): general animal information, User, Genetic background, Death etc.

dj.Diagram(subject)

# + [subject](https://github.com/datajoint/element-animal): contains the basic information of subject, including Strain, Line, Subject, Zygosity, and SubjectDeath information.
subject.Subject.describe();

# + [Session](https://github.com/datajoint/element-session): General information of experimental sessions.

dj.Diagram(session)

# + [session](https://github.com/datajoint/element-session): experimental session information
session.Session.describe();

# + [Miniscope](https://github.com/datajoint/element-miniscope): Raw scan and processed data

# + [probe and ephys](https://github.com/datajoint/element-array-ephys): Neuropixel based probe and ephys tables
dj.Diagram(miniscope)
# -

# ## Summary and next step
#
# This notebook introduced the overall structures of the schemas and tables in the workflow and relevant tools to explore the schema structure and table definitions.
#
# In the next notebook [03-process](03-process.ipynb), we will introduce the detailed steps to run through `workflow-miniscope`.
