#!/usr/bin/env python3
"""Synchronize version between pyproject.toml and server.json"""

import json
import re
from pathlib import Path
import sys


def sync_versions():
    try:
        # Read version from pyproject.toml
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        with open(pyproject_path, "r") as f:
            content = f.read()

        # Extract version using regex
        version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        if not version_match:
            print("❌ Could not find version in pyproject.toml")
            return False

        version = version_match.group(1)
        print(f"Found version: {version}")

        # Update server.json
        server_json_path = Path(__file__).parent.parent / "server.json"
        with open(server_json_path, "r") as f:
            server_data = json.load(f)

        server_data["version"] = version

        # Also update package version if packages exist
        if "packages" in server_data:
            for package in server_data["packages"]:
                package["version"] = version

        with open(server_json_path, "w") as f:
            json.dump(server_data, f, indent=2)

        print(f"✅ Synchronized version {version} between pyproject.toml and server.json")
        return True

    except Exception as e:
        print(f"❌ Error synchronizing versions: {e}")
        return False


if __name__ == "__main__":
    success = sync_versions()
    sys.exit(0 if success else 1)
