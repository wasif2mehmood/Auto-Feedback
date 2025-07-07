import json
import yaml
import pandas as pd
from pathlib import Path

class ConfigLoader:
    """Handles loading of configuration and data files"""
    
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from JSON file"""
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def load_criteria(self):
        """Load criteria from YAML file"""
        with open(self.config["criteria_path"], 'r') as f:
            return yaml.safe_load(f)
    
    def load_scores(self):
        """Load scores from CSV file"""
        return pd.read_csv(self.config["score_path"])
    
    def get_output_path(self):
        """Get configured output path"""
        return Path(self.config["output_path"])
    
    def get_mode(self):
        """Get configured mode (repo or publication)"""
        return self.config.get("mode", "repo")
    
    def get_target_publications(self):
        """Get target publications from config"""
        return self.config.get("publications", [])
    
    def get_criteria_filter(self):
        """Get criteria filter from config"""
        return self.config.get("criteria", [])