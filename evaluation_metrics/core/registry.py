

metric_registry = {}

def register_metric(name):
    """
    Decorator to register a metric analyzer class under a specific name.
    
    :param name: The unique string identifier for the metric (e.g., "loc", "halstead").
    :return: The class decorator.
    """
    def decorator(cls):
        metric_registry[name] = cls
        return cls
    return decorator
