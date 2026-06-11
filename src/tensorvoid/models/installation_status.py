#!/usr/bin/env python3
from dataclasses import dataclass

@dataclass(frozen=True)
class InstallationStatus:
    """Immutable data transfer object representing the status of a system component."""
    component_name: str
    installed: bool
    details: str
