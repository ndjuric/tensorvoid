#!/usr/bin/env python3
from typing import Protocol
from tensorvoid.models.installation_status import InstallationStatus

class InstallerProtocol(Protocol):
    """Protocol defining the structural contract for system component installers."""

    def check_status(self) -> InstallationStatus:
        """Checks the current installation status of the component."""
        ...

    def install(self) -> bool:
        """Executes the installation sequence for the component."""
        ...
