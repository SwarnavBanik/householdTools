"""
###############################################################################
Code for estimating Income Tax.
###############################################################################
Created:    Swarnav Banik on Apr 18, 2024
"""

import numpy as np
import logging
CODENAME = 'incomeTax'

# %%
class incomeTax:
    def __init__(self, income, stdDeductions = 27700, addDeductions = 0,\
                  brackets_bp = np.array([22000, 89450, 190750, 364200, 462500, 693750]),\
                  brackets_pc    = np.array([10, 12, 22, 24, 32, 35, 37]) ):
        self.income         = income
        self.brackets_bp    = brackets_bp
        self.brackets_pc    = brackets_pc 
        self.taxedIncome    = max(self.income - max(stdDeductions, addDeductions),0)
        
        if not self.taxedIncome < brackets_bp[0]:           
            if self.taxedIncome > brackets_bp[-1]:
                idx_last = len(brackets_bp)-1
            else:            
                bool_list = self.taxedIncome/self.brackets_bp < 1
                true_indices = [index for index, value in enumerate(bool_list) if value]
                idx_last     = true_indices[0]-1
            self.tax = self.brackets_bp[0]*self.brackets_pc[0]/100
            for ii in range(1,idx_last+1):
                self.tax = self.tax + (self.brackets_bp[ii]-self.brackets_bp[ii-1])*self.brackets_pc[ii]/100
            self.tax = self.tax + (self.taxedIncome-self.brackets_bp[idx_last])\
                      *self.brackets_pc[idx_last+1]/100
            self.bracketPC = self.brackets_pc[idx_last+1]
        else:
            self.tax = self.taxedIncome*self.brackets_pc[0]/100
            self.bracketPC = self.brackets_pc[0]
      
        self.effTaxRate = self.tax/self.income
        
class ssTax_FY2023:
    def __init__(self, income):
        self.rate     = 6.2/100
        self.maxTax   = 147E3*self.rate
        self.tax      = min(self.rate*income, self.maxTax)
        
class mcTax_FY2023:
    def __init__(self, income):
        self.rate     = 1.45/100
        self.tax      = self.rate*income
    
        
class incomeTax_federal_FY2023:
    def __init__(self, income, status = 'single', addDeductions = 0 ):
        self.income    = income
        self.status    = status
        if status == 'single':
            brackets_bp = np.array([11000, 44725, 95375, 182100, 231250, 578125])
            brackets_pc = np.array([10, 12, 22, 24, 32, 35, 37])
            stdDeductions = 13850
        elif status == 'married':
            brackets_bp = np.array([22000, 89450, 190750, 364200, 462500, 693750])
            brackets_pc    = np.array([10, 12, 22, 24, 32, 35, 37])
            stdDeductions = 27700
        else:
            logging.error('kk')
            
        self.incomeTax = incomeTax(self.income, stdDeductions = stdDeductions, addDeductions = addDeductions,\
                      brackets_bp = brackets_bp, brackets_pc = brackets_pc )
            
class incomeTax_CA_FY2023:
    def __init__(self, income, status = 'single', addDeductions = 0 ):
        self.income    = income
        self.status    = status
        if status == 'single':
            brackets_bp = np.array([10412, 24684, 38959, 54081, 68350, 349137, 418961, 698271, 698272])
            brackets_pc = np.array([1, 2, 4, 6, 8, 9.3, 10.3, 11.3, 12.3])
            stdDeductions = 5363
        elif status == 'married':
            brackets_bp = np.array([20839, 49371, 63644, 78765, 93037, 474824, 569790, 949649])
            brackets_pc = np.array([1, 2, 4, 6, 8, 9.3, 10.3, 11.3, 12.3])
            stdDeductions = 10726
        else:
            logging.error('kk')
            
        self.incomeTax = incomeTax(self.income, stdDeductions = stdDeductions, addDeductions = addDeductions,\
                      brackets_bp = brackets_bp, brackets_pc = brackets_pc )

