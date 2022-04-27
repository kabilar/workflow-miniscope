import pathlib
import csv
from datetime import datetime
from element_interface.utils import ingest_csv_to_table

from .pipeline import subject, session, event, trial, Equipment
from .pipeline import miniscope as scan # NEEDS FIXING?
from .paths import get_miniscope_root_data_dir


def ingest_subjects(subject_csv_path='./user_data/subjects.csv',
                    skip_duplicates=True, verbose=True):
    """
    Ingest subjects listed in the subject column of ./user_data/subjects.csv
    """
    csvs = [subject_csv_path]
    tables = [subject.Subject()]

    ingest_csv_to_table(csvs, tables, skip_duplicates=skip_duplicates, verbose=verbose)


def ingest_sessions(session_csv_path='./user_data/sessions.csv', verbose=True,
                    skip_duplicates=False):
    root_data_dir = get_miniscope_root_data_dir()

    # ---------- Insert new "Session" and "Scan" ---------
    with open(session_csv_path, newline='') as f:
        input_sessions = list(csv.DictReader(f, delimiter=','))

    # Folder structure: root / subject / session / .avi (raw)
    session_list, session_dir_list, scan_list, scanner_list = [], [], [], []

    for sess in input_sessions:
        sess_dir = pathlib.Path(sess['session_dir'])

        # Search for Miniscope-DAQ-V3 files (in that order)
        for scan_pattern, scan_type, glob_func in zip(['ms*.avi'],
                                                      ['Miniscope-DAQ-V3'],
                                                      [sess_dir.glob]):
            scan_filepaths = [fp.as_posix() for fp in glob_func(scan_pattern)]
            if len(scan_filepaths):
                acq_software = scan_type
                break
        else:
            # raise FileNotFoundError('Unable to identify scan files from the supported'
            #                         + ' acquisition softwares (Miniscope-DAQ-V3) at: '
            #                         + {sess_dir})
            pass

        if acq_software == 'Miniscope-DAQ-V3':
            daq_v3_fp = pathlib.Path(scan_filepaths[0])
            recording_time = datetime.fromtimestamp(daq_v3_fp.stat().st_ctime)
            scanner = 'Miniscope-DAQ-V3'
        else:
            # raise NotImplementedError('Processing scan from acquisition software of '
            #                           + f'type {acq_software} is not yet implemented')
            pass

        session_key = {'subject': sess['subject'], 'session_datetime': recording_time}
        if session_key not in session.Session():
            scanner_list.append({'scanner': scanner})
            session_list.append(session_key)
            scan_list.append({**session_key, 'scan_id': 0, 'scanner': scanner,
                              'acq_software': acq_software})

            session_dir_list.append({**session_key,
                                     'session_dir': sess_dir.relative_to(root_data_dir
                                                                         ).as_posix()})

    new_equip = len(set(val for dic in scanner_list for val in dic.values()))
    # if verbose:
    #     print(f'\n---- Insert {new_equip} entry(s) into experiment.Equipment ----')
    # Equipment.insert(scanner_list, skip_duplicates=True)

    if verbose:
        print(f'\n---- Insert {len(session_list)} entry(s) into session.Session ----')
    session.Session.insert(session_list)
    session.SessionDirectory.insert(session_dir_list)

    # if verbose:
    #     print(f'\n---- Insert {len(scan_list)} entry(s) into scan.Scan ----')
    # scan.Scan.insert(scan_list)

    if verbose:
        print('\n---- Successfully completed ingest_sessions ----')


def ingest_events(recording_csv_path='./user_data/behavior_recordings.csv',
                  block_csv_path='./user_data/blocks.csv',
                  trial_csv_path='./user_data/trials.csv',
                  event_csv_path='./user_data/events.csv',
                  skip_duplicates=True, verbose=True):
    csvs = [recording_csv_path, recording_csv_path,
            block_csv_path, block_csv_path,
            trial_csv_path, trial_csv_path, trial_csv_path,
            trial_csv_path,
            event_csv_path, event_csv_path, event_csv_path]
    tables = [event.BehaviorRecording(), event.BehaviorRecording.File(),
              trial.Block(), trial.Block.Attribute(),
              trial.TrialType(), trial.Trial(), trial.Trial.Attribute(),
              trial.BlockTrial(),
              event.EventType(), event.Event(), trial.TrialEvent()]

    # Allow direct insert required bc element-trial has Imported that should be Manual
    ingest_csv_to_table(csvs, tables, skip_duplicates=skip_duplicates, verbose=verbose)
                        # allow_direct_insert=True)


def ingest_alignment(alignment_csv_path='./user_data/alignments.csv',
                     skip_duplicates=True, verbose=True):

    csvs = [alignment_csv_path]
    tables = [event.AlignmentEvent()]

    ingest_csv_to_table(csvs, tables, skip_duplicates=skip_duplicates, verbose=verbose)


if __name__ == '__main__':
    ingest_subjects()
    ingest_sessions()
    ingest_events()
    ingest_alignment()
