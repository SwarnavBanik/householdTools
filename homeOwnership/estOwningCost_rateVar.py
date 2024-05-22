"""
###############################################################################
Code for estimating the cost House Ownership v/s renting.
###############################################################################
Created:    Swarnav Banik on Apr 08, 2024
"""
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

sys.path.append('../')
from src.financialTools.houseOwnCost import rentVSbuy
from src.frmtFig import frmtFig 

clrPts, mpl, plt = frmtFig(mpl, plt, FS_title = 18, FS_tickLabel = 18, FS_axisLabel = 18)

# %% Inputs ###################################################################
housePrices         = np.linspace(0.5,1.5,5)*1E6
mortgageRates       = np.linspace(1,8,100)/100
downPayRate         = 20/100
term                = 30
realEstateAppRate   = 4.16/100
invstAppRate        = 6/100
startRent           = 4050
annualIncome        = 400E3

# %% Evaluate  ################################################################

fig = plt.figure(0,figsize=(12,2*6))
gs  = GridSpec(2,1)
axs1 = fig.add_subplot(gs[0,0])
axs2 = fig.add_subplot(gs[1,0])
for housePrice in housePrices:
    loss        = np.zeros(np.shape(mortgageRates))
    breakEvenPt = np.zeros(np.shape(mortgageRates))
    for ii in range(len(mortgageRates)):    
        rentvsbuySet = rentVSbuy(housePrice, housePrice*downPayRate, startRent, term = term, \
                  realEstateAppRate = realEstateAppRate, mortgageRate = mortgageRates[ii], \
                  taxCredits= True, annualIncome = annualIncome, invstAppRate = invstAppRate)
        loss[ii]        = rentvsbuySet.buyLoss
        breakEvenPt[ii] = rentvsbuySet.brekEvenPoint
    axs1.plot(mortgageRates*100, -loss*1E-6, '-', \
              linewidth = 4, label = f'House Price = $ {housePrice*1E-6:.2f} M')
    axs2.plot(mortgageRates*100, breakEvenPt/12, '.-', \
              linewidth = 4, label = f'House Price = $ {housePrice*1E-6:.2f} M')
axs1.legend()
axs1.grid('major')
axs1.set_ylabel('Net profit when owning ($ M)')
axs1.set_title('Renting v/s Buying')
axs1.set(xlim=( 0, 9 ))
axs1.set(ylim=( -2, 8 ))
axs2.grid('major')
axs2.set_ylabel('Break Even Point (years)')
axs2.set_xlabel('Mortgage Rate (%)') 
axs2.set(xlim=( 0, 9 ))
axs2.set(ylim=( -1, 31 ))






