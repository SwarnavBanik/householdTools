"""
###############################################################################
Code for estimating investment profits.
###############################################################################
Created:    Swarnav Banik on Apr 23, 2024
"""
import sys
import logging
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

sys.path.append('../')
from src.financialTools.investments import incomeDist
from src.financialTools.investments import invstPortfolio
from src.frmtFig import frmtFig 

clrPts, mpl, plt = frmtFig(mpl, plt, FS_title = 18, FS_tickLabel = 18, FS_axisLabel = 18)

CODENAME = 'invstPortfolioManagement'
# %% Inputs ###################################################################

term                = 20
prnc_checkAccts     = 3500
prnc_savAccts       = 28000
prnc_cd             = 117186
prnc_stocks         = 35080
prnc_treasury       = 20538
prnc_401k           = 23535


# %% Single Instance ##########################################################
invstPortfolio = invstPortfolio(prncs = [prnc_checkAccts, prnc_savAccts, prnc_cd, \
                                        prnc_stocks, prnc_treasury, prnc_401k], term_years = term)     

fig = plt.figure(0,figsize=(12,2*6))
gs  = GridSpec(2,1)
axs1 = fig.add_subplot(gs[0,0])
invstPortfolio.plotGrowth_value(axs1, accounts = 'total')
axs2 = fig.add_subplot(gs[1,0])
invstPortfolio.plotGrowth_value(axs2, accounts = 'all')


