#!/usr/bin/env python3
import subprocess
import shutil
from pathlib import Path
from tensorvoid.core.logger_setup import LoggerSetup
from tensorvoid.models.installation_status import InstallationStatus
from tensorvoid.vfs.fs import FS

class AndroidSdkInstaller:
    """Handles verification and terminal-based installation of Android SDK / ADT."""
    logger = LoggerSetup.get_logger(__qualname__)

    def __init__(self, fs: FS) -> None:
        """Injects the Virtual File System dependency."""
        self.fs = fs

    def check_status(self) -> InstallationStatus:
        """Verifies if Android command-line tools are installed."""
        sdkmanager_path = self.fs.get_android_cmdline_tools_path() / "bin" / "sdkmanager"
        if not self.fs.check_exists(sdkmanager_path):
            return InstallationStatus(
                component_name="Android Development Tools (ADT)",
                installed=False,
                details="sdkmanager not found under Sdk/cmdline-tools/latest"
            )

        # Check what platforms are installed
        try:
            platform_tools_dir = self.fs.get_android_sdk_path() / "platform-tools"
            has_pt = self.fs.check_exists(platform_tools_dir)
            details = "Commandline-tools active"
            if has_pt:
                details += " | platform-tools installed"
            return InstallationStatus(
                component_name="Android Development Tools (ADT)",
                installed=True,
                details=details
            )
        except Exception as e:
            self.logger.warning(f"Error querying sdk status: {e}")
            return InstallationStatus(
                component_name="Android Development Tools (ADT)",
                installed=True,
                details="Commandline-tools active"
            )

    def install(self) -> bool:
        """Downloads, unpacks, and configures the Android command line SDK components."""
        if self.check_status().installed:
            self.logger.info("Android Development Tools (ADT) are already installed. Skipping installation.")
            return True

        sdk_dir = self.fs.get_android_sdk_path()
        cmdline_parent = sdk_dir / "cmdline-tools"
        latest_dir = self.fs.get_android_cmdline_tools_path()
        
        # Temp zip file location
        zip_path = Path("/tmp/commandlinetools.zip")
        url = "https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip"

        self.logger.info("Downloading Android Sdk commandline tools zip...")
        try:
            # Download using curl
            subprocess.run(
                ["curl", "-L", "-o", str(zip_path), url],
                check=True
            )
            
            # Ensure cmdline-tools parent directory exists
            self.fs.create_dir(cmdline_parent)
            
            # Extract to cmdline-tools folder
            self.logger.info("Unzipping commandline-tools...")
            subprocess.run(
                ["unzip", "-o", str(zip_path), "-d", str(cmdline_parent)],
                check=True,
                stdout=subprocess.DEVNULL
            )
            
            # Clean up old latest directory if it exists
            if self.fs.check_exists(latest_dir):
                self.logger.info("Removing pre-existing cmdline-tools 'latest' directory...")
                shutil.rmtree(latest_dir, ignore_errors=True)
                
            # Rename the extracted 'cmdline-tools' inside to 'latest'
            extracted_dir = cmdline_parent / "cmdline-tools"
            if self.fs.check_exists(extracted_dir):
                extracted_dir.rename(latest_dir)
                
            # Accept licenses
            self.logger.info("Accepting Android SDK licenses (running yes | sdkmanager --licenses)...")
            sdkmanager_bin = latest_dir / "bin" / "sdkmanager"
            
            # Use subprocess with shell=True to support yes pipe
            subprocess.run(
                f"yes | {sdkmanager_bin} --licenses",
                shell=True,
                check=True
            )
            
            # Install base packages: platform-tools, platforms;android-34, build-tools;34.0.0
            self.logger.info("Installing essential Sdk platforms and build-tools (android-34)...")
            subprocess.run(
                [str(sdkmanager_bin), "platform-tools", "platforms;android-34", "build-tools;34.0.0"],
                check=True
            )
            
            # Clean up zip
            if zip_path.exists():
                zip_path.unlink()
                
            return True
        except (subprocess.CalledProcessError, OSError, shutil.Error) as e:
            self.logger.error(f"Android SDK installation failed: {e}")
            return False
