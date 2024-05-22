"""
###############################################################################
Common financialTools plotting functions
###############################################################################
Created:    Swarnav Banik on Apr 18, 2024
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from src.financialTools.houseOwnCost import homeOwnership
from src.financialTools.houseOwnCost import renting
from src.frmtFig import frmtFig 
clrPts, mpl, plt = frmtFig(mpl, plt, FS_title = 18, FS_tickLabel = 18, FS_axisLabel = 18)



def plotTermTrend(figNo, house:homeOwnership, rental:renting = [], house_noTC:homeOwnership = []):

    fig = plt.figure(figNo,figsize=(12,1*6))
    gs  = GridSpec(1,1)
    axs = fig.add_subplot(gs[0,0])
    
    line1 = (house.cost_CM_pTax+house.cost_CM_main) *1E-6
    line2 = house.unrecoverCost_CM*1E-6    
    if not rental == []:
        axs.plot(rental.months/12, (rental.cost_CM)*1E-6, '--', \
              linewidth = 3, color = clrPts[1], label = 'Cost of Renting')
    axs.plot(house.months/12, house.cost_CM*1E-6, '--', \
              linewidth = 3, color = clrPts[0], label = 'Cost of Owning')
    if not rental == []:
        axs.plot(rental.months/12, (rental.unrecoverCost_CM)*1E-6, '-', \
              linewidth = 4, color = clrPts[1], label = 'Unrcv. Cost of Renting')
        idx = np.argmin(np.abs(house.unrecoverCost_CM[12:] - rental.unrecoverCost_CM[12:]))
        axs.axvline(rental.months[idx]/12, ls = '--', linewidth = 3, color = (1,1,1), \
                    label = 'Break Even Point')
   
    axs.plot(house.months/12, line2, '-', \
              linewidth = 4, color = clrPts[0], label = 'Unrcv. Cost of Owning')
       
    axs.legend()
    axs.grid('major')
    axs.set_ylabel('Million Dollars')
    axs.set_xlabel('Years') 
    plt.title('Renting v/s Buying')
    axs.set(xlim=( -5, 35 ))
    axs.set(ylim=( -1, 6 ))
