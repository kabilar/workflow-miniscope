import numpy as np
#TODO remove caiman2d_paramset
from . import (dj_config, pipeline, subjects_csv, ingest_subjects,
               sessions_csv, ingest_sessions,
               testdata_paths, caiman_paramset, recording, curations)


def test_daqv4_info_populate(testdata_paths, pipeline, recording):
    miniscope = pipeline['miniscope']
    nframes, px_height, px_width = miniscope.RecordingInfo.fetch1('nframes', 'px_height', 'px_width')
    rel_path = testdata_paths['miniscope_daqv4']


    assert nframes == 111770
    assert px_height == 600
    assert px_width == 600
    #TODO
    # assert rel_path ==  


def test_recordinginfo_populate(recording, pipeline):
    miniscope = pipeline['miniscope']

    assert len(miniscope.RecordingInfo()) == 1
