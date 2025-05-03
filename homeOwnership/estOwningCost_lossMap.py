"""
###############################################################################
Code for estimating the House Ownership loss map.
###############################################################################
Created:    Swarnav Banik on Apr 28, 2025
"""
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.colors import TwoSlopeNorm

sys.path.append('../')
from src.frmtFig import frmtFig 
from src.financialTools.houseOwnCost import rentVSbuy
clrPts, mpl, plt = frmtFig(mpl, plt, FS_title = 18, FS_tickLabel = 18, FS_axisLabel = 18)

# %% Common Functions #########################################################

def plotLoss(figNo, idx, loss, loss_contour_M):
    
    vmin = np.min(loss[idx,:,:])*1E-6
    vmax = np.max(loss[idx,:,:])*1E-6
    norm = TwoSlopeNorm(vmin= vmin, vcenter= 0, vmax=vmax)
    
    fig = plt.figure(figNo,figsize=(8,6))
    gs  = GridSpec(1,1)
    axs = fig.add_subplot(gs[0,0])
    CS = axs.contourf(housePrice/1e6, mortgageRate*100, loss[idx,:,:]*1E-6, 
                      levels=100, cmap= 'RdBu_r', norm = norm) 
    C_5000 = axs.contour(housePrice/1e6,mortgageRate*100, loss[idx,:,:]*1E-6, 
                        levels=[loss_contour_M], colors = 'black', linewidths = 2)
    axs.clabel(C_5000, inline = True, fmt='  Loss = $ %0.3f M'  , fontsize=14)
    cbar = fig.colorbar(CS)
    cbar.set_label('Loss at 1 Year ($ M)')
    axs.set_xlabel('House Price ($ M)')
    axs.set_ylabel('Mortgage Rate (%)')
    axs.tick_params(axis='both', labelsize=14)
    plt.tight_layout()
    return fig, axs

# %% Inputs ###################################################################
housePrice_start          = 0.5E6
housePrice_end          = 3E6
mortgageRate_start            = 0.1/100
mortgageRate_end            = 10/100

term                = 30

realEstateAppRate   = 4.16/100
invstAppRate        = 5/100
startRent           = 4050
annualIncome        = 500E3
rentAppRate         = 5/100
N_mortgageRate      = 50
N_housePrice        = 50


housePrice = np.linspace(housePrice_start, housePrice_end, N_housePrice)
mortgageRate = np.linspace(mortgageRate_start, mortgageRate_end, N_mortgageRate)
housePrice, mortgageRate = np.meshgrid(housePrice, mortgageRate, indexing='xy')
loss = np.zeros((3,N_housePrice, N_mortgageRate))
for ii in range(N_housePrice):
    for jj in range(N_mortgageRate):
        rentvsbuySet = rentVSbuy(housePrice[ii,jj], 0.2*housePrice[ii,jj], 
                                 startRent, term = term, realEstateAppRate = realEstateAppRate, 
                                 mortgageRate = mortgageRate[ii,jj], \
                                 taxCredits = True, annualIncome = annualIncome, 
                                 invstAppRate = invstAppRate, rentAppRate = rentAppRate)
        loss[2,ii,jj] = rentvsbuySet.unrecoverCost_CM[-1]
        loss[1,ii,jj] = rentvsbuySet.unrecoverCost_CM[5*12]
        loss[0,ii,jj] = rentvsbuySet.unrecoverCost_CM[1*12]
        del rentvsbuySet


fig, axs = plotLoss(0, 0, loss, 0.010)
axs.set_title('Loss after 1 Year\n')
fig, axs = plotLoss(1, 1, loss, 0.050)
axs.set_title('Loss after 5 Year\n')
fig, axs = plotLoss(2, 2, loss, 0)
axs.set_title('Loss after 30 Year\n')
plt.show()

