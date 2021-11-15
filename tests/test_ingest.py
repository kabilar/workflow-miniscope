import pathlib
import sys

#TODO change caiman2D_paramset
from . import (dj_config, pipeline, subjects_csv, ingest_subjects,
               sessions_csv, ingest_sessions,
               testdata_paths, caiman_paramset, recording)


def test_ingest_subjects(pipeline, ingest_subjects):
    subject = pipeline['subject']
    assert len(subject.Subject()) == 1


def test_ingest_sessions(pipeline, sessions_csv, ingest_sessions):
    miniscope = pipeline['miniscope']
    session = pipeline['session']
    get_miniscope_root_data_dir = pipeline['get_miniscope_root_data_dir']

    assert len(session.Session()) == 2

    sessions, _ = sessions_csv
    sess = sessions.iloc[0]
    sess_dir = pathlib.Path(sess.session_dir).relative_to(get_miniscope_root_data_dir())

    assert (session.SessionDirectory
            & {'subject': sess.name}).fetch1('session_dir') == sess_dir.as_posix()


def test_find_valid_full_path(pipeline, sessions_csv):
    from element_data_loader.utils import find_full_path

    miniscope_root_data_dir = pipeline['get_miniscope_root_data_dir']

    # add more options for root directories
    if sys.platform == 'win32':
        miniscope_root_data_dir = [miniscope_root_data_dir(), 'J:/', 'M:/']
    else:
        miniscope_root_data_dir = [miniscope_root_data_dir(), 'mnt/j', 'mnt/m']
    # test: providing relative-path: correctly search for the full-path
    sessions, _ = sessions_csv
    sess = sessions.iloc[0]
    session_full_path = pathlib.Path(sess.session_dir)

    rel_path = pathlib.Path(session_full_path).relative_to(
        pathlib.Path(miniscope_root_data_dir()))
    full_path = find_full_path(miniscope_root_data_dir, rel_path)

    assert full_path == session_full_path


def test_find_root_directory(pipeline, sessions_csv):
    from element_data_loader.utils import find_root_directory

    miniscope_root_data_dir = pipeline['get_miniscope_root_data_dir']

    # add more options for root directories
    # if sys.platform == 'win32':
    #     miniscope_root_data_dir = [get_miniscope_root_data_dir(), 'J:/', 'M:/']
    # else:
    #     miniscope_root_data_dir = [get_miniscope_root_data_dir(), 'mnt/j', 'mnt/m']

    # test: providing full-path: correctly search for the root_dir
    sessions, _ = sessions_csv
    sess = sessions.iloc[0]
    session_full_path = pathlib.Path(sess.session_dir)

    root_dir = find_root_directory(miniscope_root_data_dir, session_full_path)

    assert root_dir == get_miniscope_root_data_dir()


def test_paramset_insert(motion_correction_minian_paramset, segmentation_minian_paramset, pipeline):
    miniscope = pipeline['miniscope']
    from element_data_loader.utils import dict_to_uuid

    method, desc, paramset_hash = (miniscope.ProcessingParamSet & {'paramset_idx': 0}).fetch1(
        'processing_method', 'paramset_desc', 'param_set_hash')
    assert method == 'minian'
    assert desc == 'Miniscope analysis with minian using default minian parameters'
    assert dict_to_uuid(motion_correction_minian_paramset) == paramset_hash

    #TODO change description in line 84
    method, desc, paramset_hash = (miniscope.ProcessingParamSet & {'paramset_idx': 1}).fetch1(
        'processing_method', 'paramset_desc', 'param_set_hash')
    assert method == 'minian'
    assert desc == 'Calcium miniscope analysis' \
                   ' with CaImAn using default CaImAn parameters for 2d planar images'
    assert dict_to_uuid(segmentation_minian_paramset) == paramset_hash

