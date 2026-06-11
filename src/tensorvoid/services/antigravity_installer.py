#!/usr/bin/env python3
#!/usr/bin/env python3
import subprocess
import shutil
from pathlib import Path
from tensorvoid.core.logger_setup import LoggerSetup
from tensorvoid.models.installation_status import InstallationStatus
from tensorvoid.vfs.fs import FS

class AntigravityInstaller:
    """Handles verification for the Antigravity SDK (agy) and Antigravity 2."""
    logger = LoggerSetup.get_logger(__qualname__)

    def __init__(self, fs: FS) -> None:
        """Injects the Virtual File System dependency."""
        self.fs = fs

    def check_status(self) -> InstallationStatus:
        """Verifies if the Antigravity SDK and CLI are set up."""
        agy_path = shutil.which("agy")
        antigravity_path = shutil.which("antigravity")
        
        installed = bool(agy_path or antigravity_path)
        
        details = []
        if agy_path:
            details.append(f"agy: {agy_path}")
        if antigravity_path:
            details.append(f"antigravity: {antigravity_path}")
            
        if not installed:
            return InstallationStatus(
                component_name="Antigravity SDK (agy)",
                installed=False,
                details="agy/antigravity CLI not found in PATH"
            )
            
        return InstallationStatus(
            component_name="Antigravity SDK (agy)",
            installed=True,
            details=" | ".join(details)
        )

    def install(self) -> bool:
        """Checks for Antigravity SDK installation and prompts if missing."""
        if self.check_status().installed:
            self.logger.info("Antigravity SDK is already installed. Skipping.")
            return True
            
        self.logger.warning(
            "Antigravity SDK (agy) must be installed via its official distribution channel. "
            "Please consult the Antigravity documentation to install the CLI on this machine."
        )
        return True

