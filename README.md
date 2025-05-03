# STV Calculator

*By slimmy*

How to use:

1. Export election results into a csv file, formatted as the following:
    a. First row is contains each candidate's name
    b. The next rows are the ranking of each ballot, where the lowest number indicates the highest rank, 
    unless it is blank or 0 in which case it is considered "unranked"

2. Edit 'INPUT_FILE' and 'NUM_SEATS' to your csv file name and the number of seats to calculate

3. Run 'stv.py' with python from the project folder

(optional) Use 'STANDINGS_EVERY_ELECTED' and 'STANDINGS_EVERY_ELIM' to set how often standings should be printed. 'STANDINGS_EVERY_ELIM' must also have 'STANDINGS_EVERY_ELECTED', 'STANDINGS_EVERY_ELIM' will not print on eliminations of candidates with no votes

(Note) This program was designed around displaying results in a command line or text document