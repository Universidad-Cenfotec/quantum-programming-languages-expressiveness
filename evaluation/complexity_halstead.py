from utils import Utils as utils
import json
import os
import re
import pandas as pd
import numpy as np
from collections import Counter
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
        self.operators = self.metric_config.get("operators", {}) 
        self.constraints_key = self.metric_config.get("constraints_key", {})        
        self.metric_key = metric_key
        self.results = []

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

    def extract_operators_operands(self, code, comment_symbol,operators,constraints_key,arithmatic):
        """
        Extracts operators and operands from the code, ignoring lines with comments.
        
        :param code: The source code as a string.
        :param comment_symbol: The symbol used to denote comments in the language.
        :return: A tuple of (operators, operands).
        """
        # Remove lines with comments
        filtered_code = "\n".join(
            line for line in code.splitlines() if not line.strip().startswith(comment_symbol)
        )

        # Compile regex patterns for operators and operands
        constraints_pattern = re.compile(r'\b(' + '|'.join(map(re.escape, constraints_key)) + r')\b')
        operators_pattern = re.compile(r'\b(' + '|'.join(map(re.escape, operators)) + r')\b')
        operands_pattern = re.compile(r'\b([a-zA-Z_][a-zA-Z0-9_]*(_[a-zA-Z0-9_]+)*)\b')
        arithmatic_operators=re.compile(r'(' + '|'.join(map(re.escape, arithmatic)) + r')')
        # Remove operators from the filtered code
        filtered_code = constraints_pattern.sub(' ', filtered_code)

        # Count operators
        operators_n = Counter(operators_pattern.findall(filtered_code))
        filtered_code = operators_pattern.sub(' ', filtered_code)

        # Count operators
        arithmatic_n = Counter(arithmatic_operators.findall(filtered_code))      
        filtered_code = arithmatic_operators.sub(' ', filtered_code)

        operators_n.update(arithmatic_n)
        all_operands = [operand[0] for operand in operands_pattern.findall(filtered_code)]

        # Filter out keywords and operators from operands
        operands_n = Counter(word for word in all_operands if word not in constraints_key and word not in operators)
        #print(operators_n,operands_n)
        print('operators')
        print("\n".join(f"'{key}':'{value}'" for key, value in operators_n.items()))
        print('operands')
        print("\n".join(f"'{key}':'{value}'" for key, value in operands_n.items()), "\n")
        return operators_n, operands_n
    
    def calculate_vocabulary(self, n1, n2):
        """Calculates the vocabulary of the code."""
        return n1 + n2

    def calculate_length(self, N1, N2):
        """Calculates the length of the code."""
        return N1 + N2

    def calculate_volume(self, length, vocabulary):
        return length * (0 if vocabulary == 0 else np.log2(vocabulary))

    def calculate_difficulty(self, n1, n2, N2):
        """Calculates the difficulty of the code."""
        return (n1 / 2) * (N2 / n2 if n2 != 0 else 0)

    def calculate_effort(self, difficulty, volume):
        """Calculates the effort of the code."""
        return difficulty * volume

    def calculate_halstead_metrics(self,file_path, comment_symbol,operators,constraints_key,arithmatic):
        """Calculates Halstead metrics for a specific file."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                code = file.read()
            
            operators, operands = self.extract_operators_operands(code, comment_symbol, operators, constraints_key,arithmatic)
            
            # Append log to a CSV file
            log_data = {
                "File Path": [file_path],
                "Operators": [dict(operators)],
                "Operands": [dict(operands)]
            }
            log_df = pd.DataFrame(log_data)
            log_file = "evaluation/results/halstead_log.csv"
            
            if os.path.exists(log_file):
                existing_log = pd.read_csv(log_file)
                log_df = pd.concat([existing_log, log_df], ignore_index=True)
            
            log_df.to_csv("evaluation/results/halstead_log.csv", index=False)
            # Calculate basic metrics
            n1 = len(operators)  # Number of unique operators
            n2 = len(operands)   # Number of unique operands
            N1 = sum(operators.values())  # Total occurrences of operators
            N2 = sum(operands.values())   # Total occurrences of operands

            # Calculate Halstead metrics using independent functions
            vocabulary = self.calculate_vocabulary(n1, n2)
            length = self.calculate_length(N1, N2)
            volume = self.calculate_volume(length, vocabulary)
            difficulty = self.calculate_difficulty(n1, n2, N2)
            effort = self.calculate_effort(difficulty, volume)

            # Create a DataFrame for the results
            data = {
                "n1 (Unique Operators)": [n1],
                "n2 (Unique Operands)": [n2],
                "N1 (Total Operators)": [N1],
                "N2 (Total Operands)": [N2],
                "Vocabulary": [vocabulary],
                "Length": [length],
                "Volume": [volume],
                "Difficulty": [difficulty],
                "Effort": [effort]
            }
            return pd.DataFrame(data)
        except Exception as e:
            print(f"❌ Error processing file {file_path}: {e}")
            return pd.DataFrame()



    def process_files(self, scan_results):
        """
        Processes files and calculates Halstead metrics for each file.
        
        :param scan_results: Dictionary of directories and their associated files from the scanner.
        """
        print("🔍 Processing files...")
        log_file = "evaluation/results/halstead_log.csv"
        if os.path.exists(log_file):
            os.remove(log_file)
        for directory, files in scan_results.items():
            for file, file_path in files.items():
                if file_path:
                    for ext, comment_symbol in self.comment_symbols.items():
                     if file_path.endswith(ext):
                            # Extract operators and constraints_key
                            operators = self.operators.get(directory, [])
                            constraints_key = self.constraints_key.get(directory, [])
                            arithmatic = self.operators.get("arithmatic", [])
                            first_word = file_path.split('/')[0]
                            if first_word == "hosted" or first_word == "classic": 
                                python_operators = self.operators.get("python", [])
                                operators = python_operators + operators
                            # Calculate Halstead metrics and append to results
                            file_metrics = self.calculate_halstead_metrics(file_path, comment_symbol, operators, constraints_key,arithmatic)
                            if not file_metrics.empty:
                                file_metrics["Directory"] = directory
                                file_metrics["File Name"] = file
                                columns_order = ["Directory", "File Name"] + [col for col in file_metrics.columns if col not in ["Directory", "File Name"]]
                                file_metrics = file_metrics[columns_order]
                                self.results.append(file_metrics)
                            break

                           



    def run(self):
        """
        Runs the Halstead analysis for all files in the specified directories.
        """
        print("\n🚀 Running Halstead analysis...")
        scan_results = self.scanner.scan_directories(self.metric_key)
        self.process_files(scan_results)
        self.save_results()

    def save_results(self):
        """
        Saves the line count results to a CSV file.
        """
        df = pd.concat(self.results, ignore_index=True)
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        df.to_csv(self.output_file, index=True)
        print("-----------------------------------------------------------")
        #print(df)
        print("-----------------------------------------------------------")  
        print(f"✅ CSV file successfully saved: {self.output_file} \n\n\n\n ")


    def run_wrapper(self):
        """
        Wrapper method to run the CC analysis.
        """
        original_directory=utils.change_to_father_directory()  
        self.run()
        utils.change_to_directory(original_directory)