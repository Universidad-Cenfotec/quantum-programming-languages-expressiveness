from utils import Utils as utils
import json
import os
import pandas as pd
from utils import Utils as utils
from directory_scanner import DirectoryScanner

class LinesOfCodeCounter:
    """ Class to count lines of code in multiple files, ignoring comments and empty lines. """

    def __init__(self, scanner: DirectoryScanner, config_file="config.json", metric_key="loc"):
        """
        Initializes the counter with a DirectoryScanner instance and configuration.
        
        :param scanner: Instance of DirectoryScanner to handle file scanning.
        :param config_file: Path to the configuration file.
        :param metric_key: The key in the JSON file that corresponds to the desired metric.
        """
        self.scanner = scanner
        self.config = self.load_config(config_file)
        self.metric_config = self.config.get(metric_key, {})
        self.output_file = self.metric_config.get("output", "")
        self.comment_symbols = self.metric_config.get("comment_symbols", {})
        self.line_counts = {}
        self.metric_key = metric_key

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

    def count_code_lines(self, file_path, comment_symbol):
        """
        Counts lines of code in a file, ignoring empty lines and comments.
        
        :param file_path: Path to the file to analyze.
        :param comment_symbol: Comment symbol for the file type.
        :return: The number of code lines excluding comments and empty lines.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # Count only valid code lines
            code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith(comment_symbol))
            return code_lines
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return 0

    def run(self):
        """
        Runs the analysis by scanning directories and counting code lines.
        """
        print("\n 🚀 Running Line of code analysis...")        
        scan_results = self.scanner.scan_directories(self.metric_key)        
        for parent_dir, files in scan_results.items():
            self.line_counts[parent_dir] = {}
            for file, file_path in files.items():
                if file_path:                    
                    for ext, comment_symbol in self.comment_symbols.items():
                        if file_path.endswith(ext):
                            self.line_counts[parent_dir][file] = self.count_code_lines(file_path, comment_symbol)
                            break
                else:
                    self.line_counts[parent_dir][file] = 0
        self.save_results()
        print("\n 🚀 Ending Running Line of code analysis...")


    def save_results(self):
        """
        Saves the line count results to a CSV file.
        """
        df = pd.DataFrame.from_dict(self.line_counts, orient='index')
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