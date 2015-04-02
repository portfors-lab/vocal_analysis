Vocal Analysis Codez
=====================

match_bout_behaviours.py
-------------------------

This script matches up Avisoft output on bout times, and ELAN output on behaviour times. It matches a behaviour for each bout (if any), by finding which bouts occur entirely within the time bounds of a behavioural event. Will process many files in a batch and produces a single file as output. Provided to the program is a directory location for all bout time files, another for behaviour time files, another for the excel sheet that contains their time offset (which must be in seconds in cell Z2) and optionally, the location to save the output file to. Each matching pair of bout and behaviour files *must* start with the same identifier. The program will expect the excel sheet with the time sync info to be nested in another directory, below the one given at the command line.

To use this from the CLI:

    $ python match_bout_behaviours.py "<bout file directory>" "<behaviour file directory>" "<sync file directory>" "<output directory (optional)>"

directory locations may be relative or absolute. It is espeically important to enclose them in quotes if executing this on a windows machine from bash.
