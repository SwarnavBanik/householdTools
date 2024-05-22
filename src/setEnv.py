"""
###############################################################################
Code for setting up the environment
###############################################################################
Created:    Swarnav Banik on Apr 08, 2023
"""

import sys 
import socket

pc = socket.gethostname()
if pc == 'sbanik-6CD80J3':
   srcDir = '/home/sbanik/Documents/Github/pics/experimental/sbanik/generalTools/src'
   sys.path.insert(1, srcDir) 
   dataDir_oscScope = '/home/sbanik/Documents/data/oscScope'
   dataDir_esa = '/home/sbanik/Documents/data/esa'
elif pc == 'Swarnavs-MacBook-Air.local':
   srcDir = '/Users/sbanik/Documents/Github/pics/experimental/sbanik/generalTools/src'
   sys.path.insert(1,srcDir)  
   dataDir_oscScope = '/Users/sbanik/Documents/data/oscScope'
   dataDir_esa = '/Users/sbanik/Documents/data/esa'
elif pc == 'Swarnavs-Air.attlocal.net':
   srcDir = '/Users/sbanik/Documents/Github/pics/experimental/sbanik/generalTools/src'
   sys.path.insert(1,srcDir)  
   dataDir_oscScope = '/Users/sbanik/Documents/data/oscScope'
   dataDir_esa = '/Users/sbanik/Documents/data/esa'
else:
    raise Exception('setEnv: New Computer detected. Please add the default paths for your computer here.') 
import frmtFig as frmtFig
clrPts, cMap_phase = frmtFig.frmtFig()


