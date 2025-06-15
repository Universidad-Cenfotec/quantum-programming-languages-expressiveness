from abc import ABC, abstractmethod

class MetricBase(ABC):
    """
    Abstract base class for all metric analyzers.
    All concrete metric classes must inherit from this class and implement its methods.
    """

    def __init__(self, config: dict, scanner):
        """
        Initialize the metric analyzer.

        :param config: Dictionary containing the metric-specific configuration.
        :param scanner: Instance of the directory scanner to be used for locating source files.
        """
        self.config = config
        self.scanner = scanner

    @abstractmethod
    def run(self):
        """
        Execute the main analysis logic for this metric.
        """
        pass

    @abstractmethod
    def save_results(self):
        """
        Save the results of the analysis to a file or database.
        """
        pass
