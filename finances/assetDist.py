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
from src.frmtFig import frmtFig 

clrPts, mpl, plt = frmtFig(mpl, plt, FS_title = 18, FS_tickLabel = 18, FS_axisLabel = 18)
CODENAME = 'assetDist'

# %% Inputs ###################################################################

# term                = 20
# annualIncome        = 210E3 
# prnc_checkAccts     = 3500
# prnc_savAccts       = 28000
# prnc_cd             = 117186
# prnc_stocks         = 35080
# prnc_treasury       = 20632
# prnc_401k           = 23535


term                = 20
annualIncome        = 210E3 
prnc_checkAccts     = 0
prnc_savAccts       = 26964
prnc_cd             = 10000
prnc_stocks         = 34907
prnc_treasury       = 20538
prnc_401k           = 26853



stocks_splitRatio   = 0.25
cd_splitRatio       = 0.25

# %% Single Instance ##########################################################
wealth = incomeDist(annualIncome, annualExpense = 40E3, \
             contb401k_self = 23E3, contb401k_empl = 5950, contb401k_start = prnc_401k,\
             contbTreasury  = 10E3, contbTreasury_start = prnc_treasury, \
             stocks_splitRatio = stocks_splitRatio, stocks_start = prnc_stocks,\
             cd_splitRatio = cd_splitRatio, cd_start = prnc_cd,\
             sav_start = prnc_savAccts, check_start = prnc_checkAccts,\
             inRt = np.array([0, 3.5, 5, 6.9, 5, 6.9])/100, \
             term_years = term )

fig = wealth.printAnnualIncomeDist(0) 

fig = plt.figure(1,figsize=(12,2*6))
gs  = GridSpec(2,1)
axs1 = fig.add_subplot(gs[0,0])
wealth.portfolio.plotGrowth_value(axs1, accounts = 'total')
axs2 = fig.add_subplot(gs[1,0])
wealth.portfolio.plotGrowth_value(axs2, accounts = 'all')

fig = plt.figure(2,figsize=(12,2*6))
gs  = GridSpec(2,1)
axs1 = fig.add_subplot(gs[0,0])
wealth.portfolio.plotGrowth_value(axs1, accounts = 'total')
axs2 = fig.add_subplot(gs[1,0])
wealth.portfolio.plotGrowth_value(axs2, accounts = 'all-wrt-total')
wealth.portfolio.plotGrowth_value(axs2, accounts = 'total')
#%%

# fig = plt.figure(3,figsize=(12,1*6))
# gs  = GridSpec(1,1)
# axs1 = fig.add_subplot(gs[0,0])
# axs1 = wealth.portfolio.plotGrowth_value(axs1, accounts = 'volatile-wrt-total')
# axs1 = wealth.portfolio.plotGrowth_value(axs1, accounts = 'liquid and non-volatile')
# axs1.set(ylim = [0, 1])

# fig = plt.figure(3,figsize=(12,2*6))
# gs  = GridSpec(2,1)
# axs1 = fig.add_subplot(gs[0,0])
# wealth.portfolio.plotGrowth_value(axs1, accounts = 'volatile')
# axs2 = fig.add_subplot(gs[1,0])
# wealth.portfolio.plotGrowth_value(axs2, accounts = 'all')

# fig = plt.figure(4,figsize=(12,2*6))
# gs  = GridSpec(2,1)
# axs1 = fig.add_subplot(gs[0,0])
# wealth.portfolio.plotGrowth_value(axs1, accounts = 'liquid')
# axs2 = fig.add_subplot(gs[1,0])
# wealth.portfolio.plotGrowth_value(axs2, accounts = 'all')

# fig = plt.figure(5,figsize=(12,2*6))
# gs  = GridSpec(2,1)
# axs1 = fig.add_subplot(gs[0,0])
# wealth.portfolio.plotGrowth_value(axs1, accounts = 'liquid and non-volatile')
# axs2 = fig.add_subplot(gs[1,0])
# wealth.portfolio.plotGrowth_value(axs2, accounts = 'all')

# %% Hard Cash Management #####################################################
# fig = plt.figure(6,figsize=(12,2*6))
# gs  = GridSpec(2,1)
# axs1 = fig.add_subplot(gs[0,0]) 
# axs2 = fig.add_subplot(gs[1,0]) 

