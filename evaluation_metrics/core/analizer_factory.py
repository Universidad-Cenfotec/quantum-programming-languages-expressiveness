from evaluation_metrics.core.registry import metric_registry

def create_metric_analyzer(metric_name: str, config: dict, scanner):
    """
    Factory function that instantiates a registered metric analyzer.

    :param metric_name: The name of the metric (e.g., "loc", "halstead").
    :param config: The specific configuration dictionary for the metric.
    :param scanner: The initialized directory scanner instance.
    :return: An instance of the requested metric analyzer.
    :raises ValueError: If the metric is not registered.
    """
    cls = metric_registry.get(metric_name)
    if cls is None:
        raise ValueError(f"Metric '{metric_name}' is not registered.")
    return cls(config, scanner)
