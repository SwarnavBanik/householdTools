"""
###############################################################################
Code for estimating investment profits.
###############################################################################
Created:    Swarnav Banik on Apr 20, 2024
"""
import logging
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections.abc import Sized
from matplotlib.gridspec import GridSpec
from src.financialTools.incomeTax import incomeTax
from src.financialTools.incomeTax import incomeTax_federal_FY2023
from src.financialTools.incomeTax import incomeTax_CA_FY2023
from src.financialTools.incomeTax import ssTax_FY2023
from src.financialTools.incomeTax import mcTax_FY2023

from src.frmtFig import frmtFig 
clrPts, mpl, plt = frmtFig(mpl, plt, FS_title = 18, FS_tickLabel = 18, FS_axisLabel = 18)

CODENAME = 'investments'
# %% Common Functions #########################################################
def annual2month(annualVal):
    monthVal = np.zeros((len(annualVal)*12+1,))
    for ii in range(len(annualVal)):
        monthVal[ii*12+1:(ii+1)*12+1] = annualVal[ii]/12
    return monthVal

def month2annual(monthVal):
    annualVal = np.zeros((int(len(monthVal)/12),))
    for ii in range(len(annualVal)):
        annualVal[ii] = np.sum(monthVal[ii*12+1:(ii+1)*12+1])
    return annualVal

# %% Single Investment ########################################################
class investment:
    def __init__(self, prnc:np.array, invstAppRate = 6.9/100/12,\
                 liquid = True, volatile = True, name = None):
        self.liquid        = liquid
        self.volatile      = volatile
        self.name          = name
        self.term          = len(prnc) - 1
        self.invstAppRate  = invstAppRate
        self.cost_PIP      = prnc
        self.cost_CIP      = prnc.cumsum()
        self.value_CIP     = np.zeros(np.shape(self.cost_PIP))
        self.value_CIP[0]  = self.cost_PIP[0]
        for ii in range(1, self.term + 1):
            self.value_CIP[ii] = self.value_CIP[ii-1] *(1 + self.invstAppRate) + self.cost_PIP[ii]
        self.profit_CIP    = self.value_CIP - self.cost_CIP
        self.profit_PIP    = np.insert( np.diff(self.profit_CIP), 0, 0)

