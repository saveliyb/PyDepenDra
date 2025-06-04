import glob
from pathlib import Path
import yaml
from typing import Dict, List, Optional
import logging


class Config:
    def __init__(self, config_path: Optional[str] = None):
        self.ignore_files: List[str] = []
        self.ignore_deps: List[str] = []
        self.include_files: List[str] = []

        if config_path is None:
            config_path = self._find_config()

        if config_path:
            self._load_config(config_path)

    def _find_config(self) -> Optional[str]:
        """
        Searches for pydependra.yaml configuration file in the current working directory and its subdirectories.

        Returns:
            Optional[str]: Path to the found config file or None if not found.
        """
        for path in Path.cwd().rglob("pydependra.y*ml"):
            return str(path)
        return None

    def _load_config(self, config_path: str) -> None:
        """
        Loads configuration from the specified YAML file.

        Args:
            config_path (str): Path to the configuration file.
        """
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

        logging.debug(f"Loaded config: {config}")
        self.ignore_files = config.get("ignore", {}).get("files", [])
        logging.debug(f"Ignore files: {self.ignore_files}")
        self.ignore_deps = config.get("ignore", {}).get("dependencies", [])

    def is_ignored(self, file_path: str) -> bool:
        """
        Checks whether the specified file should be ignored based on configuration patterns.

        Args:
            file_path (str): Path to the file to check.

        Returns:
            bool: True if the file should be ignored, False otherwise.
        """
        path = Path(file_path).resolve()
        cwd = Path.cwd().resolve()

        try:
            rel_path = path.relative_to(cwd)
        except ValueError:
            rel_path = path

        rel_path_str = str(rel_path).replace("\\", "/").lower()

        logging.debug(f"Checking ignore for file: {rel_path_str}")
        for pattern in self.ignore_files:
            norm_pattern = pattern.replace("\\", "/").lower()
            logging.debug(f"Matching against pattern: {norm_pattern}")
            if glob.fnmatch.fnmatch(rel_path_str, norm_pattern):
                logging.debug(f"[IGNORED] {rel_path_str} matched pattern {norm_pattern}")
                return True

        logging.debug(f"[NOT IGNORED] {rel_path_str} did not match any pattern")
        return False
