from .core.metrics_controller import MetricsController
from .metrics.loc_analyzer import LOCAnalyzer 
from .metrics.cyclomatic_analyzer import CyclomaticComplexityAnalyzer
from .metrics.halstead_analyzer import HalsteadAnalyzer 

from .metrics.cc_loc_ratio_analyzer import CcLocRatioAnalyzer
from .metrics.effort_loc_ratio_analyzer import EffortLocRatioAnalyzer

def main():
    controller = MetricsController(config_file="evaluation_metrics/config.json")
    selected_metrics = ['loc','ccc', 'halstead','cc_loc_ratio','effort_loc_ratio']
    controller.run_selected_metrics(selected_metrics)

if __name__ == "__main__":
    main()
