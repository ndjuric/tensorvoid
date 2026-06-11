#!/usr/bin/env python3
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.status import Status
from prompt_toolkit.shortcuts import radiolist_dialog, input_dialog
from prompt_toolkit.styles import Style

from tensorvoid.core.logger_setup import LoggerSetup
from tensorvoid.vfs.fs import FS
from tensorvoid.services.java_installer import JavaInstaller
from tensorvoid.services.gcp_installer import GcpInstaller
from tensorvoid.services.android_sdk_installer import AndroidSdkInstaller
from tensorvoid.services.antigravity_installer import AntigravityInstaller
from tensorvoid.services.profile_configurator import ProfileConfigurator

class TerminalUi:
    """The central Cyber-Mechanical terminal user interface for Tensor Void."""
    logger = LoggerSetup.get_logger(__qualname__)

    # Termoelektrana Cyber-Mechanical HSL/ANSI styling
    _STYLE = Style.from_dict({
        'dialog': 'bg:#000000',
        'dialog.body': 'fg:#00e5ff bg:#000000',
        'dialog.border': 'fg:#00ff66',
        'radio-selected': 'fg:#00ff66 bold',
        'radio-checked': 'fg:#00ff66',
        'button': 'fg:#00e5ff',
        'button.focused': 'fg:#000000 bg:#00ff66 bold',
    })

    def __init__(
        self,
        fs: FS,
        java_installer: JavaInstaller,
        gcp_installer: GcpInstaller,
        sdk_installer: AndroidSdkInstaller,
        antigravity_installer: AntigravityInstaller,
        profile_configurator: ProfileConfigurator
    ) -> None:
        """Injects core installer service dependencies."""
        self.fs = fs
        self.java = java_installer
        self.gcp = gcp_installer
        self.sdk = sdk_installer
        self.antigravity = antigravity_installer
        self.profile = profile_configurator
        self.console = Console()

    def display_welcome(self) -> None:
        """Renders the cyber-mechanical introductory banner."""
        banner = (
            "[bold green]████████╗███████╗███╗   ██╗███████╗ ██████╗ ██████╗ [/bold green][bold cyan]██╗   ██╗ ██████╗ ██╗██████╗ \n"
            "[bold green]╚══██╔══╝██╔════╝████╗  ██║██╔════╝██╔═══██╗██╔══██╗[/bold cyan][bold cyan]██║   ██║██╔═══██╗██║██╔══██╗\n"
            "[bold green]   ██║   █████╗  ██╔██╗ ██║███████╗██║   ██║██████╔╝[/bold cyan][bold cyan]██║   ██║██║   ██║██║██║  ██║\n"
            "[bold green]   ██║   ██╔══╝  ██║╚██╗██║╚════██║██║   ██║██╔══██╗[/bold cyan][bold cyan]╚██╗ ██╔╝██║   ██║██║██║  ██║\n"
            "[bold green]   ██║   ███████╗██║ ╚████║███████║╚██████╔╝██║  ██║[/bold cyan][bold cyan] ╚████╔╝ ╚██████╔╝██║██████╔╝\n"
            "[bold green]   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝[/bold cyan][bold cyan]  ╚═══╝   ╚═════╝ ╚═╝╚═════╝ \n"
            "\n"
            "                 [bold green]⚡ HIGH-VOLTAGE WORKSPACE SETUP STATION ⚡[/]\n"
            "                 [dim]Tailored for Electronics, 3D Printing, & Vertex AI[/]"
        )
        self.console.print(Panel(banner, border_style="green", expand=False))

    def display_status_table(self) -> dict:
        """Checks and prints a high-density, structured system component status table."""
        self.console.print("\n[bold cyan]📡 [SCANNING] Reading current system environment...[/]")
        
        # Check active status of all components
        with Status("[bold green]Querying local binaries...[/]", console=self.console) as status:
            java_status = self.java.check_status()
            gcp_status = self.gcp.check_status()
            sdk_status = self.sdk.check_status()
            antigravity_status = self.antigravity.check_status()
            profile_ok = self.profile.check_is_configured()

        table = Table(
            title="[bold green]WORKSPACE TELEMETRY MATRIX[/]",
            border_style="green",
            header_style="bold cyan",
            expand=False
        )
        table.add_column("Component", style="bold")
        table.add_column("Status", justify="center")
        table.add_column("Details/Info")

        # Row adding helper
        def add_row_helper(name: str, installed: bool, details: str):
            status_cell = "[bold green]✔ ACTIVE[/]" if installed else "[bold red]❌ MISSING[/]"
            table.add_row(name, status_cell, f"[dim]{details}[/]")

        add_row_helper(java_status.component_name, java_status.installed, java_status.details)
        add_row_helper(gcp_status.component_name, gcp_status.installed, gcp_status.details)
        add_row_helper(sdk_status.component_name, sdk_status.installed, sdk_status.details)
        add_row_helper(antigravity_status.component_name, antigravity_status.installed, antigravity_status.details)
        
        profile_cell = "[bold green]✔ CONFIGURED[/]" if profile_ok else "[bold yellow]⚠ UNCONFIGURED[/]"
        table.add_row("Shell Environment Paths", profile_cell, "[dim]Checking .bashrc/.zshrc integration[/]")

        self.console.print(table)
        
        return {
            'java': java_status.installed,
            'gcp': gcp_status.installed,
            'sdk': sdk_status.installed,
            'antigravity': antigravity_status.installed,
            'profile': profile_ok,
            'auth': gcp_status.installed and "Active Account:" in gcp_status.details
        }

    def run_interactive_wizard(self, default_project: str = "PROJECT_NAME") -> None:
        """Launches the interactive arrow-key driven console menu."""
        while True:
            self.display_welcome()
            status_map = self.display_status_table()
            
            def label(text: str, key: str, done_word: str = 'INSTALLED') -> str:
                return f"{text} {'[✔ ' + done_word + ']' if status_map.get(key) else ''}"

            choice = radiolist_dialog(
                title="Tensor Void Workspace Manager",
                text="Select an action using arrow keys and press Enter:",
                values=[
                    ('status', '1. Refresh Telemetry Matrix'),
                    ('java', label('2. Install System Java SDK (JDK 17)', 'java')),
                    ('gcp', label('3. Install Google Cloud SDK (gcloud CLI)', 'gcp')),
                    ('auth', label('4. Authenticate GCP & Link Project', 'auth', 'CONFIGURED')),
                    ('sdk', label('5. Install Android SDK / ADT Components', 'sdk')),
                    ('antigravity', label('6. Install Antigravity IDE (Tarball)', 'antigravity')),
                    ('profile', label('7. Inject Shell Environment Variables', 'profile', 'CONFIGURED')),
                    ('all', '8. Run Full Installation Pipeline (Sequential)'),
                    ('exit', '9. Exit Workspace Wizard'),
                ],
                style=self._STYLE
            ).run()

            # Guard clause: Exit
            if not choice or choice == 'exit':
                self.console.print("\n[bold yellow]🔌 [HALT] Power plant shutting down. Srećno! [/]\n")
                sys.exit(0)

            try:
                self._execute_choice(choice, default_project)
            except Exception as e:
                self.logger.error(f"Error executing command option '{choice}': {e}")
                self.console.print(f"\n[bold red]✖ [ERROR] Operation failed: {e}[/]\n")

            input("\n[dim]Press [ENTER] to return to the main menu...[/]")
            self.console.clear()

    def _execute_choice(self, choice: str, default_project: str) -> None:
        """Routes the user menu selection to the appropriate service."""
        if choice == 'status':
            return  # Re-loops and updates automatically

        if choice == 'java':
            self.console.print("\n[bold cyan]🔧 Triggering OpenJDK 17 installation...[/]")
            success = self.java.install()
            self._print_result(success, "Java SDK installation")
            return

        if choice == 'gcp':
            self.console.print("\n[bold cyan]🔧 Setting up Google Cloud repositories and SDK...[/]")
            success = self.gcp.install()
            self._print_result(success, "Google Cloud SDK installation")
            return

        if choice == 'auth':
            project_id = input_dialog(
                title="GCP Project Mapping",
                text=f"Enter your active Google Cloud Project ID (default is {default_project}):",
                style=self._STYLE
            ).run()
            
            project = project_id.strip() if project_id else default_project
            self.console.print(f"\n[bold cyan]🔐 Launching interactive authentication sequence for project '{project}'...[/]")
            success = self.gcp.authenticate(project)
            self._print_result(success, f"GCP authorization with project '{project}'")
            return

        if choice == 'sdk':
            self.console.print("\n[bold cyan]🔧 Fetching and configuring Android Commandline Tools (ADT)...[/]")
            success = self.sdk.install()
            self._print_result(success, "Android SDK setup")
            return

        if choice == 'antigravity':
            self.console.print("\n[bold cyan]🔧 Extracting and permissions-configuring Antigravity IDE bundle...[/]")
            success = self.antigravity.install()
            self._print_result(success, "Antigravity IDE setup")
            return

        if choice == 'profile':
            project_id = input_dialog(
                title="Profile Environment Variable Injector",
                text=f"Enter the GOOGLE_CLOUD_PROJECT ID to export (default is {default_project}):",
                style=self._STYLE
            ).run()
            
            project = project_id.strip() if project_id else default_project
            self.console.print(f"\n[bold cyan]🔧 Injecting PATH and environmental blocks pointing to '{project}'...[/]")
            success = self.profile.configure(project)
            self._print_result(success, "Profile path configuration")
            return

        if choice == 'all':
            self._run_all_pipeline(default_project)

    def _run_all_pipeline(self, default_project: str) -> None:
        """Runs the entire installation suite sequentially as a high-density automated pipeline."""
        self.console.print("\n[bold yellow]⚡ starting high-voltage automated setup pipeline...[/]")
        
        project_id = input_dialog(
            title="Automation Suite Configuration",
            text=f"Enter your target GCP Project ID for this machine (default is {default_project}):",
            style=self._STYLE
        ).run()
        project = project_id.strip() if project_id else default_project
        
        # 1. Java
        self.console.print("\n[bold cyan][PHASE 1] Installing Java OpenJDK 17...[/]")
        if not self.java.check_status().installed and not self.java.install():
            self.console.print("[bold red]✖ [HALT] Phase 1 failed. Aborting pipeline.[/]")
            return

        # 2. GCP
        self.console.print("\n[bold cyan][PHASE 2] Installing Google Cloud SDK...[/]")
        if not self.gcp.check_status().installed and not self.gcp.install():
            self.console.print("[bold red]✖ [HALT] Phase 2 failed. Aborting pipeline.[/]")
            return

        # 3. Android ADT
        self.console.print("\n[bold cyan][PHASE 3] Installing Android SDK & platform components...[/]")
        if not self.sdk.check_status().installed and not self.sdk.install():
            self.console.print("[bold red]✖ [HALT] Phase 3 failed. Aborting pipeline.[/]")
            return

        # 4. Antigravity
        self.console.print("\n[bold cyan][PHASE 4] Extracting and setting up Antigravity IDE...[/]")
        if not self.antigravity.check_status().installed and not self.antigravity.install():
            self.console.print("[bold red]✖ [HALT] Phase 4 failed. Aborting pipeline.[/]")
            return

        # 5. Shell variables
        self.console.print("\n[bold cyan][PHASE 5] Injecting profile environment variables...[/]")
        self.profile.configure(project)

        # 6. GCP Auth
        self.console.print("\n[bold cyan][PHASE 6] Running interactive GCP authentication sequence...[/]")
        self.gcp.authenticate(project)

        self.console.print("\n[bold green]✔ [PIPELINE SUCCESSFUL] Your workspace is fully set up and ready to burn silicon! [/]")

    def _print_result(self, success: bool, label: str) -> None:
        """Helper to print standardized success or failure blocks."""
        if success:
            self.console.print(f"\n[bold green]✔ [SUCCESS] {label} completed successfully! [/]")
        else:
            self.console.print(f"\n[bold red]✖ [FAILURE] {label} failed or was cancelled. [/]")
