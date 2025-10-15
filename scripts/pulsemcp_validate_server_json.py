#!/usr/bin/env python3
"""Validate server.json against the MCP registry schema"""

import json
import requests
from jsonschema import validate, ValidationError
import sys
from pathlib import Path


def validate_server_json():
    try:
        # Load server.json
        server_json_path = Path(__file__).parent.parent / "server.json"
        with open(server_json_path, "r") as f:
            server_config = json.load(f)

        # Fetch schema
        schema_url = "https://static.modelcontextprotocol.io/schemas/2025-09-29/server.schema.json"
        response = requests.get(schema_url)
        response.raise_for_status()
        schema = response.json()

        # Validate
        validate(instance=server_config, schema=schema)
        print("✅ server.json is valid according to the MCP registry schema")
        return True

    except ValidationError as e:
        print(f"❌ server.json validation failed: {e.message}")
        if hasattr(e, "absolute_path") and e.absolute_path:
            print(f"   Path: {' -> '.join(str(p) for p in e.absolute_path)}")
        print(f"   Failed value: {e.instance}")
        return False
    except Exception as e:
        print(f"❌ Error validating server.json: {e}")
        return False


if __name__ == "__main__":
    success = validate_server_json()
    sys.exit(0 if success else 1)
