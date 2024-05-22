"""
###############################################################################
Code for extracting OSA data from csv files.
###############################################################################
Created:    Swarnav Banik on Dec 13, 2022
"""


import os
import csv
import pandas as pd

def extractCSV(path2file, fileType = 'gDoc', nRows = None):#, skipTopSection = False, skipUnitsRow = False, nRows = None):
    # extract data from a CSV file ####################################
    # Inputs:
    #   file:      CSV file path to be read
    # Outputs:
    #   df:        Data as a pandas dataframe
    ########################################################################
    if (os.path.isfile(path2file) == False): 
        raise Exception('osaDataExtract::extractCSV: File doesnt exist.')
    if fileType == 'gDoc':
        df = pd.read_csv(path2file, nrows = nRows)
    elif fileType == 'KS DSO Oscilloscope':
        df = pd.read_csv(path2file, nrows = nRows)
    elif fileType == 'Siglent ESA 3000':
        df = pd.read_csv(path2file, skiprows = [0], nrows = nRows, usecols =[0,1], header = None)
        df = df.rename(columns={0: "Frequency (Hz)", 1: "PSD (dBm)"})
    elif fileType == 'OSA':
        df = pd.read_csv(path2file, skiprows = [0], nrows = nRows, usecols =[0,1], header = None)
        df = df.rename(columns={0: "Wavelength (m)", 1: "PSD (dBm)"})
        
    #df = pd.read_csv(path2file, usecols= header)
    return df