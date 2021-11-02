import numpy as np

from . import (dj_config, pipeline, subjects_csv, ingest_subjects,
               sessions_csv, ingest_sessions,
               testdata_paths, caiman2D_paramset, processing)


# def test_scan_info_populate_scanimage_2D(testdata_paths, pipeline, scan_info):
#     scan = pipeline['scan']
#     rel_path = testdata_paths['scanimage_2d']
#     scan_key = (scan.ScanInfo & (scan.ScanInfo.ScanFile
#                                  & f'file_path LIKE "%{rel_path}%"')).fetch1('KEY')
#     nfields, nchannels, ndepths, nframes = (scan.ScanInfo & scan_key).fetch1(
#         'nfields', 'nchannels', 'ndepths', 'nframes')

#     assert nfields == 1
#     assert nchannels == 2
#     assert ndepths == 1
#     assert nframes == 25000


# def test_scan_info_populate_scanimage_3D(testdata_paths, pipeline, scan_info):
#     scan = pipeline['scan']
#     rel_path = testdata_paths['scanimage_3d']
#     scan_key = (scan.ScanInfo & (scan.ScanInfo.ScanFile
#                                  & f'file_path LIKE "%{rel_path}%"')).fetch1('KEY')
#     nfields, nchannels, ndepths, nframes = (scan.ScanInfo & scan_key).fetch1(
#         'nfields', 'nchannels', 'ndepths', 'nframes')

#     assert nfields == 3
#     assert nchannels == 2
#     assert ndepths == 3
#     assert nframes == 2000


def test_processing_populate(processing, pipeline):
    miniscope = pipeline['miniscope']
    nframes, px_height, px_width = miniscope.RecordingInfo.fetch1('nframes', 'px_height', 'px_width')

    assert len(miniscope.RecordingInfo()) == 1
    assert nframes == 111770
    assert px_height == 600
    assert px_width == 600


