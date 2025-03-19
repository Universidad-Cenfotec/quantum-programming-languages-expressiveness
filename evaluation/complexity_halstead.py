from utils import Utils as utils
import json
import os
import pandas as pd
from utils import Utils as utils
from directory_scanner import DirectoryScanner

class HalsteadComplexity:
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

    def operands(self, file_path, comment_symbol):
         pass 
    

    def operators(self, file_path, comment_symbol):
         pass 
    
    def volumn(self, df):
        pass

    def run(self):
        """
        Runs the analysis by scanning directories and counting code lines.
        """
        print("\n 🚀 Running halstead...")     
        self.save_results()   
          

    def save_results(self):
        """
        Saves the line count results to a CSV file.
        """
        df = pd.DataFrame.from_dict(self.line_counts, orient='index')
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        df.to_csv(self.output_file, index=True)
        print("-----------------------------------------------------------")
        print(df)
        print("-----------------------------------------------------------")  
        print(f"✅ CSV file successfully saved: {self.output_file} \n\n\n\n ")


    def run_wrapper(self):
        """
        Wrapper method to run the CC analysis.
        """
        original_directory=utils.change_to_father_directory()  
        self.run()
        utils.change_to_directory(original_directory)