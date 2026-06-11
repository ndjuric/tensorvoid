#!/usr/bin/env python3
import click
from tensorvoid.core.setup_orchestrator import SetupOrchestrator

@click.command()
@click.option(
    "--project",
    default="PROJECT_NAME",
    help="Default Google Cloud Project ID to configure for the environment."
)
def main(project: str) -> None:
    """Tensor Void Workspace Setup Station: Provisioning ADT and Antigravity securely on Linux."""
    orchestrator = SetupOrchestrator()
    orchestrator.execute()

if __name__ == "__main__":
    main()
