#!/usr/bin/env python3
import subprocess
import shutil
from tensorvoid.core.logger_setup import LoggerSetup
from tensorvoid.models.installation_status import InstallationStatus

class GcpInstaller:
    """Handles verification, installation, and registration of gcloud CLI and Google API credentials."""
    logger = LoggerSetup.get_logger(__qualname__)

    def __init__(self) -> None:
        """Initializes the installer."""
        pass

    def check_status(self) -> InstallationStatus:
        """Checks if gcloud CLI is installed and configured."""
        gcloud_path = shutil.which("gcloud")
        if not gcloud_path:
            return InstallationStatus(
                component_name="Google Cloud SDK (gcloud)",
                installed=False,
                details="Not found in system PATH"
            )

        try:
            # Query the active gcloud account
            result = subprocess.run(
                ["gcloud", "config", "get-value", "account"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            account = result.stdout.strip()
            
            # Query current default project
            proj_result = subprocess.run(
                ["gcloud", "config", "get-value", "project"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            project = proj_result.stdout.strip()
            
            details = f"Active Account: {account or 'None'} | Project: {project or 'None'}"
            return InstallationStatus(
                component_name="Google Cloud SDK (gcloud)",
                installed=True,
                details=details
            )
        except subprocess.SubprocessError as e:
            self.logger.warning(f"Failed to query gcloud configurations: {e}")
            return InstallationStatus(
                component_name="Google Cloud SDK (gcloud)",
                installed=True,
                details="Installed, configuration query failed"
            )

    def install(self) -> bool:
        """Installs the google-cloud-cli package on Debian/Ubuntu systems."""
        if self.check_status().installed:
            self.logger.info("Google Cloud SDK (gcloud) is already installed. Skipping installation.")
            return True

        self.logger.info("Setting up Google Cloud APT repositories...")
        try:
            # 1. Install pre-requisites
            subprocess.run(
                "sudo apt-get update && sudo apt-get install -y apt-transport-https ca-certificates gnupg curl",
                shell=True, check=True
            )
            
            # 2. Add apt-key
            subprocess.run(
                "curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg",
                shell=True, check=True
            )
            
            # 3. Add source list
            subprocess.run(
                'echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee /etc/apt/sources.list.d/google-cloud-sdk.list',
                shell=True, check=True
            )
            
            # 4. Update and install
            subprocess.run(
                "sudo apt-get update && sudo apt-get install -y google-cloud-cli",
                shell=True, check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"GCP installation failed: {e}")
            return False

    def authenticate(self, project_id: str) -> bool:
        """Runs the interactive gcloud authentication sequence for gcloud and Application Default Credentials (ADC)."""
        self.logger.info("Starting interactive Google Cloud authorization process...")
        try:
            # 1. gcloud auth login
            self.logger.info("--> Authenticating standard CLI session...")
            subprocess.run("gcloud auth login", shell=True, check=True)
            
            # 2. Set project ID
            self.logger.info(f"--> Binding default CLI project to: {project_id}...")
            subprocess.run(f"gcloud config set project {project_id}", shell=True, check=True)
            
            # 3. gcloud auth application-default login
            self.logger.info("--> Generating Application Default Credentials (ADC) for Vertex AI...")
            subprocess.run("gcloud auth application-default login", shell=True, check=True)
            
            # 4. Set quota project in ADC
            self.logger.info(f"--> Setting ADC billing quota project to: {project_id}...")
            subprocess.run(f"gcloud auth application-default set-quota-project {project_id}", shell=True, check=True)
            
            # 5. Enable Vertex AI APIs
            self.logger.info("--> Enabling Vertex AI (aiplatform.googleapis.com) APIs...")
            subprocess.run("gcloud services enable aiplatform.googleapis.com", shell=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Interactive authentication failed or cancelled: {e}")
            return False
