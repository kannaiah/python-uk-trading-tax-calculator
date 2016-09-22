"""
    Python UK trading tax calculator
    
    Copyright (C) 2015  Robert Carver
    
    You may copy, modify and redistribute this file as allowed in the license agreement 
         but you must retain this header
    
    See README.txt

"""

import numpy as np

from shredIBfiles import get_ib_trades, get_ib_positions
from shredgenericcsv import read_generic_csv
from calculatetax import calculatetax

from tradelist import TradeList
from positions import PositionList
from utils import profit_analyser

def get_all_trades_and_positions():
    """
    You can change this file for your own purposes
    """

    """
    Get trades, from IB trade reports.
    
    To get the file log in to Account manager... Reports.... trade confirmations....
    Save as .html
    
    Reports need to cover the period from when you opened your account
    
    You can only run one year of trade reports at a time, so its a good idea to run them and save them
    
    Here I'm loading reports from two IB accounts
    """
    trades1=get_ib_trades("2012.htm")
    trades2=get_ib_trades("2013.htm")
    trades3=get_ib_trades("2014.htm")
    trades4=get_ib_trades("2015.htm")
    trades5=get_ib_trades("2016.htm")
    trades6=get_ib_trades("2017.htm")

    
    """
    You can also use .csv files to store trades. I'm doing that here to account for positions I 
    transferred to IB
    
    """
    #trades3=read_generic_csv("tradespre2014.csv")
    
    ## Doesn't inherit the type
    #all_trades=TradeList(trades1+trades2+trades3)
    all_trades=TradeList(trades1+trades2+trades3+trades4+trades5+trades6)
    
    """
    Get positions, from IB files. 
    This is optional. However it is wise to cross check trades and positions to make
    sure you haven't missed anything. You should run this with the same finishing date as the trades
    
    To get the file log in to Account manager... Reports.... activity report....
    Save as .html
    """
    ##positions1=get_ib_positions('2017.htm')

    
    """
    You can join together as many of these as you like
    """
    ##all_positions=PositionList(positions1)
    
    return (all_trades, None)

if __name__=="__main__":
    
    
    ### Get trades and positions
    (all_trades, all_positions)=get_all_trades_and_positions()
    
    
    """
    Create a big report
    
    reportfile is where we output. If omitted, prints to screen.
    
        reportinglevel - ANNUAL - summary for each year, BRIEF- plus one line per closing trade, 
                   NORMAL - plus matching details per trade, CALCULATE - as normal plus calculations  
                   VERBOSE - as calculate plus full breakdown of sub-trades used for matching
    
    
    fx source can be: 'FIXED' uses fixed rates for whole year, 'QUANDL' downloads rates from www.quandl.com
      'DATABASE' this is my function for accessing my own database. It won't work for you, need to roll your own
    
    """

    ### Decide if we're calculating on a CGT or a 'true cost' basis
    CGTCalc=True

    
    taxcalc_dict=calculatetax(all_trades, all_positions, CGTCalc=CGTCalc, reportfile="TaxReport.txt",
                              reportinglevel="VERBOSE", fxsource="QUANDL") #DATABASE

    
    
    ## Example of how we can delve into the finer details. This stuff is all printed to screen
    ## You can also run this interactively
    ## CGTCalc needs to match, or it wont' make sense
    
    taxcalc_dict.display_taxes(taxyear=2012, CGTCalc=CGTCalc, reportinglevel="ANNUAL")
    taxcalc_dict.display_taxes(taxyear=2013, CGTCalc=CGTCalc, reportinglevel="ANNUAL")
    taxcalc_dict.display_taxes(taxyear=2014, CGTCalc=CGTCalc, reportinglevel="ANNUAL")
    taxcalc_dict.display_taxes(taxyear=2015, CGTCalc=CGTCalc, reportinglevel="ANNUAL")
    taxcalc_dict.display_taxes(taxyear=2016, CGTCalc=CGTCalc, reportinglevel="ANNUAL")
    
    ## Display all the trades for one code ('element')SSYSn
    ##  print 'Trades for SHLD 21JAN12 30.0 P'
    ## taxcalc_dict['SHLD 21JAN12 30.0 P'].display_taxes_for_code(taxyear=2012, CGTCalc=CGTCalc, reportinglevel="CALCULATE")

    
    ## Display a particular trade. The number '3' is as shown the report
    #taxcalc_dict['FBTP DEC 14'].matched[3].group_display_taxes(taxyear=2015, CGTCalc=CGTCalc, reportinglevel="VERBOSE")

    ## Heres a cool trade
    #taxcalc_dict['FGBS DEC 14'].element_display_taxes(taxyear=2015, CGTCalc=CGTCalc, reportinglevel="NORMAL")
    #taxcalc_dict['FGBS DEC 14'].matched[17].group_display_taxes(taxyear=2015, CGTCalc=CGTCalc, reportinglevel="VERBOSE")


    ## Bonus feature - analyse profits
    profits=taxcalc_dict.return_profits(2014, CGTCalc)
    profit_analyser(profits)

    avgcomm=taxcalc_dict.average_commission(2014)
    print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    print 'Codes: '
    codes=avgcomm.keys()
    codes.sort()
    print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    for code in codes:
        print "%s %f" % (code, avgcomm[code])
        
    print "Avg comm: ", np.nanmean(avgcomm.values())
    print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    print 'List of unmatched trades'
    for code in codes:
        if len(taxcalc_dict[code].unmatched)>0:
            print code
            print taxcalc_dict[code]
    print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'