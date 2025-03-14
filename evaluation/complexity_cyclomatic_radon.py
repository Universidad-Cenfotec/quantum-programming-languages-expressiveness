import json
import os
import pandas as pd
from radon.complexity import cc_visit
from utils import Utils as utils
from directory_scanner import DirectoryScanner

class CyclomaticComplexityAnalyzer:
    """Class to analyze Cyclomatic Complexity (CC) of Python files."""

    def __init__(self, scanner: DirectoryScanner, config_file="config.json", metric_key="cc"):
        """
        Initializes the analyzer with a DirectoryScanner instance and configuration.
        
        :param scanner: Instance of DirectoryScanner to handle file scanning.
        :param config_file: Path to the configuration file.
        :param metric_key: The key in the JSON file that corresponds to the desired metric.
        """
        self.scanner = scanner
        self.config = self.load_config(config_file)
        self.metric_config = self.config.get(metric_key, {})
        self.output_file = self.metric_config.get("output", "")
        self.cc_results = {}
        self.metric_key =metric_key

    def load_config(self, config_file):
        """Reads configuration from JSON file and returns it."""
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            print(f"✅ Configuration loaded from {config_file}")
            return config
        except Exception as e:
            print(f"❌ Error loading config file: {e}")
            exit(1)

    def measure_cc(self, file_path):
        """
        Measures the Cyclomatic Complexity (CC) of a Python file.
        
        :param file_path: Path to the Python file to analyze.
        :return: The total Cyclomatic Complexity of all functions in the file.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            # Analyze CC using radon
            functions = cc_visit(code)
            print(f"🔍 FUNCTIONS")
            print(file_path)
            print(functions)
            total_cc = sum(func.complexity for func in functions)  # Sum CC of all functions in the file            
            return total_cc
        except Exception as e:
            print(f"❌ Error analyzing CC for {file_path}: {e}")
            return 0

    def run(self):
        """
        Runs the analysis by scanning directories and computing CC values.
        """
        print("\n 🚀 Running Cyclomatic Complexity analysis...")       
        scan_results = self.scanner.scan_directories(self.metric_key)
        for parent_dir, files in scan_results.items():
            self.cc_results[parent_dir] = {}
            for file, file_path in files.items():
                if file_path:
                    self.cc_results[parent_dir][file] = self.measure_cc(file_path)
                else:
                    self.cc_results[parent_dir][file] = 0
        self.save_results()    
        print("\n 🚀 Ending Running Cyclomatic Complexity analysis...")

    def save_results(self):
        """
        Saves the CC analysis results to a CSV file.
        """
        df = pd.DataFrame.from_dict(self.cc_results, orient='index')
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        df.to_csv(self.output_file, index=True)
        print(f"✅ CSV file successfully saved: {self.output_file}")


    def run_wrapper(self):
        """
        Wrapper method to run the CC analysis.
        """
        original_directory=utils.change_to_father_directory()  
        self.run()
        utils.change_to_directory(original_directory)
        