# %% Portfolio of Investments #################################################
class invstPortfolio:
    def __init__(self, prncs = np.zeros((6,)), inRts = np.array([0, 4.5, 5, 6.9, 5, 6.9])/100, \
                 accountNames = ['Checkings', 'Savings', 'CDs', 'Stocks', 'Treasury', '401K'],\
                 liquid   = [True, True, False, True, False, False],\
                 volatile = [False, False, False, True, False, True],\
                 term_years = 30 ):
        if len(inRts) != len(accountNames) or len(inRts) != len(liquid) or len(inRts) != len(volatile):
            logging.error('investments:invstPortfolio:: lengths of inRts and accountNames are different.')
            return
        else:
            self.noOfAccounts = len(inRts)
        self.term           = term_years*12
        self.months         = np.array(range(self.term+1))
        if np.shape(prncs)[0] != self.noOfAccounts:
            logging.error('investments:invstPortfolio:: prncs needs to be of the same row size as number of accounts.')
            return
       
        self.accounts       = []
        for ii in range(len(accountNames)):
            self.accounts.append(self.setInvstAccount(prncs[ii], inRts[ii], \
                                 liquid[ii], volatile[ii], accountNames[ii]))

        costs_PIP   = np.array([x.cost_PIP for x in self.accounts])
        costs_CIP   = np.array([x.cost_CIP for x in self.accounts])
        values_CIP  = np.array([x.value_CIP for x in self.accounts])
        profits_CIP = np.array([x.profit_CIP for x in self.accounts])
        self.cost_PIP    = np.sum(costs_PIP, axis = 0)
        self.cost_CIP    = np.sum(costs_CIP, axis = 0)
        self.value_CIP   = np.sum(values_CIP, axis = 0)
        self.profit_CIP  = np.sum(profits_CIP, axis = 0)
     
        
    def setInvstAccount(self, prncVal, inRt, liquid, volatile, name):  
        if not isinstance(prncVal, Sized):
            prnc    = np.zeros((self.term+1,))
            prnc[0] = prncVal            
        elif len(prncVal) == 1:
            prnc    = np.zeros((self.term+1,0))
            prnc[0] = prncVal
        elif not len(np.array(prncVal)) == self.term+1:
            logging.error('investments:invstPortfolio::setInvstAccount::: length of prncVal is wrong.')
        else:
            prnc = prncVal

        invstAcct = investment(prnc, invstAppRate = inRt/12, liquid = liquid, \
                               volatile = volatile, name = name)
        return invstAcct
    
    
    def getCondAssets(self, cond = 'volatile'):
        if cond == 'volatile':
            cond  = [x.volatile for x in self.accounts]
        elif cond == 'liquid':
            cond  = [x.liquid for x in self.accounts]
        elif cond == 'liquid and non-volatile':
            cond  = np.logical_and([x.liquid for x in self.accounts],\
                                   [not x.volatile for x in self.accounts])
        else:
            logging.error('investments:invstPortfolio::getCondAssets::: accounts needs to be all or total.')
            return
        true_indices = [index for index, value in enumerate(cond) if value]
        false_indices = [index for index, value in enumerate(cond) if not value]
        tot_cost_true = 0
        tot_cost_false = 0
        tot_value_true = 0
        tot_value_false = 0
        for ii in true_indices:
            tot_cost_true = tot_cost_true + self.accounts[ii].cost_CIP 
            tot_value_true = tot_value_true + self.accounts[ii].value_CIP 
        for ii in false_indices:
            tot_cost_false = tot_cost_false + self.accounts[ii].cost_CIP
            tot_value_false = tot_value_false + self.accounts[ii].value_CIP
        return tot_cost_true, tot_cost_false, tot_value_true, tot_value_false

        
    
    def plotGrowth_value(self, axs, accounts = 'total'):    
        if accounts == 'all':
            for ii in range(self.noOfAccounts):
                axs.plot(self.months/12, self.accounts[ii].value_CIP*1E-6, '-', \
                          linewidth = 4, label = self.accounts[ii].name)
        elif accounts == 'total':
            axs.plot(self.months/12, self.cost_CIP*1E-6, '-', \
                      linewidth = 4, label = 'Cost')
            axs.plot(self.months/12, self.value_CIP*1E-6, '-', \
                      linewidth = 4, label = 'Value')
        elif accounts == 'all-wrt-total':
            for ii in range(0,self.noOfAccounts):
                y = [x.value_CIP for x in self.accounts]
                if ii == 0:
                    baseline = np.zeros(np.shape(self.accounts[ii].value_CIP))
                else:
                    baseline = np.sum(y[:ii], axis = 0)*1E-6
                axs.fill_between(self.months/12, self.accounts[ii].value_CIP*1E-6+baseline, baseline,ls =  '-', \
                          linewidth = 4, label = self.accounts[ii].name)
        elif accounts == 'volatile':
            tot_cost_true, tot_cost_false, tot_value_true, tot_value_false = \
                self.getCondAssets(accounts)
            axs.plot(self.months/12, tot_cost_true*1E-6, '--', color = clrPts[0], linewidth = 4, label = 'Volatile Cost')   
            axs.plot(self.months/12, tot_cost_false*1E-6, '--', color = clrPts[1], linewidth = 4, label = 'Non Voltile Cost')
            axs.plot(self.months/12, tot_value_true*1E-6, '-', color = clrPts[0], linewidth = 4, label = 'Volatile Value')   
            axs.plot(self.months/12, tot_value_false*1E-6, '-', color = clrPts[1], linewidth = 4, label = 'Non Voltile Value')
        elif accounts == 'liquid':
            tot_cost_true, tot_cost_false, tot_value_true, tot_value_false = \
               self.getCondAssets(accounts)
            axs.plot(self.months/12, tot_cost_true*1E-6, '--', color = clrPts[1], linewidth = 4, label = 'Liquid Cost')   
            axs.plot(self.months/12, tot_cost_false*1E-6, '--', color = clrPts[0], linewidth = 4, label = 'Non Liquid Cost')
            axs.plot(self.months/12, tot_value_true*1E-6, '-', color = clrPts[1], linewidth = 4, label = 'Liquid Value')   
            axs.plot(self.months/12, tot_value_false*1E-6, '-', color = clrPts[0], linewidth = 4, label = 'Non Liquid Value')
        elif accounts == 'liquid and non-volatile':
            tot_cost_true, tot_cost_false, tot_value_true, tot_value_false = \
               self.getCondAssets(accounts)
            axs.plot(self.months/12, tot_cost_true*1E-6, '--', color = clrPts[1], linewidth = 4, label = 'Liquid and Non Volatile Cost')   
            axs.plot(self.months/12, tot_cost_false*1E-6, '--', color = clrPts[0], linewidth = 4, label = 'Remaining Cost')
            axs.plot(self.months/12, tot_value_true*1E-6, '-', color = clrPts[1], linewidth = 4, label = 'Liquid and Non Volatile Value')   
            axs.plot(self.months/12, tot_value_false*1E-6, '-', color = clrPts[0], linewidth = 4, label = 'Remaining Value')
        
        
        else:
            logging.error('investments:invstPortfolio::plotGrowth_value::: accounts needs to be all or total.')
            
        axs.legend()
        axs.grid('major')
        axs.set_ylabel('Million Dollars')
        axs.set_xlabel('Years') 
        

