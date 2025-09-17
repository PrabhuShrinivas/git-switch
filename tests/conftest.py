import os
import sys
import json
from pathlib import Path
from typing import Dict, Tuple, Callable, List, Optional

# Ensure 'src' is importable before tests import package modules
_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import pytest


@pytest.fixture()
def tmp_home(tmp_path, monkeypatch):
    home = tmp_path / "home"
    (home / ".config").mkdir(parents=True, exist_ok=True)
    (home / ".ssh").mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("HOME", str(home))
    # Some libraries also read USERPROFILE on Windows; harmless on *nix
    monkeypatch.setenv("USERPROFILE", str(home))
    return home


@pytest.fixture()
def isolate_paths(tmp_home, monkeypatch):
    """Patch git_switch.ssh_manager to use a temporary HOME and derived paths."""
    import importlib
    from git_switch import ssh_manager as sm

    # Repoint module-level path constants to the tmp HOME
    home = tmp_home
    config_dir = home / ".config" / "git-switch"
    ssh_dir = home / ".ssh"
    managed_dir = ssh_dir / "git-switch"
    include_file = ssh_dir / "git-switch-managed.conf"
    ssh_config_file = ssh_dir / "config"
    profiles_file = config_dir / "profiles.json"

    monkeypatch.setattr(sm, "HOME_DIR", home, raising=False)
    monkeypatch.setattr(sm, "CONFIG_DIR", config_dir, raising=False)
    monkeypatch.setattr(sm, "SSH_DIR", ssh_dir, raising=False)
    monkeypatch.setattr(sm, "MANAGED_DIR", managed_dir, raising=False)
    monkeypatch.setattr(sm, "INCLUDE_FILE", include_file, raising=False)
    monkeypatch.setattr(sm, "SSH_CONFIG_FILE", ssh_config_file, raising=False)
    monkeypatch.setattr(sm, "PROFILES_FILE", profiles_file, raising=False)

    # Ensure fresh directories exist
    config_dir.mkdir(parents=True, exist_ok=True)
    ssh_dir.mkdir(parents=True, exist_ok=True)
    managed_dir.mkdir(parents=True, exist_ok=True)

    # Return the patched module for convenience
    return sm


@pytest.fixture()
def write_state(isolate_paths) -> Callable[[Dict[str, dict], Optional[str]], None]:
    sm = isolate_paths

    def _write(profiles: Dict[str, dict], active: Optional[str]) -> None:
        data = {"profiles": profiles, "active_profile": active}
        sm.PROFILES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(sm.PROFILES_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)

    return _write


class SubprocessRecorder:
    def __init__(self):
        self.calls: List[Tuple[List[str], dict]] = []

    def __call__(self, args, **kwargs):
        # Record call
        cmd = list(args)
        self.calls.append((cmd, kwargs))

        # Simulate exit codes across git and clipboard usages
        # Return object with .stdout/.stderr attributes similar to subprocess.CompletedProcess
        class Result:
            def __init__(self):
                self.stdout = b""
                self.stderr = b""

        return Result()


@pytest.fixture()
def record_subprocess(monkeypatch):
    rec = SubprocessRecorder()
    monkeypatch.setattr("subprocess.run", rec)
    return rec

