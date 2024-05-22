"""
###############################################################################
Code for estimating the cost House Ownership v/s renting.
###############################################################################
Created:    Swarnav Banik on Apr 08, 2024
"""
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt

sys.path.append('../')
from src.financialTools.houseOwnCost import rentVSbuy
from src.frmtFig import frmtFig 

clrPts, mpl, plt = frmtFig(mpl, plt, FS_title = 18, FS_tickLabel = 18, FS_axisLabel = 18)

# %% Inputs ###################################################################
housePrice          = 1.0E6
downPay             = 200E3
term                = 30
mortgageRate        = 7/100
realEstateAppRate   = 4.16/100
invstAppRate        = 6/100
startRent           = 4050
annualIncome        = 400E3

# %% Evaluate  ################################################################
rentvsbuySet = rentVSbuy(housePrice, downPay, startRent, term = term, \
          realEstateAppRate = realEstateAppRate, mortgageRate = mortgageRate, \
          taxCredits= True, annualIncome = annualIncome, invstAppRate = invstAppRate)

# %% Plot #####################################################################  
rentvsbuySet.plotTermTrend(0)

