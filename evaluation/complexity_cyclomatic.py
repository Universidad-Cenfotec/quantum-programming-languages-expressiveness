from pathlib import Path
import re
import pandas as pd
import os
from utils import Utils as utils
class CyclomaticComplexityCalculator:
    def __init__(self, scanner, metric_key="ccc"):
        """
        Initialize the complexity calculator with a directory scanner.
        
        :param scanner: An instance of the DirectoryScanner class.
        :param metric_key: The key in the JSON configuration that specifies complexity constructs.
        """
        self.scanner = scanner
        self.metric_key = metric_key
        self.constructs = self.scanner.config.get(self.metric_key, {}).get("constructs", {})
        self.output_file = self.scanner.config.get(self.metric_key, {}).get("output", "")
        self.cc_results = {}

        
    def measure_complexity(self, file_path, language):
        """Measures cyclomatic complexity for a specific file and language, ignoring comments."""
        constructs = self.constructs.get(language, [])        
        comment_symbols = self.scanner.config.get(self.metric_key, {}).get("comment_symbols", {})
        comment_symbol = comment_symbols.get(f".{language}", None)        
        if not constructs:
            print(f"❌ No constructs defined for language: {language}")
            return 0
        complexity = 1
        table_data = [] 
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                directory_name = Path(file_path).parent.name
                file_name = Path(file_path).stem
                for line in f:
                    line = line.strip()             
                    if comment_symbol and line.startswith(comment_symbol):
                        continue  
                    #for construct in constructs:
                    #    if re.search(r"\b" + re.escape(construct) + r"\b", line):
                    #        table_data.append([directory_name, file_name, construct, line.strip()])
                    #        complexity += 1
                    for construct in constructs:
                        if language == "aplf":
                            matches = re.findall(re.escape(construct), line)                            
                        else:
                            matches = re.findall(r"\b" + re.escape(construct) + r"\b", line)
                        if matches:
                            table_data.append([directory_name, file_name, construct, line.strip()])
                            complexity += len(matches)

                    #for construct in constructs:
                    #    if re.search(re.escape(construct), line):  # Quitamos \b
                    #        table_data.append([directory_name, file_name, construct, line.strip()])
                    #        complexity += 1
            
        except Exception as e:
            print(f"❌ Error reading file {file_path}: {e}")
            return 0        
        return complexity, table_data

    def compute_complexity(self, scan_results):
        """
        Computes complexity for each file in the scan results.
        
        :param scan_results: Dictionary of directories and their associated files from the scanner.
        """
        df = pd.DataFrame(columns=["Language", "Algorithm", "Construct", "Line"])
        for directory, files in scan_results.items():
            self.cc_results[directory] = {}
            for file, file_path in files.items():
                if file_path:
                    for language in self.constructs.keys():
                        if file_path.endswith(f".{language}"):  # Assume language name matches file extension
                            self.cc_results[directory][file], table_data = self.measure_complexity(file_path, language)
                            if table_data:
                                df_new = pd.DataFrame(table_data, columns=["Language", "Algorithm" ,"Construct", "Line"])
                                df = pd.concat([df, df_new], ignore_index=True)                                
                            break
                else:
                    self.cc_results[directory][file] = 0
        #print(df.to_string(index=False))    
        df.to_csv("evaluation/results/cc_log.csv", index=True)      

    def save_results(self):
        """
        Saves the complexity results to a CSV file.
        """
        df = pd.DataFrame.from_dict(self.cc_results, orient='index')
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        df.to_csv(self.output_file, index=True)
        print("\n\n\n -----------------------------------------------------------")
        print(df)
        print("-----------------------------------------------------------")  
        print(f"✅ CSV file successfully saved: {self.output_file}")

    def run(self):
        """
        Runs the process: scan directories, calculate complexity, and save results.
        """
        print("🚀 Starting complexity calculation...")
        scan_results = self.scanner.scan_directories(self.metric_key)
        self.compute_complexity(scan_results)
        self.save_results()
        print("🚀 Complexity calculation finished.")

    def run_wrapper(self):
        """
        Wrapper method to run the CC analysis.
        """
        original_directory=utils.change_to_father_directory()  
        self.run()
        utils.change_to_directory(original_directory)
