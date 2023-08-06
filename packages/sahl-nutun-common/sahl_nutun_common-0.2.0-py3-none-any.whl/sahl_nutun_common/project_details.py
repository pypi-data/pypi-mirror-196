""" Attempt to return project details from pyproject.toml
file either in local directory or 1 dir up
"""

import os, os.path
import sys
import toml


class TomlError(Exception):
    pass


class PyProjectToml:
    def __init__(self, toml_path="pyproject.toml"):
        try:
            # We may be running as a frozen PyInstaller exe, get file from the root
            directory = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
            f = os.path.join(directory, toml_path)
            if not os.path.exists(f):
                f = toml_path
                if not os.path.exists(f):
                    f = f"../{toml_path}"

            with open(f, "r") as fh:
                t = toml.load(f)
            sec = t["tool"]["poetry"]
            self.version = sec.get("version", "Unknown Version")
            self.name = sec.get("name", "Name not known")
            self.description = sec.get("description", "")
            if sec["name"]:
                self.executable_file_name = f"{self.name}_{self.version}"
                self.windows_executable_file_name = f"{self.executable_file_name}.exe"

        except Exception:
            raise TomlError()
