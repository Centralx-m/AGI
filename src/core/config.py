"""
Configuration Manager
=====================

Manages configuration settings for the Unlimited AI Agent.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """Configuration manager for the agent"""
    
    def __init__(self, config_path: str = 'config/settings.yaml'):
        self.config_path = config_path
        self.data = self._load()
    
    def _load(self) -> Dict:
        """Load configuration from file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                        return yaml.safe_load(f) or {}
                    elif self.config_path.endswith('.json'):
                        return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        return {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key (dot notation supported)"""
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value"""
        keys = key.split('.')
        target = self.data
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value
        self._save()
    
    def _save(self) -> None:
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                    yaml.dump(self.data, f, default_flow_style=False)
                elif self.config_path.endswith('.json'):
                    json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_all(self) -> Dict:
        """Get all configuration data"""
        return self.data