# %% Income Allocation ########################################################
class incomeDist:
    def __init__(self, annualIncome, annualExpense = 40E3, \
                 contb401k_self = 17E3, contb401k_empl = 6E3, contb401k_start = 0,\
                 contbTreasury = 10E3, contbTreasury_start = 0, \
                 stocks_splitRatio = 0.25, stocks_start = 0,\
                 cd_splitRatio = 0.25, cd_start = 0,\
                 sav_start = 0, check_start = 0,\
                 inRt = np.array([0, 4.5, 5, 6.9, 5, 6.9])/100, \
                 term_years = 30 ):   
        # Initialize ##########################################################
        if not isinstance(annualIncome, Sized):
            self.annualIncome  = annualIncome * np.ones((term_years,))        
        elif not len(np.array(annualIncome)) == term_years:
            logging.error('investments:incomeDist:: length of annualIncome is wrong.')
        else:
            self.annualExpense  = annualExpense
        if not isinstance(annualExpense, Sized):
            self.annualExpense  = annualExpense * np.ones((term_years,))        
        elif not len(np.array(annualExpense)) == term_years:
            logging.error('investments:incomeDist:: length of annualIncome is wrong.')
        else:
            self.annualExpense  = annualExpense 
        if not isinstance(contb401k_self, Sized):
            contb401k_self  = contb401k_self * np.ones((term_years,))        
        elif not len(np.array(contb401k_self)) == term_years:
            logging.error('investments:incomeDist:: length of annualIncome is wrong.')
        if not isinstance(contb401k_empl, Sized):
            contb401k_empl  = contb401k_empl * np.ones((term_years,))        
        elif not len(np.array(contb401k_empl)) == term_years:
            logging.error('investments:incomeDist:: length of annualIncome is wrong.')
        if not isinstance(contbTreasury, Sized):
            contbTreasury  = contbTreasury * np.ones((term_years,))        
        elif not len(np.array(contbTreasury)) == term_years:
            logging.error('investments:incomeDist:: length of contbTreasury is wrong.')
            
        self.term         = term_years*12
        self.months       = np.array(range(self.term+1))
        self.prnc         = np.zeros((6,self.term+1))
        self.remainder    = annual2month(self.annualIncome)
        
        if not isinstance(stocks_splitRatio, Sized):
            stocks_splitRatio  = stocks_splitRatio * np.ones((self.term+1,))        
        elif not len(np.array(stocks_splitRatio)) == self.term+1:
            logging.error('investments:incomeDist:: length of stocks_splitRatio is wrong.')
        if not isinstance(cd_splitRatio, Sized):
            cd_splitRatio  = cd_splitRatio * np.ones((self.term+1,))        
        elif not len(np.array(cd_splitRatio)) == self.term+1:
            logging.error('investments:incomeDist:: length of cd_splitRatio is wrong.')
        
        
        self.det401contribution(contb401k_start, contb401k_self, contb401k_empl)
        self.deductTaxes()
        self.deductExpenses()
        self.detTreasurycontribution(contbTreasury, contbTreasury_start)
        self.splitIncome(stocks_splitRatio, cd_splitRatio, stocks_start, cd_start, sav_start, check_start)
        self.invest(inRt)
 
       
    def det401contribution(self, contb401k_start, contb401k_self, contb401k_empl, limit_401k = 23E3):
        contb401k      = contb401k_empl + [min(x, limit_401k) for x in contb401k_self]
        self.prnc[5,:] = annual2month(contb401k)
        self.prnc[5,0] = contb401k_start
        self.remainder = self.remainder - annual2month(contb401k_self)
        self.annualDeductions = contb401k - contb401k_empl
        self.income_401k = contb401k_empl
        
    def deductTaxes(self):
        self.annualTax = np.zeros(np.shape(self.annualIncome))
        for ii in range(len(self.annualIncome)):
            annualTax_fed = incomeTax_federal_FY2023(self.annualIncome[ii], status = 'single',\
                                    addDeductions = self.annualDeductions[ii]) 
            annualTax_ca = incomeTax_CA_FY2023(self.annualIncome[ii], status = 'single',\
                                    addDeductions = self.annualDeductions[ii])
            annualTax_ss = ssTax_FY2023(self.annualIncome[ii])
            annualTax_mc = mcTax_FY2023(self.annualIncome[ii])
            self.annualTax[ii] = annualTax_fed.incomeTax.tax + annualTax_ca.incomeTax.tax \
                                + annualTax_ss.tax + annualTax_mc.tax
        self.remainder = self.remainder - annual2month(self.annualTax)  

    def deductExpenses(self):
        self.remainder = self.remainder - annual2month(self.annualExpense)  

    def detTreasurycontribution(self, contbTreasury, contbTreasury_start, limit_treasury = 10E3):
        self.prnc[4,:] = [min(x, limit_treasury/12) for x in annual2month(contbTreasury)]
        self.remainder[1:] = self.remainder[1:] - self.prnc[4,1:]
        self.prnc[4,0] = contbTreasury_start
                
    def splitIncome(self, stocks_splitRatio, cd_splitRatio, stocks_start, cd_start, sav_start, check_start):
        
        if any(stocks_splitRatio + cd_splitRatio > 1):
            logging.error('investments:incomeDist::splitIncome::: split ratios are wrong. lala')
            return
       
        self.prnc[3,:]   = stocks_splitRatio * self.remainder
        self.prnc[2,:]   = cd_splitRatio * self.remainder
        self.remainder[1:]   = self.remainder[1:] - self.prnc[3,1:] - self.prnc[2,1:]
        self.prnc[3,0]   = stocks_start
        self.prnc[2,0]   = cd_start
        self.prnc[1,:]   = self.remainder
        self.prnc[1,0]   = sav_start
        self.remainder   = self.remainder - self.remainder
        self.prnc[0,0]   = check_start
        
    def invest(self, inRt):
        accountNames = ['Checkings', 'Savings', 'CDs', 'Stocks', 'Treasury', '401K']
        liquid       = [True, True, False, True, False, False]
        volatile     = [False, False, False, True, False, True]
        self.portfolio = invstPortfolio(prncs = self.prnc, inRts = inRt, accountNames = accountNames,\
                                            liquid   = liquid, volatile = volatile,\
                                            term_years = int(self.term/12))
        self.annualContributions = np.zeros((6,int(self.term/12)))
        for ii in range(6):
            self.annualContributions[ii] = month2annual(self.portfolio.accounts[ii].cost_PIP)

    def printAnnualIncomeDist(self,figNo):
        fig = plt.figure(figNo,figsize=(12,3*5))
        gs  = GridSpec(3,1)
        axs1 = fig.add_subplot(gs[0,0])
        self.printIncomeAndSaving(axs1)
        axs2 = fig.add_subplot(gs[1:3,0])
        self.printSavingDist(axs2)
        return fig
        
    def printIncomeAndSaving(self, axs, year = 1):
        axs.barh(0,(self.annualIncome[year-1]+self.income_401k[year-1])*1E-3,  height = 0.8, label = 'Income')
        axs.barh(1,self.annualTax[year-1]*1E-3,  height = 0.8, label = 'Tax')
        axs.barh(1,self.annualExpense[year-1]*1E-3,  height = 0.8, left = self.annualTax[year-1]*1E-3, label = 'Expenses')
        axs.barh(2,sum(self.annualContributions[:,year-1])*1E-3,  height = 0.8, label = 'Savings')
        axs.legend()
        axs.set(title = f'Annual Income Distribution: Year# {year:}')
        axs.set_xlabel('Amount (k $)')
        plt.yticks(range(3), ['Income', 'Loss', 'Savings']) 
        axs.grid('major')
        
    def printSavingDist(self, axs, year = 1):
        for ii in range(len(self.portfolio.accounts)):
            axs.bar(ii,self.annualContributions[ii,year-1]*1E-3, width = 0.8, \
                      label = self.portfolio.accounts[ii].name + f' = {self.annualContributions[ii,year-1]*1E-3:.2}')
        plt.xticks(range(len(self.portfolio.accounts)), [x.name for x in self.portfolio.accounts]) 
        axs.grid('major')
        axs.set_ylabel('Amount (k $)')
        
        

    
