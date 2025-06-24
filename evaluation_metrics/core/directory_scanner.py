import json
import os
import glob

class DirectoryScanner:
    """
    Scans a set of directories for specific files with supported extensions.
    """

    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config file: {e}")
            exit(1)

    def scan_directories(self, metric_key: str):
        """
        Scans directories defined in the global config and matches files by extension.

        :param metric_key: Just passed for compatibility — not used directly anymore.
        :return: dict of {directory_name: {filename: full_path}}
        """
        directories = self.config.get("directories", [])
        files = self.config.get("files", [])
        languages = self.config.get("languages", {})

        extensions = [lang["extension"] for lang in languages.values()]

        results = {}
        print("DIRECTORIES")
        print(directories)

        for directory in directories:
            parent_dir = os.path.basename(directory)
            if not os.path.exists(directory):
                print(f"Error: Skipping non-existing directory: {directory}")
                continue

            results[parent_dir] = {}
            for file_name in files:
                file_found = False
                for ext in extensions:
                    pattern = os.path.join(directory, "**", f"{file_name}*{ext}")
                    file_paths = glob.glob(pattern, recursive=True)
                    if file_paths:
                        results[parent_dir][file_name] = file_paths[0]
                        file_found = True
                        break
                if not file_found:
                    print(f"Warning No matching file found for {file_name} in {directory}")

        return results
