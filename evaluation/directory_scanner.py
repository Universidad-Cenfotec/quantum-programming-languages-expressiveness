import json
import os
import glob

class DirectoryScanner:
    """Class responsible for scanning directories for various file types."""

    def __init__(self, config_file="config.json"):
        """
        Initializes the scanner and loads configuration settings for a specific metric.
        
        :param config_file: Path to the configuration file.
        :param metric_key: The key in the JSON file that corresponds to the desired metric.
        """
        self.metric_key = ''
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        """Reads configuration from JSON file and returns it."""
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            #print(f"✅ Configuration loaded from {config_file}")
            return config
        except Exception as e:
            print(f"❌ Error loading config file: {e}")
            exit(1)

    def scan_directories(self, metric_key ):
        """
        Scans directories and retrieves files matching the configuration extensions.
        
        :return: A dictionary where keys are directories and values are dictionaries of file names and paths.
        """
        self.metric_key = metric_key
        metric_config = self.config.get(self.metric_key, {})
        files = metric_config.get("files", [])
        directories = metric_config.get("directories", [])
        comment_symbols = metric_config.get("comment_symbols", {})

        results = {}
        print("DIRECTORIES")
        print(directories)
        for directory in directories:
            parent_dir = os.path.basename(directory)
            if not os.path.exists(directory):
                print(f"❌ Skipping non-existing directory: {directory}")
                continue            
            results[parent_dir] = {}
            for file in files:                
                file_found = False                
                for ext in comment_symbols.keys():                    
                    file_paths = glob.glob(os.path.join(directory, "**", f"{file}*{ext}"), recursive=True)
                    if file_paths:
                        results[parent_dir][file] = file_paths[0]
                        #print(f"✅ Found {file_paths[0]}")
                        file_found = True
                        break
                if not file_found:
                    print(f"⚠ No matching file found for {file} in {directory}")
        return results

    def set_metric(self, metric_key):
        self.metric_key = metric_key