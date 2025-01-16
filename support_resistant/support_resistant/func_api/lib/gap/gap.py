import pprint
import argparse
import sys
from typing import Any, List
from collections import defaultdict
from abc import ABC, abstractmethod
from lib.TechnicalAnalysisBase.TechnicalAnalysis import TechnicalAnalysisBase
from datetime import datetime


class GapAnalysis(TechnicalAnalysisBase, ABC):
    """ 
    GapAnalysis is an abstract class, and therefore cannot be instantiated itself. 
    It must be inherited by other classes and its abstract methods implemented.

    Args:
        gap_min_pct : int

    Returns  The gap_results attribute is a dictionary used to store the detected gap results
    """
    gap_results: defaultdict(list)
    def __init__(self) -> None:
        """
        Initialize the GapAnalysis class and its gap_results attribute.
        """
        super().__init__()
        self.gap_results = defaultdict(list)

    def set(self, param, value) -> None:
        """
        Set a parameter's value with validation and overwriie it.
        """
        self.set_check_inputs(param, value)
        if value < 1:
            raise ValueError(
                f"The parameter {param} takes an integer greater than 0.")
        setattr(self, param, value)

    @abstractmethod
    def detect_newgap(self):
        """
        detect a new gap date
        """
        raise NotImplementedError

    @abstractmethod
    def add_newgap(self):
        """
        record a new gap data
        """
        raise NotImplementedError

    @abstractmethod
    def sequential_process(self):
        """
        Output: a dictionary with keys being a tuple (price, date) and values being 
        a list of segment endings. For example,
        up gap:
        the  highest price on previous days is 150 and the lowest price 152 on current day 2021-06-15
        is a newly detected up gap, and its valid state till 2021-07-09;the data entry is recorded as:
        { 
            ("2021-06-14", 152,150): [ 
                ["2021-07-09",'up_gap'],["active"]] 
            ] 
        }

        down gap:
        the  lowest price on previous days is 143 and the highest price 140 on current day 2021-08-15
        is a newly detected up gap, and its valid state till 2021-09-09;the data entry is recorded as:
        { 
            ("2021-08-14", 143,140): [ 
                ["2021-09-09",'down_gap'],["active"]] 
            ] 
        }
        """
        raise NotImplementedError


class UpGapAnalysis(GapAnalysis):
    """
    The parameter "upgap_min_pct" is a setting that can be specified by the front-end. 
    It represents the minimum percentage increase required to identify an "up gap". 
    This parameter allows the user to set a threshold for which gaps should be considered significant and which can be ignored. 
    In other words, if the percentage increase for a gap is below this threshold, it will not be recorded as a significant gap.
    ex: upgap_min_pct=1.2  is 1.2%
    """
    upgap_min_pct: float
    def __init__(self,upgap_min_pct) -> None:
        """
        Initialize UpGapAnalysis with upgap_min_pct.
        """
        super().__init__(upgap_min_pct)
        self.upgap_min_pct = float(upgap_min_pct)

    def detect_newgap(self, stock_hist_2consdays) -> List:
        """
        Detect a new up gap in the given stock history.

        Args:
            stock_hist_2consdays (DataFrame): Historical stock data  on two days for analysis
            
        Returns: 
          the list in two days date
        """
        if ((stock_hist_2consdays['low'][1]-stock_hist_2consdays['high'][0])/stock_hist_2consdays['high'][0]
                > self.upgap_min_pct*0.01):
            return [stock_hist_2consdays.index[0], stock_hist_2consdays.index[1]]
        else:
            return []

    def add_newgap(self, det_update, stock_hist_2consdays) -> None:
        """
        Add a new up gap to the gap_results dictionary.

        Args:
            det_update (list) : the two days date
            stock_hist_2consdays (DataFrame): Historical stock data  on two days for analysis

        Returns:
            None
        """
        newgap = {
            "end_date": det_update[1], 'state': 'active', 'attribute': 'up_gap'}
        self.gap_results[(det_update[0], stock_hist_2consdays.at[det_update[1], 'low'],
                         stock_hist_2consdays.at[det_update[0], 'high'])] = newgap
        
    def sequential_process(self):
        pass


