import os
import re
import pandas as pd
import numpy as np
from collections import Counter
from evaluation_metrics.core.metric_base import MetricBase
from evaluation_metrics.core.registry import register_metric


@register_metric("halstead")
class HalsteadAnalyzer(MetricBase):
    """
    Analyzer for calculating Halstead complexity metrics.
    """

    def __init__(self, config, scanner):
        super().__init__(config, scanner)
        self.output_file = config["metrics"]["halstead"]["output"]
        self.output_file_log = config["metrics"]["halstead"]["output_log"]
        self.languages = config["languages"]
        self.arithmatic_operators = config.get("operators", {}).get("arithmatic", [])
        self.files = config["files"]
        self.results = []

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

    def extract_operators_operands(self, code, comment_symbol, operators, constraints_key, directory, language):
        filtered_code = "\n".join(
            line for line in code.splitlines() if not line.strip().startswith(comment_symbol)
        )
        constraints_pattern = re.compile(r'\b(' + '|'.join(map(re.escape, constraints_key)) + r')\b')
        filtered_code = constraints_pattern.sub(' ', filtered_code)

        flag = r'\b' if language != "aplf" else ''

        op_pattern = re.compile(f'{flag}(' + '|'.join(map(re.escape, operators)) + f'){flag}')
        op_counts = Counter(op_pattern.findall(filtered_code))
        filtered_code = op_pattern.sub(' ', filtered_code)

        arith_pattern = re.compile('(' + '|'.join(map(re.escape, self.arithmatic_operators)) + ')')
        arith_counts = Counter(arith_pattern.findall(filtered_code))
        filtered_code = arith_pattern.sub(' ', filtered_code)

        op_counts.update(arith_counts)

        operand_pattern = re.compile(r'\b([a-zA-Z_][a-zA-Z0-9_]*(_[a-zA-Z0-9_]+)*)\b')
        operands = [m[0] for m in operand_pattern.findall(filtered_code)]
        operand_counts = Counter(
            word for word in operands if word not in constraints_key and word not in operators
        )

        print(f"\n[DEBUG] File: {language}")
        print("Operators:", dict(op_counts))
        print("Operands:", dict(operand_counts))
        return op_counts, operand_counts


    def calculate_metrics(self, operators, operands):
        n1 = len(operators)
        n2 = len(operands)
        N1 = sum(operators.values())
        N2 = sum(operands.values())

        vocabulary = n1 + n2
        length = N1 + N2
        volume = length * (0 if vocabulary == 0 else np.log2(vocabulary))
        difficulty = (n1 / 2) * (N2 / n2 if n2 != 0 else 0)
        effort = difficulty * volume

        return {
            "n1 (Unique Operators)": n1,
            "n2 (Unique Operands)": n2,
            "N1 (Total Operators)": N1,
            "N2 (Total Operands)": N2,
            "Vocabulary": vocabulary,
            "Length": length,
            "Volume": volume,
            "Difficulty": difficulty,
            "Effort": effort
        }

    def run(self):
        print("\n Running Halstead analysis...")
        scan_results = self.scanner.scan_directories("halstead")
        log_file = self.output_file_log

        if os.path.exists(log_file):
            os.remove(log_file)

        for directory, files in scan_results.items():
            for file, file_path in files.items():
                if not file_path:
                    continue
                language = self._detect_language(file_path)
                if not language:
                    print(f"Warning Skipping file with unknown language: {file_path}")
                    continue
                lang_conf = self.languages[language]
                comment_symbol = lang_conf.get("comment_symbol", "//")
                operators = lang_conf.get("operators", [])
                constraints_key = lang_conf.get("constraints", [])                
                
                hosted_in = lang_conf.get("hosted_in")
                if hosted_in and hosted_in in self.languages:
                    host_conf = self.languages[hosted_in]
                    operators += host_conf.get("operators", [])
                    constraints_key += host_conf.get("constraints", [])
                                    
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        code = f.read()
                    op_counts, operand_counts = self.extract_operators_operands(
                        code, comment_symbol, operators, constraints_key, directory, language
                    )
                    metrics = self.calculate_metrics(op_counts, operand_counts)
                    metrics["Directory"] = directory
                    metrics["File Name"] = file
                    self.results.append(pd.DataFrame([metrics]))

                    # Append log
                    log_data = {
                        "File Path": [file_path],
                        "Operators": [dict(op_counts)],
                        "Operands": [dict(operand_counts)]
                    }
                    log_df = pd.DataFrame(log_data)
                    log_df.to_csv(log_file, mode="a", index=False, header=not os.path.exists(log_file))

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    def save_results(self):
        df = pd.concat(self.results, ignore_index=True)
        column_order = [
            "Directory",
            "File Name",
            "n1 (Unique Operators)",
            "n2 (Unique Operands)",
            "N1 (Total Operators)",
            "N2 (Total Operands)",
            "Vocabulary",
            "Length",
            "Volume",
            "Difficulty",
            "Effort"
        ]
        df = df[column_order]
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        df.to_csv(self.output_file, index=True)
        print("-----------------------------------------------------------")
        print(df)
        print("-----------------------------------------------------------")
        print(f"Halstead metrics saved to {self.output_file}\n")