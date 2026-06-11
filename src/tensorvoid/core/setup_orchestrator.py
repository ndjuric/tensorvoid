#!/usr/bin/env python3
from tensorvoid.vfs.fs import FS
from tensorvoid.services.java_installer import JavaInstaller
from tensorvoid.services.gcp_installer import GcpInstaller
from tensorvoid.services.android_sdk_installer import AndroidSdkInstaller
from tensorvoid.services.antigravity_installer import AntigravityInstaller
from tensorvoid.services.profile_configurator import ProfileConfigurator
from tensorvoid.ui.terminal_ui import TerminalUi

class SetupOrchestrator:
    """The Composition Root of the application, orchestrating all services and triggering the Terminal UI."""

    def __init__(self) -> None:
        """Initializes and wires all system installers and utilities via dependency injection."""
        self.fs = FS()
        
        # Instantiate all modular sub-services
        self.java = JavaInstaller()
        self.gcp = GcpInstaller()
        self.sdk = AndroidSdkInstaller(fs=self.fs)
        self.antigravity = AntigravityInstaller(fs=self.fs)
        self.profile = ProfileConfigurator(fs=self.fs)
        
        # Inject all instances into the user interface manager
        self.ui = TerminalUi(
            fs=self.fs,
            java_installer=self.java,
            gcp_installer=self.gcp,
            sdk_installer=self.sdk,
            antigravity_installer=self.antigravity,
            profile_configurator=self.profile
        )

    def execute(self) -> None:
        """Triggers the active CLI wizard execution loop."""
        self.ui.run_interactive_wizard()
