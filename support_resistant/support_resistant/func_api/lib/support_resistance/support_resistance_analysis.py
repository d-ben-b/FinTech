from typing import Any, List
from collections import defaultdict
import pprint
from lib.TechnicalAnalysisBase.TechnicalAnalysis import ValleysAnalysis,PeaksAnalysis


class SupportResistance(PeaksAnalysis, ValleysAnalysis):
    """ 
    Detect support and resistance levels.

    Args:
        parameters of peaks and valleys
        max number of swaps between support and resistance
        parameter of closeness_threshold :
        Determine if the support lines are too close to each other, 
        or if the resistance lines are too close to each other.

    Returns:
        the support and resistance analysis results as a dictionary
    """
    max_num_supp_resis_swaps: int
    _supp_name = "support"
    _resis_name = "resistance"
    closeness_threshold: int
    def __init__(self, closeness_threshold, peak_left, peak_right, valley_left, valley_right,
                 max_num_supp_resis_swaps,
                 ):
        """
        Initialize SupportResistance with various parameters.
        """
        PeaksAnalysis.__init__(self, peak_left, peak_right)
        ValleysAnalysis.__init__(self, valley_left, valley_right)
        self.supp_resis = defaultdict(list)
        self.closeness_threshold = float(closeness_threshold)*0.01 
        self.max_num_supp_resis_swaps = int(max_num_supp_resis_swaps)
        self.support_firstcrossover=defaultdict(list)
        self.resistance_firstcrossover=defaultdict(list)


    def _add_peak(self, det_peakdate, stock_history) -> None:
        """
        Add a newly detected peak to the supp_resis dictionary.

        Args:
            det_peakdate (list): Detected peak date and information.
            stock_history (DataFrame): Historical stock data for analysis.

        Returns:
            None
        """
        # add newly detected up gap and down gap with its level extended to today
        self.supp_resis[
            (det_peakdate[0], stock_history.at[det_peakdate[0], 'high'])
        ] = [[stock_history.index[-1], self._resis_name], ['active']]

    def _find_Peaks(self, stock_history) -> None:
        """
        Find new peak values in the given stock history and update supp_resis.

        Args:
            stock_history (DataFrame): Historical stock data for analysis.

        Returns:
            None
        """
        det_peakdate = PeaksAnalysis.detect_newextremum(self, stock_history)
        if len(det_peakdate) > 0:
            highest_price = stock_history.at[det_peakdate[0], 'high']
            peak_stock = [det_peakdate[0], highest_price, self._resis_name]
            if len(self.supp_resis) == 0:
                self._add_peak(det_peakdate, stock_history)
            else:
                self._determine_dominants(peak_stock, stock_history)

    def _add_valley(self, det_valleydate, stock_history) -> None:
        """
        Add a newly detected valley to the supp_resis dictionary.
         Find new peak values in the given stock history and update supp_resis.

        Args:
            det_valleydate (list): Detected valley date and information
            stock_history (DataFrame): Historical stock data for analysis.

        Returns:
            None
        """
        self.supp_resis[
            (det_valleydate[0], stock_history.at[det_valleydate[0], 'low'])
        ] = [[stock_history.index[-1], self._supp_name], ['active']]

    def _find_Valleys(self, stock_history) -> None:
        """
        Find new valley values in the given stock history and update supp_resis.

        Args:
            stock_history (DataFrame): Historical stock data for analysis.

        Returns:
            None
        """
        det_valleydate = ValleysAnalysis.detect_newextremum(
            self, stock_history)
        if len(det_valleydate) > 0:
            lowest_price = stock_history.at[det_valleydate[0], 'low']
            valley_stock = [det_valleydate[0], lowest_price, self._supp_name]
            if len(self.supp_resis) == 0:
                self._add_valley(det_valleydate, stock_history)
            else:
                self._determine_dominants( valley_stock, stock_history)
    
    def _reistance_dominant(self,stock,old_resis,stock_history) -> None:
        """
        determind the old resistance and new resistance exist.

        Args:
            stock (list) : Stock information including date, price, and type
            old_resis (list) : old resistance data
            stock_history (DataFrame): Historical stock data for analysis.

        Returns:
            None
        """
        for number in self.supp_resis.keys():
                if number[1] in old_resis:
                    if len(self.supp_resis[number])==2 :
                        self.supp_resis[number]=[[stock[0],self._resis_name], ['inactive']]
                # swaps to resistance attribute
                    else:
                        self.supp_resis[number][1] = [
                            stock[0], self._resis_name]
                        self.supp_resis[number][2]= ['inactive']
           
        if stock[0] != stock_history.index[-1]:
            self._add_peak([stock[0]], stock_history)
        else:
            self.supp_resis[(stock[0], stock[1])].insert(-1,
            [stock_history.index[0], self._resis_name])

    def _support_dominant(self,stock,old_supp,stock_history) -> None:
        """
        determind the old support and new support  exist.

        Args:
            stock (list) : Stock information including date, price, and type
            old_supp (list) : old support  data
            stock_history (DataFrame): Historical stock data for analysis.

        Returns:
            None
        """
        for number in self.supp_resis.keys():
                if number[1] in old_supp:
                    if len(self.supp_resis[number])==2 :
                        self.supp_resis[number]=[[stock[0],self._supp_name], ['inactive']]
               # swaps to support attribute
                    else:
                        self.supp_resis[number][1] = [
                            stock[0], self._supp_name]
                        self.supp_resis[number][2]= ['inactive']
        if stock[0] != stock_history.index[-1]:
            self._add_valley([stock[0]], stock_history)
        else:
            self.supp_resis[(stock[0], stock[1])].insert(-1,
            [stock_history.index[0], self._supp_name])

    def _update_state_to_date(self, stock_history) -> None:
        """
        Update the state of support and resistance levels up to the current date.

        Args:
            stock_history (DataFrame): Historical stock data for analysis.

        Returns:
            None
        """
        for pricekey in self.supp_resis.keys():
            if self.supp_resis[pricekey][-1] == ['active'] and (
                    self.supp_resis[pricekey][-2][0] != stock_history.index[0]):
                self.supp_resis[pricekey][-2][0] = stock_history.index[0]
                # check breakup
                if ((pricekey[1] < stock_history['close'][0]) and
                        self.supp_resis[pricekey][-2][1] == self._resis_name):
                    # not yet reach max number of segments (i.e., 1 + max_num_supp_resis_swaps)
                    if (len(self.supp_resis[pricekey]) < self.max_num_supp_resis_swaps+2):
                        swaps_support = [pricekey[0],
                                         pricekey[1], self._supp_name]
                        self._determine_dominants(
                             swaps_support, stock_history)
                    elif (len(self.supp_resis[pricekey]) == self.max_num_supp_resis_swaps+2):
                        self.support_firstcrossover[self.supp_resis[pricekey][0][0]]=pricekey[1]
                        self.supp_resis[pricekey][-2][0] = stock_history.index[0]
                        self.supp_resis[pricekey][-1] = ['inactive']
                    # not yet reach max number of segments (i.e., 1 + max_num_supp_resis_swaps)
                # check breakdown
                elif ((pricekey[1] > stock_history['close'][0]) and
                      self.supp_resis[pricekey][-2][1] == self._supp_name):
                    if (len(self.supp_resis[pricekey]) < self.max_num_supp_resis_swaps+2):
                        swaps_resistance = [pricekey[0],
                                            pricekey[1], self._resis_name]
                        self._determine_dominants(
                            swaps_resistance, stock_history)
                    elif(len(self.supp_resis[pricekey]) == self.max_num_supp_resis_swaps+2):
                        self.resistance_firstcrossover[self.supp_resis[pricekey][0][0]]=pricekey[1]
                        self.supp_resis[pricekey][-2][0] = stock_history.index[0]
                        self.supp_resis[pricekey][-1] = ['inactive']

    def _determine_dominants(self, stock, stock_history) -> None:
        """
        Determine dominant support and resistance levels.

        Args:
            stock (list): Stock information including date, price, and type.
            stock_history (DataFrame): Historical stock data for analysis.

        Returns:
            None
        """
        old_resis=[]
        old_supp=[]
        equal_value=[]
        for i in self.supp_resis.keys():
            if (abs(i[1]-stock[1])/i[1] <= self.closeness_threshold and
                    self.supp_resis[i][-1][0]== 'active' ):
                # resistance
                if (stock[-1] == self._resis_name and
                     self.supp_resis[i][-2][1] == self._resis_name):
                    if stock[1]==i[1]:
                        equal_value.append(stock[1])
                    else:
                        old_resis.append( i[1])
                elif (stock[-1] == self._supp_name and
                      self.supp_resis[i][-2][1] == self._resis_name):
                    old_supp.append( i[1])
                # support
                elif (stock[-1] == self._supp_name and
                        self.supp_resis[i][-2][1] == self._supp_name):
                    if stock[1]==i[1]:
                        equal_value.append(stock[1])
                    else:
                        old_supp.append( i[1])
                elif (stock[-1] == self._resis_name and
                        self.supp_resis[i][-2][1] == self._supp_name):
                        old_resis.append( i[1])
        #  new peak or valley does not affect other old peaks or valleys
        if len(old_resis) == 0 and len(old_supp) == 0 and stock[0] != stock_history.index[-1]:
            if stock[-1] == 'resistance':
                self._add_peak([stock[0]], stock_history)
            else:
                self._add_valley([stock[0]], stock_history)
        #  new peak  affect other old peaks 
        elif len(old_resis) != 0 and (old_resis== [stock[-2]]) :
                if self.supp_resis[stock[0], stock[1]][-2][0] == stock_history.index[-1]:
                    if(stock_history.index[-1] - stock[0]).days > self.peak_right:
                            self.supp_resis[stock[0], stock[1]].insert(-1,
                                                                    [stock_history.index[-1], self._resis_name])
                            self.support_firstcrossover[stock_history.index[-1]]=stock[1]
        #  new valley  affect other old valleys 
        elif len(old_supp) != 0 and (old_supp== [stock[-2]]) :
                if self.supp_resis[stock[0], stock[1]][-2][0] == stock_history.index[-1]:
                    if(stock_history.index[-1] - stock[0]).days > self.peak_right:
                            self.supp_resis[stock[0], stock[1]].insert(-1,
                                                                    [stock_history.index[-1], self._supp_name])
                            self.resistance_firstcrossover[stock_history.index[-1]]=stock[1]
        # resistance: newly > previous
        elif (len(old_resis) > 0 and stock[1] > max(old_resis)):
            self._reistance_dominant(stock,old_resis,stock_history)
        # support: newly > previous
        elif (len(old_supp) > 0 and stock[1] < min(old_supp)):
            self._support_dominant(stock,old_supp,stock_history)

    def sequential_process(self, stock_history) -> None:
        """
        Perform sequential analysis of stock history to detect levels.

        Args:
            stock_history (DataFrame): Historical stock data for analysis.

        Returns: a dictionary with keys being a tuple (price, date) and values being 
        a list of segment endings. For example, the price 152 on 2021-06-15  is a 
        newly detected valley, and its support is valid till 2021-07-09, followed by 
        changing to resistance till "2021-08-20"; the data entry is recorded as:
        { 
            ("2021-06-15", 152): [ 
                ["2021-07-09", "support"], 
                ["2021-08-20", "resistance"],['active']
            ] 
        }
        """
        # loop over days starting at the 3rd day
        for i in range(2, len(stock_history)):
            # detect new peak
            if i >= self.peak_left+self.peak_right:
                self._find_Peaks(stock_history.iloc[
                    i-self.peak_left-self.peak_right: i+1])
            # detect new valley
            if i >= self.valley_left+self.valley_right:
                self._find_Valleys(stock_history.iloc[
                    i-self.valley_left-self.valley_right: i+1])
                
            self._update_state_to_date(stock_history.iloc[i:i+1])
