Vocal Analysis Codez
=====================

match_bout_behaviours.py
-------------------------

This script matches up Avisoft output on bout times, and ELAN output on behaviour times. It matches a behaviour for each bout (if any), by finding which bouts occur entirely within the time bounds of a behavioural event. Will process many files in a batch and produces a single file as output. Provided to the program is a directory location for all bout time files and another for behaviour time files, and optionally, the location to save the output file to. Each matching pair of bout and behaviour files *must* start with the same identifier.

To use this from the CLI:

    $ python match_bout_behaviours.py "<bout file directory>" "<behaviour file directory>" "<output directory (optional)>"

directory locations may be relative or absolute. It is espeically important to enclose them in quotes if executing this on a windows machine from bash.
