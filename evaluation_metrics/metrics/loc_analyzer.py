
import os
import pandas as pd
from evaluation_metrics.core.metric_base import MetricBase
from evaluation_metrics.core.registry import register_metric


@register_metric("loc")
class LOCAnalyzer(MetricBase):
    """
    Analyzer for counting lines of code (LOC), ignoring empty lines and comments.
    """

    def __init__(self, config, scanner):
        super().__init__(config, scanner)
        self.output_file = config["metrics"]["loc"]["output"]
        self.languages = config["languages"]
        self.files = config["files"]
        self.results = {}

    def count_code_lines(self, file_path, comment_symbol):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            return sum(1 for line in lines if line.strip() and not line.strip().startswith(comment_symbol))
        except Exception as e:
            print(f" Error reading {file_path}: {e}")
            return 0

    def run(self):
        print("\n Running LOC analysis...")
        scan_results = self.scanner.scan_directories("loc")
        for directory, files in scan_results.items():
            self.results[directory] = {}
            for file, file_path in files.items():
                if not file_path:
                    self.results[directory][file] = 0
                    continue
                language = self._detect_language(file_path)
                if not language:
                    print(f"Warning Skipping unknown extension: {file_path}")
                    self.results[directory][file] = 0
                    continue
                comment_symbol = self.languages[language].get("comment_symbol", "#")
                self.results[directory][file] = self.count_code_lines(file_path, comment_symbol)

    def save_results(self):
        df = pd.DataFrame.from_dict(self.results, orient="index")
        df = df.astype("Int64")
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        df.to_csv(self.output_file, index=True)
        print("-----------------------------------------------------------")
        print(df)
        print("-----------------------------------------------------------")
        print(f"LOC results saved to {self.output_file}\n")
