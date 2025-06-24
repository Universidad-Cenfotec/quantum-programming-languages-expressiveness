from abc import ABC, abstractmethod
import os

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

    
    def _detect_language(self, file_path):
        file_path_lower = file_path.lower()
        for lang_key, lang_conf in self.languages.items():
            ext = lang_conf["extension"]
            if file_path.endswith(ext) and lang_key in file_path_lower:
                return lang_key

        for lang_key, lang_conf in self.languages.items():
            if file_path.endswith(lang_conf["extension"]):
                return lang_key

        return None
