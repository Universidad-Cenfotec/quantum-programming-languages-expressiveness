import json
from evaluation_metrics.core.directory_scanner import DirectoryScanner
from evaluation_metrics.core.analizer_factory import create_metric_analyzer

class MetricsController:
    """
    Central controller that manages the execution of all metric analyzers.
    """

    def __init__(self, config_file: str):
        """
        Initialize the controller by loading configuration and setting up the scanner.

        :param config_file: Path to the JSON configuration file.
        """
        self.config_file = config_file
        self.config = self._load_config(config_file)
        self.scanner = DirectoryScanner(config_file=config_file)

    def _load_config(self, path: str) -> dict:
        """
        Load the configuration from a JSON file.

        :param path: Path to the configuration file.
        :return: Configuration dictionary.
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"ERROR: Failed to load config: {e}")
            return {}

    def run_selected_metrics(self, selected_metrics: list[str]):
        """
        Execute the selected metric analyzers.

        :param selected_metrics: List of metric names to run (e.g., ["loc", "ccc", "halstead"]).
        """
        for metric_name in selected_metrics:
            if metric_name not in self.config["metrics"]:
                print(f"No configuration found for metric '{metric_name}'. Skipping.")
                continue

            try:
                analyzer = create_metric_analyzer(metric_name, self.config, self.scanner)
                print(f"\n=== Running metric: {metric_name} ===")
                analyzer.run()
                analyzer.save_results()
            except Exception as e:
                print(f"Failed to run metric '{metric_name}': {e}")
