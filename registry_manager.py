#!/usr/bin/env python3
"""
DeveloperOS Central Tool Registry Manager
Utility to inspect, validate, search, and export tool ecosystem metadata.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


class RegistryManager:
    """Manages queries, validation, and exports for DeveloperOS tools registry."""

    def __init__(self, registry_path: Optional[Path] = None):
        if registry_path is None:
            registry_path = Path(__file__).parent / "tools_registry.json"
        self.registry_path = Path(registry_path)
        self.data: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry file not found at {self.registry_path}")
        with open(self.registry_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @property
    def version(self) -> str:
        return self.data.get("version", "unknown")

    @property
    def suites(self) -> List[Dict[str, Any]]:
        return self.data.get("suites", [])

    @property
    def tools(self) -> List[Dict[str, Any]]:
        return self.data.get("tools", [])

    def get_suite(self, suite_id: str) -> Optional[Dict[str, Any]]:
        for suite in self.suites:
            if suite["id"] == suite_id:
                return suite
        return None

    def get_tool(self, tool_id: str) -> Optional[Dict[str, Any]]:
        for tool in self.tools:
            if tool["id"] == tool_id:
                return tool
        return None

    def get_tools_for_suite(self, suite_id: str) -> List[Dict[str, Any]]:
        return [t for t in self.tools if t.get("suite_id") == suite_id]

    def search_tools(self, query: str) -> List[Dict[str, Any]]:
        q = query.lower()
        results = []
        for tool in self.tools:
            match_name = q in tool["name"].lower()
            match_desc = q in tool["description"].lower()
            match_tags = any(q in tag.lower() for tag in tool.get("tags", []))
            if match_name or match_desc or match_tags:
                results.append(tool)
        return results

    def validate_integrity(self) -> List[str]:
        """Validates that suites, tools, and cross-references are sound."""
        errors = []
        suite_ids = {s["id"] for s in self.suites}

        # Check unique suite IDs
        if len(suite_ids) != len(self.suites):
            errors.append("Duplicate suite IDs detected.")

        # Check tools
        tool_ids = set()
        for t in self.tools:
            tid = t.get("id")
            if not tid:
                errors.append("Tool missing required 'id' field.")
                continue
            if tid in tool_ids:
                errors.append(f"Duplicate tool ID: '{tid}'")
            tool_ids.add(tid)

            sid = t.get("suite_id")
            if sid not in suite_ids:
                errors.append(f"Tool '{tid}' references unknown suite_id: '{sid}'")

        return errors


def main() -> int:
    manager = RegistryManager()
    errors = manager.validate_integrity()
    if errors:
        print(f"Registry Validation FAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"DeveloperOS Registry v{manager.version} - Integrity OK")
    print(f"Total Suites Registered: {len(manager.suites)}")
    print(f"Total Tools Cataloged:  {len(manager.tools)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
