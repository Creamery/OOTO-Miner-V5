# OOTO-Miner-Python
Run the OOTO_Driver.py script to start the program. It should show a Tkinter UI window.

This is the full Python implementation of the OOTO Miner based off of its Java implementation (see OOTO-Miner-Java). It is much lighter and faster.

Manual Mining:
- The Out of the Ordinary (OOTO) Miner is a data mining application that analyses two groups of data - taken from a single data set - and mines out the features that make them different (or rather, out of the ordinary) from each other. The tests used to compare the two group sof data are chi-test and z-test. 

Automated Mining:
- Automatically groups all possible feature groups and filters out unnecessary groups. It then applies the mining algorithm to all generated features. Its output can be visualized in the AM tab.

# Requirements
- Runs in Python 2.7
- Install Tkinter
- Install XlsxWriter (run 'pip install XlsxWriter' in terminal)
- Install Pillow (run 'pip install Pillow' in terminal)
- Install scipy and numpy
- Install pandas
- Install enum
- Install sklearn

