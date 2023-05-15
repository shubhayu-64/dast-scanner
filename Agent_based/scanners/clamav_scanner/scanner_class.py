from config import Config
import pyclamd
import json
import os


class ClamAVScanner:
    def __init__(self):
        self.clamd = pyclamd.ClamdAgnostic()
        self.base_directory = Config().base_directory
        self.output_file_path = Config().scan_results_directory + \
            "clamav_scan_results.json"
        self.scan_results = {}

    def ping(self):
        # Check if the clamd daemon is alive
        return self.clamd.ping()

    def reload(self):
        # Reload the virus signature database
        return self.clamd.reload()

    def scan_directory(self):
        # Scan the directory
        file_paths = [os.path.join(root, file) for root, _, files in os.walk(
            self.base_directory) for file in files]
        print(file_paths)

        results = self.clamd.multiscan_file(file_paths[0])
        print(results)

        # Add the results to the dictionary
        # for file_path, result in results.items():
        #     if result:
        #         self.scan_results[file_path] = result

    def save_scan_results(self):
        # Save the scan results to a file
        with open(self.output_file_path, 'w') as f:
            json.dump(self.scan_results, f)
