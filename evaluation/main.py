import json
from complexity_cyclomatic_radon import CyclomaticComplexityAnalyzer
from directory_scanner import DirectoryScanner
from complexity_cyclomatic import CyclomaticComplexityCalculator
from utils import Utils as utils
from complexity_lloc import LinesOfCodeCounter
#from metrics_analysis import MetricsAnalysis

def main():
    config_file = 'config.json'
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    scanner = DirectoryScanner(config_file=config_file)   
    cc_analyzer = CyclomaticComplexityAnalyzer(scanner=scanner, metric_key = "cc")
    loc_analyzer = LinesOfCodeCounter(scanner=scanner, metric_key = "loc")
    cc_calucator = CyclomaticComplexityCalculator(scanner=scanner, metric_key = "ccc")
    loc_analyzer.run_wrapper()
    cc_analyzer.run_wrapper() 
    cc_calucator.run_wrapper()  
    
if __name__ == "__main__":
    main()
