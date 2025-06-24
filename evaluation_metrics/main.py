from .core.metrics_controller import MetricsController
from .metrics.loc_analyzer import LOCAnalyzer 
from .metrics.cyclomatic_analyzer import CyclomaticComplexityAnalyzer
from .metrics.halstead_analyzer import HalsteadAnalyzer 


def main():
    controller = MetricsController(config_file="evaluation_metrics/config.json")
    selected_metrics = ['loc','ccc', 'halstead']
    controller.run_selected_metrics(selected_metrics)

if __name__ == "__main__":
    main()
