import yaml


class Config:
    def __init__(self) -> None:
        with open("config.yaml", 'r') as f:
            self.config = yaml.safe_load(f)

        self.target = self.config['settings']['target']
        self.log_file = self.config['settings']['log_file']
        self.scan_results_directory = self.config['settings']['scan_results_directory']
        self.base_directory = self.config['settings']['base_directory']
