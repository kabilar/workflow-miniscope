import pathlib
import csv
from datetime import datetime

from .pipeline import subject, scan, session, event, trial, Equipment
from .paths import get_imaging_root_data_dir


def ingest_general(csvs, tables, skip_duplicates=True, verbose=True,
                   allow_direct_insert=False):
    """
    Inserts data from a series of csvs into their corresponding table:
        e.g., ingest_general(['./lab_data.csv', './proj_data.csv'],
                                 [lab.Lab(),lab.Project()]
    ingest_general(csvs, tables, skip_duplicates=True, verbose=True,
                   allow_direct_insert=False)
        :param csvs: list of relative paths to CSV files.  CSV are delimited by commas.
        :param tables: list of datajoint tables with ()
        :param verbose: print number inserted (i.e., table length change)
        :param skip_duplicates: skip items that are either (a) duplicates within the csv
                                or (b) already exist in the corresponding table
        :param allow_direct_insert: Permit insertion directly into calculated tables
    """
    for csv_filepath, table in zip(csvs, tables):
        with open(csv_filepath, newline='') as f:
            data = list(csv.DictReader(f, delimiter=','))
        if verbose:
            prev_len = len(table)
        table.insert(data, skip_duplicates=skip_duplicates,
                     # Ignore extra fields because some CSVs feed multiple tables
                     ignore_extra_fields=True, allow_direct_insert=allow_direct_insert)
        if verbose:
            insert_len = len(table) - prev_len     # report length change
            print(f'\n---- Inserting {insert_len} entry(s) '
                  + f'into {table.table_name} ----')


def ingest_subjects(subject_csv_path='./user_data/subjects.csv',
                    skip_duplicates=True, verbose=True):
    """
    Ingest subjects listed in the subject column of ./user_data/subjects.csv
    """
    csvs = [subject_csv_path]
    tables = [subject.Subject()]

    ingest_general(csvs, tables, skip_duplicates=skip_duplicates, verbose=verbose)


def ingest_sessions(session_csv_path='./user_data/sessions.csv', verbose=True,
                    skip_duplicates=False):
    root_data_dir = get_imaging_root_data_dir()

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
            raise FileNotFoundError('Unable to identify scan files from the supported'
                                    + ' acquisition softwares (Miniscope-DAQ-V3) at: '
                                    + {sess_dir})

        if acq_software == 'Miniscope-DAQ-V3':
            daq_v3_fp = pathlib.Path(scan_filepaths[0])
            recording_time = datetime.fromtimestamp(daq_v3_fp.stat().st_ctime)
            scanner = 'Miniscope-DAQ-V3'
        else:
            raise NotImplementedError('Processing scan from acquisition software of '
                                      + f'type {acq_software} is not yet implemented')

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
    if verbose:
        print(f'\n---- Insert {new_equip} entry(s) into experiment.Equipment ----')
    Equipment.insert(scanner_list, skip_duplicates=True)

    if verbose:
        print(f'\n---- Insert {len(session_list)} entry(s) into session.Session ----')
    session.Session.insert(session_list)
    session.SessionDirectory.insert(session_dir_list)

    if verbose:
        print(f'\n---- Insert {len(scan_list)} entry(s) into scan.Scan ----')
    scan.Scan.insert(scan_list)

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
    ingest_general(csvs, tables, skip_duplicates=skip_duplicates, verbose=verbose,
                   allow_direct_insert=True)


def ingest_alignment(alignment_csv_path='./user_data/alignments.csv',
                     skip_duplicates=True, verbose=True):

    csvs = [alignment_csv_path]
    tables = [event.AlignmentEvent()]

    ingest_general(csvs, tables, skip_duplicates=skip_duplicates, verbose=verbose)


if __name__ == '__main__':
    ingest_subjects()
    ingest_sessions()
    ingest_events()
    ingest_alignment()
