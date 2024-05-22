"""
###############################################################################
Code for estimating House Ownership.
###############################################################################
Created:    Swarnav Banik on Apr 08, 2024
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
CODENAME = 'houseOwncost'

from src.financialTools.incomeTax import incomeTax
from src.financialTools.incomeTax import incomeTax_federal_FY2023
from src.financialTools.investments import investment
from src.frmtFig import frmtFig 
clrPts, mpl, plt = frmtFig(mpl, plt, FS_title = 18, FS_tickLabel = 18, FS_axisLabel = 18)

# %%

class homeOwnership:
    """ Home  Ownership 
    """
    def __init__(self, housePrice, downPay, mortgageRate, mortgageTerm = 30, \
                 propTaxRate = 0.8/100, maintainRate = 1/100, realEstateAppRate = 4.16/100,\
                 invstAppRate = 6.9/100, taxCredits = True, taxStatus = 'married', annualIncome = 400E3):
        self.housePrice         = housePrice
        self.downPay            = downPay
        self.mortgageRate       = mortgageRate
        self.propTaxRate        = propTaxRate
        self.maintainRate       = maintainRate
        self.realEstateAppRate  = realEstateAppRate
        self.mortgageTerm       = mortgageTerm
        if self.downPay/self.housePrice < 0.2:
            print('Downpayment is less than 20%. The bank may require you to pay PMI. This analysis considers PMI = 0.')
        
        # Establish the timeline ##############################################
        self.months  = np.array(range(0, self.mortgageTerm*12+1))
        self.years   = np.array(range(0, self.mortgageTerm+1))
        
        # Estimate the 'cost' of owning #######################################   
        self.getMiscCostPA()
        self.getBankCost() 
        if taxCredits:
            self.getTaxCredit(annualIncome = annualIncome, taxStatus = taxStatus)  
        else:
            self.taxSavings_PM = np.zeros((self.mortgageTerm*12+1,)) 
                
        self.cost_PM = self.cost_PM_prnc + self.cost_PM_debt \
                     + self.cost_PM_pTax + self.cost_PM_main \
                     + np.insert( np.zeros((self.mortgageTerm*12,)) , 0, self.downPay )\
                     - self.taxSavings_PM
        self.cost_CM = self.cost_PM.cumsum()
               
        # Estimate the property and 'equity value' ############################
        self.getValApp()
        self.equity_CM_val = self.equity_CM_frc * self.value_CM
        
        # Estimate the net 'profit' made ######################################        
        self.profit_CM     = self.equity_CM_val - self.cost_CM
       
        # Estimate unrecoverable costs ########################################  
        self.getUnrecoverableCosts(invstAppRate = invstAppRate)
        
    def getMiscCostPA(self):
        self.cost_PM_pTax   = np.insert( (self.propTaxRate/12)*self.housePrice*np.ones((self.mortgageTerm*12,)) , 0, 0 )
        self.cost_PM_main   = np.insert( (self.maintainRate/12)*self.housePrice*np.ones((self.mortgageTerm*12,)), 0, 0 )
        self.cost_CM_pTax  = self.cost_PM_pTax.cumsum()
        self.cost_CM_main  = self.cost_PM_main.cumsum()       
  
        
    def getBankCost(self):        
        cost_PM_bank = (self.housePrice - self.downPay)*(self.mortgageRate/12)\
            /( 1 - ( 1 + (self.mortgageRate/12) )**(-self.mortgageTerm*12) )
            
        self.cost_PM_prnc    = np.zeros((self.mortgageTerm*12+1,))
        self.cost_PM_debt    = np.zeros((self.mortgageTerm*12+1,))
        self.equity_CM_frc   = np.ones((self.mortgageTerm*12+1,))*self.downPay/self.housePrice
        for ii in range(1,self.mortgageTerm*12+1):
            self.cost_PM_debt[ii]   = (self.mortgageRate/12) * \
                (self.housePrice-self.downPay-np.sum(self.cost_PM_prnc[0:ii]))
            self.cost_PM_prnc[ii]   = cost_PM_bank - self.cost_PM_debt[ii]
            self.equity_CM_frc[ii]  = self.equity_CM_frc[ii] + np.sum(self.cost_PM_prnc[0:ii+1])/self.housePrice
        self.cost_CM_debt = self.cost_PM_debt.cumsum()
        self.cost_CM_prnc = self.cost_PM_prnc.cumsum()
        
    def getTaxCredit(self, annualIncome = 400E3, limit = 750E3, taxStatus = 'married'):       
        self.cost_PA_debt  = np.zeros((self.mortgageTerm+1,))
        self.it_deductions = np.zeros((self.mortgageTerm+1,))
        for ii in range(1,self.mortgageTerm+1):
            self.cost_PA_debt[ii]   = np.sum(self.cost_PM_debt[1+(ii-1)*12:1+ii*12])
            self.it_deductions[ii]  = min(self.cost_PA_debt[ii], limit) 
        self.taxSavings_PA       = np.zeros((self.mortgageTerm+1,))
        for ii in range(1,self.mortgageTerm):
            it_noDebt = incomeTax_federal_FY2023(annualIncome, status = taxStatus, addDeductions = 0 ).incomeTax.tax
            it_ysDebt = incomeTax_federal_FY2023(annualIncome, status = taxStatus, addDeductions = self.it_deductions[ii] ).incomeTax.tax
            self.taxSavings_PA[ii+1] = it_noDebt - it_ysDebt        
        self.taxSavings_PM = np.zeros((self.mortgageTerm*12+1,))
        for ii in range(1,self.mortgageTerm+1):
            for jj in range(1+12*(ii-1),1+12*ii):
                self.taxSavings_PM[jj] = min((self.taxSavings_PA[ii] - np.sum(self.taxSavings_PM[1+12*(ii-1):jj])), \
                                             self.cost_PM_prnc[jj]+self.cost_PM_debt[jj])
       
    def getValApp(self):
        self.value_CM = np.ones((self.mortgageTerm*12+1,))*self.housePrice
        for ii in range(self.mortgageTerm*12+1):
            self.value_CM[ii] = self.housePrice * (1+self.realEstateAppRate/12)**ii
        
        
    def getUnrecoverableCosts(self, invstAppRate = 6.9/100):
        self.invstAppRate  = invstAppRate        
        self.hyInvst = investment(self.cost_PM, invstAppRate = invstAppRate/12)
        self.unrecoverCost_CM   = - self.profit_CM + self.hyInvst.profit_CIP

    
      
            
class renting:
    """ Renting
    Parameters
    ----------
    """
    def __init__(self, startRent, rentAppRate = 3.5/100, rentTerm = 30, invstAppRate = 6.9/100):
        self.startRent     = startRent
        self.rentAppRate   = rentAppRate
        self.rentTerm      = rentTerm
        
        self.months   = np.array(range(0, self.rentTerm*12+1))
        self.cost_PM  = np.zeros((self.rentTerm*12+1,))
        for ii in range(1, self.rentTerm*12+1):            
            self.cost_PM[ii] = self.startRent * (1+self.rentAppRate)**(np.floor(ii/12))
        self.cost_CM = self.cost_PM.cumsum()
        self.getUnrecoverableCosts(invstAppRate = invstAppRate)
        
    def getUnrecoverableCosts(self, invstAppRate = 6.9/100):
        self.invstAppRate  = invstAppRate        
        self.hyInvst = investment(self.cost_PM, invstAppRate = invstAppRate/12)
        self.unrecoverCost_CM = self.cost_CM + self.hyInvst.profit_CIP
        
        
class rentVSbuy:
    def __init__(self, housePrice, downPay, startRent, term = 30, \
                 mortgageRate = 7/100, propTaxRate = 0.8/100, maintainRate = 1/100, \
                 realEstateAppRate = 4.16/100, rentAppRate = 3.5/100,\
                 invstAppRate = 6.9/100, taxCredits = True, annualIncome = 400E3 ):
        self.house      = homeOwnership(housePrice, downPay, mortgageRate, mortgageTerm = term, \
                                   propTaxRate = propTaxRate, maintainRate = maintainRate, \
                                   realEstateAppRate = realEstateAppRate, invstAppRate = invstAppRate, \
                                   taxCredits = taxCredits, annualIncome = annualIncome )
        self.house_noTC = homeOwnership(housePrice, downPay, mortgageRate, mortgageTerm = term, \
                                   propTaxRate = propTaxRate, maintainRate = maintainRate, \
                                   realEstateAppRate = realEstateAppRate, invstAppRate = invstAppRate, \
                                   taxCredits = False )
        self.rental     = renting(startRent, rentTerm = term, rentAppRate = rentAppRate, invstAppRate = invstAppRate)
        self.buyLoss    = self.house.unrecoverCost_CM[-1] - self.rental.unrecoverCost_CM[-1]
        
        if self.buyLoss < 0:
            idx = np.argmin(np.abs(self.house.unrecoverCost_CM[12:] - self.rental.unrecoverCost_CM[12:]))
            self.brekEvenPoint = self.rental.months[idx+12]
        elif self.buyLoss == 0:
            self.brekEvenPoint = self.rental.months[-1]
        else:
            self.brekEvenPoint = np.NaN
            
        
        
        
    def plotTermTrend(self, figNo):

        fig = plt.figure(figNo,figsize=(12,1*6))
        gs  = GridSpec(1,1)
        axs = fig.add_subplot(gs[0,0])
        
        line2 = self.house.unrecoverCost_CM*1E-6    
        axs.plot(self.rental.months/12, (self.rental.cost_CM)*1E-6, '--', \
              linewidth = 3, color = clrPts[1], label = 'Cost of Renting')
        axs.plot(self.house.months/12, self.house.cost_CM*1E-6, '--', \
                  linewidth = 3, color = clrPts[0], label = 'Cost of Owning')
        axs.plot(self.rental.months/12, (self.rental.unrecoverCost_CM)*1E-6, '-', \
              linewidth = 4, color = clrPts[1], label = 'Unrcv. Cost of Renting')
        
        axs.plot(self.house.months/12, line2, '-', \
                  linewidth = 4, color = clrPts[0], label = 'Unrcv. Cost of Owning')
        axs.axvline(self.brekEvenPoint/12, ls = '--', linewidth = 3, color = (1,1,1), \
                    label = f'Break Even Point = {self.brekEvenPoint/12:.1f} year')
           
        axs.legend()
        axs.grid('major')
        axs.set_ylabel('Million Dollars')
        axs.set_xlabel('Years') 
        plt.title('Renting v/s Buying')
        axs.set(xlim=( -5, 35 ))
        axs.set(ylim=( -0.1, 7 ))
        
        

        
        

        

        
                
