from typing import Any, List
from abc import ABC, abstractmethod


class TechnicalAnalysisBase(object):
    def __init__(self) -> None:
        pass

    def check_param_exists(self, param) -> None:
        if not hasattr(self, param):
            raise ValueError(
                f"The parameter {param} is not defined in the class.")

    def set_check_inputs(self, param, value) -> None:
        self.check_param_exists(param)
        if (not isinstance(value, type(getattr(self, param)))):
            raise TypeError(
                f"The parameter {param} takes data type {type(getattr(self, param))}."
            )

    def get(self, param) -> Any:
        self.check_param_exists(param)
        return getattr(self, param)


class ExtremumAnalysis(TechnicalAnalysisBase,ABC):
    """
    Abstract base class for detecting and analyzing extremum values (peaks or valleys) in stock data.
    Subclasses must implement abstract methods for extremum detection.

    Args: 
        extremum_left:
            How many days the extreme value (maximum or minimum) 
            within a certain period of time has shifted to the left on the timeline.

        extremum_right:
            How many days the extreme value (maximum or minimum) 
            within a certain period of time has shifted to the right on the timeline 
    """
    extremum_left: int
    extremum_right: int
    def __init__(self):
        """
        Initialize the ExtremumAnalysis class.
        """
        TechnicalAnalysisBase().__init__()

    @abstractmethod
    def detect_newextremum(self):
        """
        Detect a new extremum date. Must be implemented by subclasses.
        """
        raise NotImplementedError


class PeaksAnalysis(ExtremumAnalysis):
    """
    Detecting and analyzing peaks in stock data.

    Args:
        peak_left(int):
            How many days the maximum 
            within a certain period of time has shifted to the left on the timeline.
    
        peak_right(int):
            How many days the maximum 
            within a certain period of time has shifted to the right on the timeline
    Returns:
        None
    """
    peak_left: int
    peak_right: int
    
    def __init__(self, peak_left, peak_right) -> None:
        """
        Initialize PeaksAnalysis with peak_left and peak_right.
        """
        self.peak_left = int(peak_left)
        self.peak_right = int(peak_right)

    def set(self, param, value) -> None:
        """
        Set a parameter's value with validation and overwrite it.
        """
        super().set_check_inputs(param, value)
        if value < 1:
            raise ValueError(
                f"The parameter {param} takes an integer greater than 0.")
        setattr(self, param, value)

    def detect_newextremum(self, stock_history) -> List:
        """
        Detect a new peak date.

        Args:
            stock_history (DataFrame) : Historical stock data
        
        Returns:
            list :detect a peak date
        """
        if (stock_history['high'][self.peak_left] ==
                max(stock_history['high'][0:self.peak_left+self.peak_right+1])):
            return [stock_history.index[self.peak_left]]
        else:
            return []


class ValleysAnalysis(ExtremumAnalysis):
    """
    Detecting and analyzing valleys in stock data

    Args:
        valley_left:
            How many days the minimum 
            within a certain period of time has shifted to the left on the timeline.
        
        valley_right:
            How many days the minimum
            within a certain period of time has shifted to the right on the timeline
    
    Returns:
        None
    """
    valley_left: int
    valley_right: int
    
    def __init__(self, valley_left, valley_right) -> None:
        """
        Initialize ValleysAnalysis with valley_left and valley_right.
        """
        self.valley_left = int(valley_left)
        self.valley_right = int(valley_right)

    def set(self, param, value) -> None:
        """
        Set a parameter's value with validation and overwrite it.
        """
        super().set_check_inputs(param, value)
        if value < 1:
            raise ValueError(
                f"The parameter {param} takes an integer greater than 0.")
        setattr(self, param, value)

    def detect_newextremum(self, stock_history) -> List:
        """
        Detect a new valley date.

        Args:
            stock_history (DataFrame) : Historical stock data
        
        Returns:
            list :detect a valley date
        """
        if (stock_history['low'][self.valley_left] ==
                min(stock_history['low'][0:self.valley_left+self.valley_right+1])):
            return [stock_history.index[self.valley_left]]
        else:
            return []