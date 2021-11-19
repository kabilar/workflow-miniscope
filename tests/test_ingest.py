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

