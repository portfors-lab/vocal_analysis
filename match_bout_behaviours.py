"""Finds which behaviour is associated with each bout. Provided as
Command line arguments are directory paths to the location of auto-generated 
bout and behaviour files, and optionally an output location.
"""
import glob
import os
import re

import pandas as pd
import numpy as np

def match_bout_to_behaviour(bout_file, behaviour_file, animal_id):
    """Associates a behaviour to each bout, by finding which bouts are
    contained within behvaiour events.

    Args:
        bout_file : File ouput from avisoft with columns <start time>, <end time> (seconds), 
                    each row represents a bout
        behaviour_file : ELAN output file with  columns <start time>, <duration>, 
                         <behaviour type>, each row represents a behaviour event.
        animal_id : Identifier to associate bouts found with the input files

    Returns:
        (pandas.DataFrame) -- a DataFrame with columns ['bout', 'behaviour']
    """
    # use panads for import, does a better job than most
    behav =  pd.read_csv(behaviour_file, delimiter='\t', names=['start', 'duration', 'behaviour'])

    # bout file imports funny, with a lot of extra columns
    # using the appropriate \t delimiter is worse for some reason
    bout_times = pd.read_csv(bout_file, sep='\s', header=None, skiprows=1)
    bout_times = bout_times.iloc[:,0:2] # so just remove extra columns
    bout_times.columns = ['start', 'end']

    bout_behaviours = pd.DataFrame(columns=['bout', 'behaviour'])
    # may be a more efficient way to do this, but iterate over bouts for now
    for bout_num, bout in bout_times.iterrows():
        # find the behavour that the bout is contained in
        logical_index_array = np.logical_and(behav['start'] < bout['start'], behav['start'] + behav['duration'] > bout['end'])
        behav_row = np.where(logical_index_array)[0]
        if len(behav_row) > 0:
            # behaviours do not overlap, so there can be only one
            behav_row = behav_row[0]
            bout_behaviours.loc[bout_num, 'bout'] =  animal_id + '_bout_' + str(bout_num)
            bout_behaviours.loc[bout_num, 'behaviour'] = behav.loc[behav_row, 'behaviour']
    return bout_behaviours


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print '''Not enough arguments. Usage:\n
        python bout_behaviours.py <bout file directory> <behaviour file directory> <output directory>
        '''
        sys.exit(-1)

    bout_dir = sys.argv[1]
    behave_dir = sys.argv[2]
    if len(sys.argv) > 3:
        outfile = os.path.join(sys.argv[3],'bout_behaviours.csv')
    else:
        outfile = 'bout_behaviours.csv'

    # find all .lbl files, then find .txt behavour file to match
    bout_files = glob.glob(os.path.join(bout_dir,'*.lbl'))

    all_bouts =  pd.DataFrame(columns=['bout', 'behaviour'])
    for bout_file in bout_files:
        # find matching behaviour file

        # separate filenames from the filepath
        bout_fname = os.path.basename(bout_file)
        match = re.match('[a-zA-Z0-9]+_[a-zA-Z0-9]+_[a-zA-Z0-9]+', bout_fname)
        if match is None:
            print 'Found invalid file name', bout_file
            continue
        prefix = match.group(0)
        behaviour_file = glob.glob(os.path.join(behave_dir, prefix + '*ehavior*.txt'))
        # glob returns a list, there should be only a single match
        if len(behaviour_file) == 0:
            print 'No behavour file for ', prefix
            continue
        elif len(behaviour_file) > 1:
            print 'Mutltiple matches for behaviour file ', behaviour_file
        behaviour_file = behaviour_file[0]
        print 'Matched {} file to {}'.format(bout_file, behaviour_file)
        
        bb = match_bout_to_behaviour(bout_file, behaviour_file, prefix)
        all_bouts = all_bouts.append(bb, ignore_index=True)

    print 'Finished finding bout behaviours. Bouts processed: ', len(all_bouts)
    all_bouts.to_csv(outfile, index=False) # do not include column numbers
