import os
import re
import pandas as pd
from pathlib import Path
from evaluation_metrics.core.metric_base import MetricBase
from evaluation_metrics.core.registry import register_metric

@register_metric("ccc")
class CyclomaticComplexityAnalyzer(MetricBase):
    """
    Analyzer for computing Cyclomatic Complexity for supported languages.
    """

    def __init__(self, config, scanner):
        super().__init__(config, scanner)
        self.output_file = config["metrics"]["ccc"]["output"]
        self.output_file_log = config["metrics"]["ccc"]["output_log"]
        self.languages = config["languages"]
        self.files = config["files"]
        self.results = {}

    def measure_complexity(self, file_path, language):
        constructs = self.languages[language].get("constructs", [])
        comment_symbol = self.languages[language].get("comment_symbol", None)
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
                    for construct in constructs:
                        if language == "aplf":
                            matches = re.findall(re.escape(construct), line)
                        else:
                            matches = re.findall(r"\b" + re.escape(construct) + r"\b", line)
                        if matches:
                            table_data.append([directory_name, file_name, construct, line.strip()])
                            complexity += len(matches)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return 0, []

        return complexity, table_data

    def run(self):
        print("\n Running Cyclomatic Complexity analysis...")
        scan_results = self.scanner.scan_directories("ccc")
        df_log = pd.DataFrame(columns=["Language", "Algorithm", "Construct", "Line"])
        for directory, files in scan_results.items():
            self.results[directory] = {}
            for file, file_path in files.items():
                if not file_path:
                    self.results[directory][file] = 0
                    continue
                language = self._detect_language(file_path)
                if not language:
                    print(f"Warning: Skipping unrecognized file type: {file_path}")
                    continue
                complexity, table_data = self.measure_complexity(file_path, language)
                self.results[directory][file] = complexity
                if table_data:
                    df_new = pd.DataFrame(table_data, columns=["Language", "Algorithm", "Construct", "Line"])
                    df_log = pd.concat([df_log, df_new], ignore_index=True)        
        df_log.to_csv(self.output_file_log, index=False)

    def save_results(self):
        df = pd.DataFrame.from_dict(self.results, orient="index")
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        df = df.astype("Int64")
        df.to_csv(self.output_file, index=True)
        print("-----------------------------------------------------------")
        print(df)
        print("-----------------------------------------------------------")
        print(f"Cyclomatic Complexity saved to {self.output_file}\n")