# cd_ratio = np.linspace(0, 0.7, 5)
# for ii in range(len(cd_ratio)):
#     wealth = incomeDist(annualIncome, annualExpense = 40E3, \
#                  contb401k_self = 23E3, contb401k_empl = 6E3, contb401k_start = prnc_401k,\
#                  contbTreasury = 10E3, contbTreasury_start = prnc_treasury, \
#                  stocks_splitRatio = stocks_splitRatio, stocks_start = prnc_stocks,\
#                  cd_splitRatio = cd_ratio[ii], cd_start = prnc_cd,\
#                  sav_start = prnc_savAccts, check_start = prnc_checkAccts,\
#                  inRt = np.array([0, 4.5, 5, 6.9, 5, 6.9])/100, \
#                  term_years = 30 )
#     tot_cost_true, tot_cost_false, tot_value_true, tot_value_false = wealth.portfolio.getCondAssets('liquid and non-volatile')
#     line1, = axs1.plot(wealth.months/12, tot_value_true*1E-6, '-', linewidth = 3, \
#               label = '$\\left[{\\rm I}_{\\rm stocks}+{\\rm I}_{\\rm cd}\\right]/{\\rm I}_{\\rm tot}$'+f' = {cd_ratio[ii] + stocks_splitRatio:.2f}')
#     axs2.plot(wealth.months/12, wealth.portfolio.value_CIP*1E-6, '-', linewidth = 3, color = line1.get_color(),\
#               label = '$\\left[{\\rm I}_{\\rm stocks}+{\\rm I}_{\\rm cd}\\right]/{\\rm I}_{\\rm tot}$'+f' = {cd_ratio[ii] + stocks_splitRatio:.2f}') 

# axs1.legend()
# axs1.grid('major')
# axs1.set_ylabel('Hard Cash (M $)')
# axs2.grid('major')
# axs2.set_ylabel('Total Assets (M $)')
# axs2.set_xlabel('Years') 

# # %% Volatality Management ####################################################

# fig = plt.figure(7,figsize=(12,3*6))
# gs  = GridSpec(3,1)
# axs1 = fig.add_subplot(gs[0,0]) 
# axs2 = fig.add_subplot(gs[1,0]) 
# axs3 = fig.add_subplot(gs[2,0]) 

# stock_ratio = np.linspace(0, 0.5, 5)
# hardcash = np.zeros(np.shape(cd_ratio))
# for ii in range(len(cd_ratio)):
#     wealth = incomeDist(annualIncome, annualExpense = 40E3, \
#                  contb401k_self = 23E3, contb401k_empl = 6E3, contb401k_start = prnc_401k,\
#                  contbTreasury = 10E3, contbTreasury_start = prnc_treasury, \
#                  stocks_splitRatio = stock_ratio[ii], stocks_start = prnc_stocks,\
#                  cd_splitRatio = cd_splitRatio, cd_start = prnc_cd,\
#                  sav_start = prnc_savAccts, check_start = prnc_checkAccts,\
#                  inRt = np.array([0, 4.5, 5, 6.9, 5, 6.9])/100, \
#                  term_years = 30 )
#     tot_cost_true, tot_cost_false, tot_value_true, tot_value_false = wealth.portfolio.getCondAssets('volatile')
#     line1, = axs1.plot(wealth.months/12, tot_value_false*1E-6, '-', linewidth = 3, \
#               label = '${\\rm I}_{\\rm stocks}/{\\rm I}_{\\rm tot}$'+f' = {stock_ratio[ii]:.2f}')  
#     axs2.plot(wealth.months/12, wealth.portfolio.value_CIP*1E-6, '-', linewidth = 3, color = line1.get_color(),\
#               label = '${\\rm I}_{\\rm stocks}/{\\rm I}_{\\rm tot}$'+f' = {stock_ratio[ii]:.2f}') 
#     axs3.plot(wealth.months/12, tot_value_false/wealth.portfolio.value_CIP, '-', linewidth = 3, color = line1.get_color(),\
#               label = '${\\rm I}_{\\rm stocks}/{\\rm I}_{\\rm tot}$'+f' = {stock_ratio[ii]:.2f}') 
        
# axs1.legend()
# axs1.grid('major')
# axs1.set_ylabel('Non Volatile Assets \n A$_{\\rm non-vol}$ (M)')
# axs2.grid('major')
# axs2.set_ylabel('Total Assets \n A$_{\\rm tot}$ (M)')
# axs3.grid('major')
# axs3.set_ylabel('Non Volatile Fraction \n $\\frac{{\\rm A}_{\\rm non-vol}}{{\\rm A}_{\\rm tot}}$')
# axs3.set(ylim = [0, 1])
# axs3.set_xlabel('Years') 