class DownGapAnalysis(GapAnalysis):
    """
    The parameter "downgap_min_pct" is a setting that can be specified by the front-end. 
    It represents the minimum percentage increase required to identify an "down gap". 
    This parameter allows the user to set a threshold for which gaps should be considered significant and which can be ignored. 
    In other words, if the percentage increase for a gap is below this threshold, it will not be recorded as a significant gap.
    ex: downgap_min_pct=1.2  is 1.2%
    """
    downgap_min_pct: float
    def __init__(self, downgap_min_pct) -> None:
        """
        Initialize DownGapAnalysis with downgap_min_pct.
        """
        super().__init__()
        self.downgap_min_pct = float(downgap_min_pct)

    def detect_newgap(self, stock_hist_2consdays) -> List:
        """
        Detect a new down gap in the given stock history.

        Args:
            stock_hist_2consdays (DataFrame): Historical stock data  on two days for analysis
            
        Returns: 
          the list in two days date
        """
        if ((stock_hist_2consdays['low'][0]-stock_hist_2consdays['high'][1]) / stock_hist_2consdays['low'][0]
                > self.downgap_min_pct*0.01):
            return [stock_hist_2consdays.index[0], stock_hist_2consdays.index[1]]
        else:
            return []

    def add_newgap(self, det_update, stock_hist_2consdays)-> None:
        """
        Add a new down gap to the gap_results dictionary.

        Args:
            det_update (list) : the two days date
            stock_hist_2consdays (DataFrame): Historical stock data  on two days for analysis

        Returns:
            None
        """
        newgap_value = {
            "end_date": det_update[1], 'state': 'active', 'attribute': 'down_gap'}
        self.gap_results[(det_update[0], stock_hist_2consdays.at[det_update[0], 'low'],
                         stock_hist_2consdays.at[det_update[1], 'high'])] = newgap_value

    def sequential_process(self):
        pass


class SequentialDetectionGapAnalysis(UpGapAnalysis, DownGapAnalysis):
    """
    Perform sequential gap detection and analysis on stock data.
    Inherits from both UpGapAnalysis and DownGapAnalysis classes.
    Returns the gap analysis results as a dictionary
    """
    def __init__(self,upgap_min_pct,downgap_min_pct) -> None:
        """
        Initialize SequentialDetectionGapAnalysis with upgap_min_pct and downgap_min_pct.
        """
        UpGapAnalysis.__init__(self, upgap_min_pct)
        DownGapAnalysis.__init__(self, downgap_min_pct)

    def _find_gaps(self, stock_hist_2consdays)-> None:
        """
        Find new gaps in the given stock history and add them to gap_results.

        Args:
            stock_hist_2consdays (DataFrame): Historical stock data  on two days for analysis

        Returns:
            None
        """
        detected_update = UpGapAnalysis.detect_newgap(self, stock_hist_2consdays)
        detected_downdate = DownGapAnalysis.detect_newgap(self, stock_hist_2consdays)
        # add newly detected up gap and down gap with its level extended to today
        if len(detected_update) > 0:
            UpGapAnalysis.add_newgap(self, detected_update, stock_hist_2consdays)
        if len(detected_downdate) > 0:
            DownGapAnalysis.add_newgap(self, detected_downdate, stock_hist_2consdays)

    def _update_state(self, stock_hist_curr)-> None:
        """
        Update the state of active gaps based on current stock history.

        Args:
            stock_hist_curr (DataFrame): Historical stock data  on two days for analysis

        Returns:
            None
        """
        for pricekey in self.gap_results.keys():
            if self.gap_results[pricekey]['state'] == 'active':
                self.gap_results[pricekey]['end_date'] = stock_hist_curr.index[0]
                if ((pricekey[2] > stock_hist_curr['close'][0]) and
                        self.gap_results[pricekey]['attribute'] == 'up_gap'):
                    self.gap_results[pricekey]['state'] = 'inactive'
                elif ((pricekey[1] < stock_hist_curr['close'][0]) and
                      self.gap_results[pricekey]['attribute'] == 'down_gap'):
                    self.gap_results[pricekey]['state'] = 'inactive'

    def sequential_process(self, stock_history)-> None:
        """
        Perform sequential gap detection and analysis on the entire stock history.
        Args:
            stock_history (Dataframe): Historical stock data for analysis

        Returns:
            the gap analysis results as a dictionary
        """
        for i in range(1, len(stock_history)):
            # detect new up gap and new down gap
            if len(self.gap_results) != 0:
                self._update_state(stock_history.iloc[i:i+1])
            self._find_gaps(stock_history[i-1:i+1])
        return self.gap_results
