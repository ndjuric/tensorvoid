#!/usr/bin/env python3
import subprocess
import shutil
from tensorvoid.core.logger_setup import LoggerSetup
from tensorvoid.models.installation_status import InstallationStatus

class JavaInstaller:
    """Handles verification and installation of OpenJDK 17."""
    logger = LoggerSetup.get_logger(__qualname__)

    def __init__(self) -> None:
        """Initializes the installer."""
        pass

    def check_status(self) -> InstallationStatus:
        """Checks if OpenJDK is installed and gets its version."""
        java_path = shutil.which("java")
        if not java_path:
            return InstallationStatus(
                component_name="Java Development Kit (JDK 17)",
                installed=False,
                details="Not found in system PATH"
            )

        try:
            result = subprocess.run(
                ["java", "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            # java -version prints version info primarily to stderr
            output = result.stderr or result.stdout
            first_line = output.splitlines()[0] if output else "Java found"
            return InstallationStatus(
                component_name="Java Development Kit (JDK 17)",
                installed=True,
                details=first_line
            )
        except (subprocess.SubprocessError, IndexError) as e:
            self.logger.warning(f"Failed to query java version: {e}")
            return InstallationStatus(
                component_name="Java Development Kit (JDK 17)",
                installed=True,
                details="Installed (Path exists, version query failed)"
            )

    def install(self) -> bool:
        """Installs OpenJDK 17 via the apt package manager."""
        if self.check_status().installed:
            self.logger.info("Java Development Kit (JDK 17) is already installed. Skipping installation.")
            return True

        self.logger.info("Executing system update and package installation...")
        try:
            # Running with output to terminal directly to support interactive sudo prompt
            result = subprocess.run(
                "sudo apt-get update && sudo apt-get install -y openjdk-17-jdk",
                shell=True,
                check=True
            )
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to install OpenJDK: {e}")
            return False
