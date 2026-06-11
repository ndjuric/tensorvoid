#!/usr/bin/env python3
import os
from pathlib import Path
from tensorvoid.core.logger_setup import LoggerSetup
from tensorvoid.vfs.fs import FS

class ProfileConfigurator:
    """Safely and idempotently configures the shell profile environment blocks (.bashrc and .zshrc)."""
    logger = LoggerSetup.get_logger(__qualname__)

    # Static block token to prevent duplicate injection
    _BLOCK_START_MARKER = "# >>> TENSOR VOID CORE CONFIGURATION START >>>"
    _BLOCK_END_MARKER = "# <<< TENSOR VOID CORE CONFIGURATION END <<<"

    def __init__(self, fs: FS) -> None:
        """Injects the Virtual File System dependency."""
        self.fs = fs

    def check_is_configured(self) -> bool:
        """Checks if the Tensor Void configuration block exists in active shell profiles."""
        bashrc = self.fs.get_bashrc_path()
        zshrc = self.fs.get_zshrc_path()
        
        has_bash = self._has_marker(bashrc)
        has_zsh = self._has_marker(zshrc)
        
        # If at least one active shell profile has the marker, we consider it configured
        return has_bash or has_zsh

    def configure(self, project_id: str) -> bool:
        """Idempotently injects the environment configuration block into active profiles."""
        bashrc = self.fs.get_bashrc_path()
        zshrc = self.fs.get_zshrc_path()
        
        block_text = self._build_config_block(project_id)
        
        # Configure .bashrc if it exists
        if self.fs.check_exists(bashrc):
            self._inject_into_profile(bashrc, block_text)
            
        # Configure .zshrc if it exists
        if self.fs.check_exists(zshrc):
            self._inject_into_profile(zshrc, block_text)
            
        return True

    def _has_marker(self, path: Path) -> bool:
        """Scans a file to determine if the Tensor Void marker block is present."""
        if not self.fs.check_exists(path):
            return False
        content = self.fs.read_text(path)
        return self._BLOCK_START_MARKER in content

    def _build_config_block(self, project_id: str) -> str:
        """Generates the environment configuration block string."""
        return (
            f"\n{self._BLOCK_START_MARKER}\n"
            "# ==========================================\n"
            "# Tensor Void: Android SDK & Java Configuration\n"
            "# ==========================================\n"
            "export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64\n"
            "export ANDROID_HOME=$HOME/Android/Sdk\n"
            "export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$HOME/.local/bin:$PATH\n"
            "\n"
            "# ==========================================\n"
            "# Tensor Void: Vertex AI Context Configuration\n"
            "# ==========================================\n"
            f'export GOOGLE_CLOUD_PROJECT="{project_id}"\n'
            f"{self._BLOCK_END_MARKER}\n"
        )

    def _inject_into_profile(self, path: Path, block: str) -> None:
        """Idempotently appends the configuration block to the specified file."""
        if self._has_marker(path):
            self.logger.info(f"Configuration already present in {path.name}. Skipping injection.")
            return

        self.logger.info(f"Injecting Tensor Void configuration block into {path.name}...")
        try:
            content = self.fs.read_text(path)
            
            # Ensure the file ends with a newline before appending
            if content and not content.endswith("\n"):
                content += "\n"
                
            self.fs.write_text(path, content + block)
        except OSError as e:
            self.logger.error(f"Failed to configure profile {path}: {e}")
            raise
