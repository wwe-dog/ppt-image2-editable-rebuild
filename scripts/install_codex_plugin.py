#!/usr/bin/env python3
"""Install this repository as a local Codex plugin for slash-command support."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


PLUGIN_NAME = "ppt-image2-editable-rebuild"


def copy_plugin_repo(source_root: Path, plugin_root: Path) -> None:
    if plugin_root.exists():
        shutil.rmtree(plugin_root)

    def ignore(_dir: str, names: list[str]) -> set[str]:
        ignored = {".git", "__pycache__", ".pytest_cache"}
        return {name for name in names if name in ignored or name.endswith(".pyc")}

    shutil.copytree(source_root, plugin_root, ignore=ignore)


def update_marketplace(marketplace_path: Path) -> None:
    marketplace_path.parent.mkdir(parents=True, exist_ok=True)
    if marketplace_path.exists():
        data = json.loads(marketplace_path.read_text(encoding="utf-8"))
    else:
        data = {
            "name": "personal",
            "interface": {"displayName": "Personal"},
            "plugins": [],
        }

    plugins = data.setdefault("plugins", [])
    entry = {
        "name": PLUGIN_NAME,
        "source": {
            "source": "local",
            "path": f"./plugins/{PLUGIN_NAME}",
        },
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": "Productivity",
    }

    for index, plugin in enumerate(plugins):
        if plugin.get("name") == PLUGIN_NAME:
            plugins[index] = entry
            break
    else:
        plugins.append(entry)

    marketplace_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    source_root = Path(__file__).resolve().parents[1]
    home = Path.home()
    plugin_root = home / "plugins" / PLUGIN_NAME
    marketplace_path = home / ".agents" / "plugins" / "marketplace.json"

    copy_plugin_repo(source_root, plugin_root)
    update_marketplace(marketplace_path)

    print(f"Installed local plugin source: {plugin_root}")
    print(f"Updated personal marketplace: {marketplace_path}")
    print()
    print("Next steps:")
    print(f"1. codex plugin add {PLUGIN_NAME}@personal")
    print("2. Restart Codex or open a new thread.")
    print(f"3. Use /{PLUGIN_NAME} from the slash command list.")


if __name__ == "__main__":
    main()
