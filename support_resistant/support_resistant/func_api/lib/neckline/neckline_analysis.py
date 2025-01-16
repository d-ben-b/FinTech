from typing import Any, List
import pandas as pd
from collections import defaultdict
from lib.TechnicalAnalysisBase.TechnicalAnalysis import ValleysAnalysis,PeaksAnalysis
import pprint


class NecklineAnalysis(ValleysAnalysis, PeaksAnalysis):
    """ 
    Detect valleys and peaks to find best neckline.

    Args: 
        parameters of  valleys and peaks and necklines
        nk_startdate: Extend the initial neckline by up to several days to older trading days.
        nk_enddate:Extend the initial neckline by up to several days to newer trading days.
        nk_initial_interval: Maximum number of days for the initial neckline.
        nk_value_ratio:Filter out the larger ratio.

    Returns:
        the support and resistance analysis results as a dictionary
    """
    valley_left: int
    valley_right: int
    peak_left: int
    peak_right: int
    nk_startdate: int
    nk_enddate: int
    nk_initial_interval: int
    nk_value_ratio: int

    def __init__(self, valley_left, valley_right, peak_left, peak_right, nk_startdate, nk_enddate, nk_initial_interval, nk_value_ratio):
        """
         Initialize with parameters for valleys and peaks
        """
        ValleysAnalysis.__init__(self, valley_left, valley_right)
        PeaksAnalysis.__init__(self, peak_left, peak_right)
        self.neckline = defaultdict(list)
        self.nk_startdate = int(nk_startdate)
        self.nk_enddate = int(nk_enddate)
        self.nk_initial_interval = int(nk_initial_interval)
        self.nk_value_ratio = int(nk_value_ratio)
        self.support_neckline_singal= defaultdict(list)
        self.resistance_neckline_singal= defaultdict(list)

    def _choose_best_line_peak(self,old_points,new_points,new_peak_date,stock_data):
        """
        Selects the best line configuration based on certain conditions between old and new peaks.
        
        Args:
            old_points (list): List of attributes for the old peak.
            new_points (list): List of attributes for the new peak.
            new_peak_date (int): Date of the new peak.
            stock_data (DataFrame): DataFrame containing stock data.

        Returns:
            list: List of the best line configurations that satisfy the conditions.
        """
        best_line=[] #List to store the best line configurations
        # Calculate body bottom values for old and new peaks
        bodybottom_start = max(old_points[2], old_points[3])
        bodybottom_end = max(new_points[2], new_points[3])
        # check the date  between newly peak and old peak is less than self.nk_initial_interval
        # and new valley bodybottom > old valley bodybottom
        if (new_points[0] > old_points[0] and
            ((stock_data.loc[new_points[0]]['X'] -
                stock_data.loc[old_points[0]]['X']) < self.nk_initial_interval)
                and new_points[0] == new_peak_date):
            initial_neckline_stock = stock_data.loc[old_points[0]                                                                        :new_points[0]]
            # define four necklines
            bodybottom_startend = self._line_analysis_peak(
                old_points[1], bodybottom_start, new_points[1], bodybottom_end, initial_neckline_stock)
            bodybottom_start_wiskend = self._line_analysis_peak(
                old_points[1], bodybottom_start, new_points[1], new_points[-2], initial_neckline_stock)
            wiskstart_bodybottomend = self._line_analysis_peak(
                old_points[1], old_points[-2], new_points[1], bodybottom_end, initial_neckline_stock)
            wisk_startend = self._line_analysis_peak(
                old_points[1], old_points[-2], new_points[1], new_points[-2], initial_neckline_stock)
            # calculate the old valleys bodybottom < newly valley bodybottom
            # Check middle points exits
            best_line_all = [
                bodybottom_startend, bodybottom_start_wiskend, wiskstart_bodybottomend, wisk_startend]
            best_line_active = [
                x for x in best_line_all if 'inactive' not in x]
            if len(best_line_active) > 0:
                best_line_active_result = [
                    i for i in best_line_active if i[-1] == min([peak[-1] for peak in best_line_active])]
                best_line_active_result = [
                    [best_line_active_result[0][0], best_line_active_result[0][1]], old_points[0], old_points[1]]
                best_line.append(best_line_active_result)
        return best_line
    
    def _choose_best_line_valley(self,old_points,new_points,new_valley_date,stock_data):
        """
        Selects the best line configuration based on certain conditions between old and new valleys.
        
        Args:
            old_points (list): List of attributes for the old valley.
            new_points (list): List of attributes for the new valley.
            new_valley_date (int): Date of the new valley.
            stock_data (DataFrame): DataFrame containing stock data.

        Returns:
            list: List of the best line configurations that satisfy the conditions.
        """
        best_line=[]#List to store the best line configurations
        # Calculate body bottom values for old and new valleys
        bodybottom_start = max(old_points[2], old_points[3])
        bodybottom_end = max(new_points[2], new_points[3])
        # check the date  between newly valley and old valley is less than self.nk_initial_interval
        # and new valley bodybottom > old valley bodybottom
        bodybottom_start = min(old_points[2], old_points[3])
        bodybottom_end = min(new_points[2], new_points[3])
        # check the date  between newly valley and old valley is less than self.nk_initial_interval
        # and new valley bodybottom > old valley bodybottom
        if (new_points[0] > old_points[0] and
            ((stock_data.loc[new_points[0]]['X'] -
                stock_data.loc[old_points[0]]['X']) < self.nk_initial_interval)
                and new_points[0] == new_valley_date):
            # define four necklines
            initial_neckline_stock = stock_data.loc[old_points[0]                                                                        :new_points[0]]
            bodybottom_startend = self._line_analysis_valley(
                old_points[1], bodybottom_start, new_points[1], bodybottom_end, initial_neckline_stock)
            bodybottom_start_wiskend = self._line_analysis_valley(
                old_points[1], bodybottom_start, new_points[1], new_points[-2], initial_neckline_stock)
            wiskstart_bodybottomend = self._line_analysis_valley(
                old_points[1], old_points[-2], new_points[1], bodybottom_end, initial_neckline_stock)
            wisk_startend = self._line_analysis_valley(
                old_points[1], old_points[-2], new_points[1], new_points[-2], initial_neckline_stock)
            # calculate the old valleys bodybottom < newly valley bodybottom
            # Check middle points exits
            best_line_all = [
                bodybottom_startend, bodybottom_start_wiskend, wiskstart_bodybottomend, wisk_startend]
            best_line_active = [
                x for x in best_line_all if 'inactive' not in x]
            if len(best_line_active) > 0:
                best_line_active_result = [
                    i for i in best_line_active if i[-1] == min([valley[-1] for valley in best_line_active])]
                best_line_active_result = [
                    [best_line_active_result[0][0], best_line_active_result[0][1]], old_points[0], old_points[1]]
                best_line.append(best_line_active_result)
        return best_line
    
    def _add_neckline_peak(self,old_points,new_points,stock_data,best_line):
        """
        Adds a neckline based on the best line configuration between old and new peaks.

        Args:
            old_points (list): List of attributes for the old peak.
            new_points (list): List of attributes for the new peak.
            stock_data (DataFrame): DataFrame containing stock data.
            best_line (list): List of the best line configuration.

        Returns:
            None
        """
        self.neckline[new_points] = {'line': best_line[0][0], 'start_date': {
                                    'date': best_line[0][1], 'xline': best_line[0][-1]},
                                    'end_date': {'date': new_points[0], 'xline': new_points[1]},
                                    'state': {'start': 'active', 'end': 'active'}, 'attribute': 'resistance'}
        self._update_startdates(
            best_line[0], new_points, old_points, stock_data.loc[:best_line[0][1]][-self.nk_startdate-1:-1])
        self._update_enddates(
            new_points, stock_data.iloc[-self.peak_right:])
    def _add_neckline_valley(self,old_points,new_points,stock_data,best_line):
        """
        Adds a neckline based on the best line configuration between old and new valleys.

        Args:
            old_points (list): List of attributes for the old valley.
            new_points (list): List of attributes for the new valley.
            stock_data (DataFrame): DataFrame containing stock data.
            best_line (list): List of the best line configuration.

        Returns:
            None
        """
        self.neckline[new_points] = {'line': best_line[0][0], 'start_date': {
                                'date': best_line[0][1], 'xline': best_line[0][-1]},
                                'end_date': {'date': new_points[0], 'xline': new_points[1]},
                                'state': {'start': 'active', 'end': 'active'}, 'attribute': 'support'}
        self._update_startdates(
            best_line[0], new_points, old_points, stock_data.loc[:best_line[0][1]][-self.nk_startdate-1:-1])
        self._update_enddates(
            new_points, stock_data.iloc[-self.valley_right:])
        
    def _best_line_analysis_valley(self, new_valley_date, stock_data):
        """
        Analyze best lines for valleys.

        Parameters:
        new_valley_date: The date of the new valley.
        stock_data: Historical stock data.

        This method identifies best lines for valleys based on specific criteria.
        """
        best_line = []
        for new_points in self.neckline.keys():
            if new_points[-1] == 'valley':
                for old_points in self.neckline.keys():
                    if self.neckline[new_points] == []:
                        if old_points[-1] == 'valley':
                            best_line=self._choose_best_line_valley(old_points,new_points,new_valley_date,stock_data)
                            if len(best_line) != 0:
                                self._add_neckline_valley(old_points,new_points,stock_data,best_line)

    def _best_line_analysis_peak(self, new_peak_date, stock_data):
        """
        Analyze best lines for peaks.
        This method identifies best lines for peaks based on specific criteria

        Args:
            new_peak_date(list): The date of the new peak.
            stock_data(DataFrame): Historical stock data.

        Returns:
            None
        """
        best_line = []
        for new_points in self.neckline.keys():
            if new_points[-1] == 'peak':
                for old_points in self.neckline.keys():
                    if old_points[-1] == 'peak':
                        if self.neckline[new_points] == []:
                            best_line=self._choose_best_line_peak(old_points,new_points,new_peak_date,stock_data)
                            if len(best_line) != 0:
                                self._add_neckline_peak(old_points,new_points,stock_data,best_line)

    def _line_analysis_valley(self, x2, y2, x1, y1, stock_interval):
        """
        Analyze the valley line.
        This method calculates and analyzes the valley line based on specific criteria

        Args:
            x2, y2: Coordinates of the second point.
            x1, y1: Coordinates of the first point.
            stock_interval: Stock data within the interval.

        Returns:
            list:line function about k1,b1,ratio
        """
        date_interval = stock_interval['X'][-1]-stock_interval['X'][0]
        # Check if y1 is less than y2, which is not a valid valley condition
        if y1 < y2:
            return ['inactive']
        # Check if the ratio exceeds the allowed value
        elif ((y1-y2)/y1)/date_interval > (self.nk_value_ratio /100)/100:
            return ['inactive']
        else:
            ratio = ((y1-y2)/y1)*100
            k1 = (y1 - y2) / (x1 - x2)
            b1 = y2 - k1 * x2
            # Check if the valley line crosses above the open or close prices
            for i in range(0, len(stock_interval)):
                pricekey = k1*stock_interval['X'][i]+b1
                if (pricekey > min(stock_interval['open'][i], stock_interval['close'][i])):
                    return ['inactive']
            # Return the parameters of the valley line
            return [k1, b1, ratio]

    def _line_analysis_peak(self, x2, y2, x1, y1, stock_interval):
        """
        Analyze the peak line.
        This method calculates and analyzes the peak line based on specific criteria.

        Args:
            x2, y2: Coordinates of the second point.
            x1, y1: Coordinates of the first point.
            stock_interval: Stock data within the interval.

        Returns:
            list:line function about k1,b1,ratio
        """
        date_interval = stock_interval['X'][-1]-stock_interval['X'][0]
        # Check if y1 is less than y2, which is not a valid valley condition
        if y1 > y2:
            return ['inactive']
        # Check if the ratio exceeds the allowed value
        elif (-(y1-y2)/y1)/date_interval > (self.nk_value_ratio /100)/100:
            
            return ['inactive']
        else:
            ratio = (-(y1-y2)/y1)*100
            k1 = (y1 - y2) / (x1 - x2)
            b1 = y2 - k1 * x2
            # Check if the valley line crosses above the open or close prices
            for i in range(0, len(stock_interval)):
                pricekey = k1*stock_interval['X'][i]+b1
                if (pricekey < max(stock_interval['open'][i], stock_interval['close'][i])):
                    return ['inactive']
            # Return the parameters of the valley line
            return [k1, b1, ratio]

    def _update_startdates(self, best_line, new_points, old_points, start_stockdata):
        """
        Update the start dates for the neckline based on specific conditions.
        This method updates the start dates of the neckline based on certain criteria

        Args:
            best_line(list): Parameters of the best line.
            new_points(list): Coordinates of the new point.
            old_points(list): Coordinates of the old point.
            start_stockdata(DataFrame): Stock data within the interval.
        
        Returns:
            None
        """
        k1 = best_line[0][0]
        b = best_line[0][1]
        for i in range(len(start_stockdata)-1, -1, -1):
            pricekey = start_stockdata['X'][i]*k1+b
            if (self.neckline[new_points]['state']['start'] == 'active'):
                self.neckline[new_points]['start_date']['date'] = start_stockdata.index[i]
                self.neckline[new_points]['start_date']['xline'] = start_stockdata['X'][i]
                if (old_points[1]-start_stockdata['X'][i] < self.nk_startdate):
                    if (pricekey > start_stockdata['close'][i] and
                            new_points[-1] == 'valley'):
                        self.neckline[new_points]['state']['start'] = 'inactive'
                    elif (pricekey < start_stockdata['close'][i] and
                          new_points[-1] == 'peak'):
                        self.neckline[new_points]['state']['start'] = 'inactive'
                elif old_points[1]-start_stockdata['X'][i] == self.nk_startdate:
                    self.neckline[new_points]['start_date']['date'] = old_points[0]
                    self.neckline[new_points]['start_date']['xline'] = old_points[1]
                    self.neckline[new_points]['state']['start'] = 'inactive'

    def _update_enddates(self, new_points, stock_data):
        """
        Update the end dates for the neckline based on specific conditions.
        This method updates the end dates of the neckline based on certain criteria.

        Args:
            new_points(list): Coordinates of the new point.
            stock_data(DataFrame): Stock data within the interval.
        
        Returns:
            None
        """
        if self.neckline[new_points] != []:
            k1 = self.neckline[new_points]['line'][0]
            b = self.neckline[new_points]['line'][1]
            for i in range(0, len(stock_data)):
                if self.neckline[new_points]['state']['end'] == 'active':
                    self.neckline[new_points]['end_date']['date'] = stock_data.index[i]
                    self.neckline[new_points]['end_date']['xline'] = stock_data['X'][i]
                    if stock_data['X'][-1]-(self.neckline[new_points]['end_date']['xline']) < self.nk_enddate:
                        if (stock_data['X'][i]*k1+b > stock_data['close'][i] and
                                new_points[-1] == 'valley'):
                            self.neckline[new_points]['state']['end'] = 'inactive'
                        elif (stock_data['X'][i]*k1+b < stock_data['close'][i] and
                              new_points[-1] == 'peak'):
                            self.neckline[new_points]['state']['end'] = 'inactive'
                    elif stock_data['X'][-1]-(self.neckline[new_points]['end_date']['xline']) == self.nk_enddate:
                        self.neckline[new_points]['state']['start'] = 'inactive'

    def _update_state_to_tdate(self, stock_history):
        """
        Update the state of the neckline based on specific conditions and 
        update support/resistance signals.

        Args:
            stock_history (DataFrame): Historical stock data.
        
        Returns:
            None
        """
        if len(self.neckline) > 1:
            for pricekey in self.neckline.keys():
                if self.neckline[pricekey] != []:
                    if self.neckline[pricekey]['state']['end'] == 'active':
                        k1 = self.neckline[pricekey]['line'][0]
                        b = self.neckline[pricekey]['line'][1]
                        self.neckline[pricekey]['end_date']['date'] = stock_history.index[-1]
                        self.neckline[pricekey]['end_date']['xline'] = stock_history['X'][-1]
                        if ((stock_history['X'][-1])-(pricekey[1]) < self.nk_enddate):
                            if (pricekey[-1] == 'valley') and (
                                    stock_history['X'][-1]*k1+b > stock_history['close'][-1]):
                                self.support_neckline_singal[stock_history.index[-1]]=stock_history['close'][-1]
                                self.neckline[pricekey]['state']['end'] = 'inactive'
                                for i in self.neckline.keys():
                                    if i[-1] == 'peak' and self.neckline[i] != [] and(
                                    self.neckline[i]['state']['end'] == 'active'):
                                        self.neckline[i]['end_date']['date'] = stock_history.index[-1]
                                        self.neckline[i]['end_date']['xline'] = stock_history['X'][-1]
                                        self.neckline[i]['state']['end'] = 'inactive'
                            elif (pricekey[-1] == 'peak') and (
                                    stock_history['X'][-1]*k1+b < stock_history['close'][-1]):
                                self.resistance_neckline_singal[stock_history.index[-1]]=stock_history['close'][-1]
                                self.neckline[pricekey]['state']['end'] = 'inactive'
                                for j in self.neckline.keys():
                                    if j[-1] == 'valley' and self.neckline[j] != [] and(
                                    self.neckline[j]['state']['end'] == 'active'):
                                        self.neckline[j]['end_date']['date'] = stock_history.index[-1]
                                        self.neckline[j]['end_date']['xline'] = stock_history['X'][-1]
                                        self.neckline[j]['state']['end'] = 'inactive'
                        elif ((stock_history['X'][-1])-(pricekey[1])
                              == self.nk_enddate):
                            self.neckline[pricekey]['end_date']['date'] = pricekey[0]
                            self.neckline[pricekey]['end_date']['xline'] = pricekey[1]
                            self.neckline[pricekey]['state']['end'] = 'inactive'

    def sequential_process(self, stock_history):
        """
        Perform the sequential analysis of the stock history data.
        This method processes the stock history data sequentially, detecting valleys and peaks,
        performing analysis, and updating the state of the neckline and support/resistance signals

        Argss:
            stock_history(DataFrame): Historical stock data.

        Returns:
            the neckline analysis results as a dictionary
        """
        for i in range(2, len(stock_history)):
            # detect new valley
            if i >= self.valley_left+self.valley_right:
                det_valleydate = ValleysAnalysis.detect_newextremum(self,stock_history.iloc[
                    i-self.valley_left-self.valley_right: i+1])
                if len(det_valleydate) > 0:
                    self.neckline[
                        (det_valleydate[0], stock_history.at[det_valleydate[0], 'X'],
                         stock_history.at[det_valleydate[0], 'open'],
                         stock_history.at[det_valleydate[0], 'close'],
                         stock_history.at[det_valleydate[0], 'low'], 'valley')
                    ]
                    if len(self.neckline) > 1:
                        self._best_line_analysis_valley(
                            det_valleydate[0], stock_history[:i+1])
            if i >= self.peak_left+self.peak_right:
                det_peakdate = PeaksAnalysis.detect_newextremum(self,stock_history.iloc[
                    i-self.peak_left-self.peak_right: i+1])
                if len(det_peakdate) > 0:
                    self.neckline[
                        (det_peakdate[0], stock_history.at[det_peakdate[0], 'X'],
                         stock_history.at[det_peakdate[0], 'open'],
                         stock_history.at[det_peakdate[0], 'close'],
                         stock_history.at[det_peakdate[0], 'high'], 'peak')
                    ]
                    if len(self.neckline) > 1:
                        self._best_line_analysis_peak(
                            det_peakdate[0], stock_history[:i+1])
            self._update_state_to_tdate(stock_history[:i+1])


        
