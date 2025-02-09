import os
import yaml
from pathlib import Path
from typing import Dict, Any
from string import Template

def load_yaml(file_path: str) -> Dict[Any, Any]:
    with open(file_path, 'r') as f:
        # Replace environment variables
        template = Template(f.read())
        yaml_str = template.safe_substitute(os.environ)
        return yaml.safe_load(yaml_str)

class Config:
    def __init__(self, config_dir: str = "config"):
        self.base = load_yaml(f"{config_dir}/base.yaml")
        self.models = load_yaml(f"{config_dir}/models.yaml")
        self.experiments = load_yaml(f"{config_dir}/experiments.yaml")
    
    def get_model_config(self, model_id: str) -> Dict[str, Any]:
        return self.models['models'][model_id]
    
    def get_all_experiments(self) -> Dict[str, Any]:
        experiments = {}
        for experiment_id, experiment_config in self.experiments['experiments'].items():
            experiments[experiment_id] = experiment_config
        return experiments
    
    def get_strategy_config(self, strategy_id: str) -> Dict[str, Any]:
        return self.experiments['strategies'][strategy_id]

    def get_experiment_config(self, experiment_id: str) -> Dict[str, Any]:
        exp_config = self.experiments['experiments'][experiment_id]
        strategy = self.experiments['strategies'][exp_config['strategy']]
        
        # Resolve language group if specified
        if isinstance(exp_config['target_languages'], str):
            target_langs = self.experiments['language_groups'][exp_config['target_languages']]
        else:
            target_langs = exp_config['target_languages']
            
        return {
            'base_path': self.base['paths']['base_flores'],
            'source_language': self.base['default_source']['language'],
            'source_code': self.base['default_source']['code'],
            'model': exp_config['model'],
            'temperature': exp_config.get('temperature', strategy['temperature']),
            'num_lines': exp_config['num_lines'],
            'strategy': exp_config['strategy'],
            'target_languages': target_langs,
            'in_file': exp_config['in_file']
        } 

    def get_language_code(self, language: str) -> str:
        """Get the FLORES code for a given language name"""
        code = self.base.get('language_codes', {}).get(language)
        if not code:
            raise ValueError(f"Language code not found for: {language}")
        return code

    def get_all_language_codes(self) -> Dict[str, str]:
        """Get all language codes mapping"""
        return self.base.get('language_codes', {}) 