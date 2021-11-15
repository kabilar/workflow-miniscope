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


def test_motion_correction_populate_caiman(curations, pipeline, testdata_paths):
    miniscope = pipeline['miniscope']

    rel_path = testdata_paths['caiman']
    curation_key = (miniscope.Curation
                    & f'curation_output_dir LIKE "%{rel_path}"').fetch1('KEY')

    miniscope.MotionCorrection.populate(curation_key)

    assert (miniscope.Curation * miniscope.ProcessingParamSet
            & curation_key).fetch1('processing_method') == 'caiman'

    assert len(miniscope.MotionCorrection.Block & curation_key) == 9

    x_shifts = (miniscope.MotionCorrection.RigidMotionCorrection
                & curation_key).fetch1('x_shifts')
    assert len(x_shifts) == (miniscope.RecordingInfo
                             & curation_key).fetch1('nframes')

    ave_img = (miniscope.MotionCorrection.Summary & curation_key).fetch1('average_image')
    img_width, img_height = (miniscope.RecordingInfo.Field & curation_key).fetch1(
        'px_width', 'px_height')
    assert ave_img.shape == (img_height, img_width)


def test_segmentation_populate_minian(curations, pipeline, testdata_paths):
    miniscope = pipeline['miniscope']

    rel_path = testdata_paths['minian']
    curation_key = (miniscope.Curation
                    & f'curation_output_dir LIKE "%{rel_path}"').fetch1('KEY')

    miniscope.MotionCorrection.populate(curation_key)
    miniscope.Segmentation.populate(curation_key)
    miniscope.Fluorescence.populate(curation_key)
    miniscope.Activity.populate(curation_key)

    assert (miniscope.Curation * miniscope.ProcessingParamSet
            & curation_key).fetch1('processing_method') == 'minian'

    assert len(miniscope.Segmentation.Mask & curation_key) == 57

    assert len(miniscope.MaskClassification.MaskType & curation_key
               & 'mask_classification_method = "minian_default_classifier"'
               & 'mask_type = "soma"') == 27

    assert len(miniscope.Fluorescence.Trace & curation_key & 'fluo_channel = 0') == 57
    assert len(miniscope.Activity.Trace & curation_key
               & 'fluo_channel = 0' & 'extraction_method = "minian_deconvolution"') == 57

    nframes = (miniscope.RecordingInfo & curation_key).fetch1('nframes')
    f, fneu = (miniscope.Fluorescence.Trace & curation_key
               & 'fluo_channel = 0' & 'mask = 0').fetch1(
        'fluorescence', 'neuropil_fluorescence')
    assert len(f) == len(fneu) == nframes


def test_segmentation_populate_caiman(curations, pipeline, testdata_paths):
    miniscope = pipeline['miniscope']


    rel_path = testdata_paths['caiman']
    curation_key = (miniscope.Curation
                    & f'curation_output_dir LIKE "%{rel_path}"').fetch1('KEY')

    miniscope.MotionCorrection.populate(curation_key)
    miniscope.Segmentation.populate(curation_key)
    miniscope.Fluorescence.populate(curation_key)
    miniscope.Activity.populate(curation_key)

    assert (miniscope.Curation * miniscope.ProcessingParamSet
            & curation_key).fetch1('processing_method') == 'caiman'

    assert len(miniscope.Segmentation.Mask & curation_key) == 30
    assert len(miniscope.Fluorescence.Trace * miniscope.MaskClassification.MaskType
               & curation_key & 'fluo_channel = 0') == 21
    assert len(miniscope.Activity.Trace * miniscope.MaskClassification.MaskType
               & curation_key & 'fluo_channel = 0'
               & 'extraction_method = "caiman_deconvolution"') == 21
    assert len(miniscope.Activity.Trace * miniscope.MaskClassification.MaskType
               & curation_key & 'fluo_channel = 0'
               & 'extraction_method = "caiman_dff"') == 21

    nframes = (miniscope.RecordingInfo & curation_key).fetch1('nframes')
    f = (miniscope.Fluorescence.Trace & curation_key
         & 'fluo_channel = 0' & 'mask = 1').fetch1('fluorescence')
    assert len(f) == nframes


