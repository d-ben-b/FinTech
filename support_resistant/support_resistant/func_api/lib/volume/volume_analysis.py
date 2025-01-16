import pprint
import argparse
import sys
from typing import Any, List
from collections import defaultdict
from .cal_dates import cal_Qwd
from lib.TechnicalAnalysisBase.TechnicalAnalysis import TechnicalAnalysisBase
from abc import ABC, abstractmethod


class VolumeAnalysis(ABC,TechnicalAnalysisBase):
    """"
    Abstract base class for detecting and analyzing volume patterns in stock data.
    Subclasses must implement abstract methods for volume detection and analysis.
    Parameter for current number of days :previous_days
    The number of days that a volume band can last:survival_time
    """
    previous_days: float
    survival_time: int

    def __init__(self) -> None:
        """
        Initialize ProtrudingVolumeAnalysis with volume_previous_days and volume_survival_time.
        """
        TechnicalAnalysisBase().__init__()

    def set(self, param, value) -> None:
        """
        Set a parameter's value with validation and overwriie it.
        """
        super().set_check_inputs(param, value)
        if value < 1:
            raise ValueError(
                f"The parameter {param} takes an integer greater than 0.")
        setattr(self, param, value)

    @abstractmethod
    def detect_newvolume(self):
        """
        Detect a new protruding volume date.
        """
        raise NotImplementedError

    @abstractmethod
    def add_newvolume(self):
        """
        Add a new protruding volume to the bar_large_volume dictionary.
        """
        raise NotImplementedError

    @abstractmethod
    def sequential_process(self):
        """
        Output: a dictionary with keys being a tuple (price, date) and values being 
        a list of segment endings. For example,
        the  highest price on previous days is 150 and the lowest price 152 on current day 2021-06-15
        is a newly detected up gap, and its valid state till 2021-07-09;the data entry is recorded as:
        { 
            ("2021-06-14", 152,150): {end_date:"2021-07-09",
                                      state:inactive,
                                      first:"2021-06-21"
                                      second:"2021-07-09"
                                      volume:61300400}
                                      }
        """
        raise NotImplementedError


class ProtrudingVolumeAnalysis(VolumeAnalysis):
    """ 
    Detect volume levels.
    The parameter "volume_previous_days" is a setting that can be specified by the front-end. 
    The parameter "volume_survival_time" is a setting that can be specified by the front-end
    Parameter represents the number of days
    Input: 
        parameters of volume,
        valid days of survival_time
    Returns  the volume analysis results as a dictionary
    """

    volume_previous_days: int
    volume_survival_time: int

    def __init__(self, volume_previous_days, volume_survival_time) -> None:
        self.volume_previous_day = int(volume_previous_days)
        self.volume_survival_time = int(volume_survival_time)
        self.bar_large_volume = defaultdict(list)

    def set(self, param, value) -> None:
        """
        Set a parameter's value with validation.
        """
        super().set_check_inputs(param, value)
        if value < 1:
            raise ValueError(
                f"The parameter {param} takes an integer greater than 0.")
        setattr(self, param, value)

    def detect_newvolume(self, previous_day_interval) -> List:
        """
        Detect a new protruding volume date.
        """
        average = sum(previous_day_interval['volume'][:-1].values)/len(
            previous_day_interval['volume'][:-1].values)

        if previous_day_interval['volume'][-1] > average*1.5:
            return [previous_day_interval.index[-1]]
        else:
            return []

    def add_newvolume(self, detect_newvolume, previous_day_interval):
        """
        Add a new protruding volume to the bar_large_volume dictionary.
        """
        newvolume_value = {'end_date':detect_newvolume[0],'state':'active',
            'volume':previous_day_interval.at[detect_newvolume[0], 'volume'],
            'first':None,'second':None}
        self.bar_large_volume[
            (detect_newvolume[0], previous_day_interval.at[detect_newvolume[0], 'high'],
             previous_day_interval.at[detect_newvolume[0], 'low'])]=newvolume_value
  
    def _find_large_volume(self, previous_day_interval, qwd_date):
        """
        Find new protruding volume patterns in the given stock history and add them to bar_large_volume.
        """
        det_volumedate = self.detect_newvolume(previous_day_interval)
        # add newly detected volume with its level extended to today
        if len(det_volumedate) > 0 and det_volumedate[0] not in qwd_date:
            if len(self.bar_large_volume) == 0:
                self.add_newvolume(det_volumedate, previous_day_interval)
            else:
                self._determine_dominant(
                    det_volumedate, previous_day_interval)

    def _update_state(self, stock_hist_curr):
        """
        Update the state of active protruding volume patterns based on current stock history.
        """
        for pricekey in self.bar_large_volume.keys():
            if self.bar_large_volume[pricekey]['state'] == 'active':
                self.bar_large_volume[pricekey]['end_date'] = stock_hist_curr.index[0]
                if ((self.bar_large_volume[pricekey]['end_date']-pricekey[0]).days 
                    < self.volume_survival_time):
                    # highest price < closing price
                    if (stock_hist_curr['close'][0] > pricekey[1]):
                        high_crossover=['high',stock_hist_curr.index[0]]
                        if self.bar_large_volume[pricekey]['first'] == None:
                            self.bar_large_volume[pricekey]['first']=high_crossover
                        elif 'high' not in self.bar_large_volume[pricekey]['first']:
                            self.bar_large_volume[pricekey]['second']=high_crossover
                            self.bar_large_volume[pricekey]['state']='inactive'
                    # lowest price > closing price
                    elif (stock_hist_curr['close'][0] < pricekey[2]):
                        low_crossover=['low',stock_hist_curr.index[0]]
                        if  self.bar_large_volume[pricekey]['first'] == None:
                            self.bar_large_volume[pricekey]['first']=low_crossover
                        elif 'low' not in self.bar_large_volume[pricekey]['first']:
                            self.bar_large_volume[pricekey]['second']=low_crossover
                            self.bar_large_volume[pricekey]['state']='inactive'
                else:
                    self.bar_large_volume[pricekey]['state'] = 'inactive'

    def _determine_dominant(self, det_newvolunedate, previous_day_interval):
        """
        Determine the dominant protruding volume pattern when a new one is detected.
        """
        old_volume = []
        for pricekey in self.bar_large_volume.keys():
            if self.bar_large_volume[pricekey]['end_date'] == det_newvolunedate[0]:
                old_volume.append(pricekey)
        if len(old_volume) > 0:
            if self.bar_large_volume[old_volume[0]]['volume'] < previous_day_interval['volume'].iloc[-1]:
                self.bar_large_volume[old_volume[0]]['state'] = 'inactive'
                self.add_newvolume(det_newvolunedate, previous_day_interval)
        else:
            self.add_newvolume(det_newvolunedate, previous_day_interval)

    def sequential_process(self, stock_history):
        """
        Perform sequential protruding volume pattern detection and analysis on the entire stock history.
        Returns the volume analysis results as a dictionary
        """
        # calculate Quadruple witching day
        qwd_date = cal_Qwd(stock_history)
        # loop over stock history
        for i in range(self.volume_previous_day+1, len(stock_history)+1):
            if len(self.bar_large_volume) != 0:
                self._update_state(stock_history.iloc[i-1:i])
            # calculate large volume and append to bar_large_volume
            self._find_large_volume(stock_history.iloc[
                i-self.volume_previous_day-1: i], qwd_date)