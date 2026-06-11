#!/usr/bin/env python3
from pathlib import Path
from tensorvoid.core.logger_setup import LoggerSetup

class FS:
    """The central Virtual File System (VFS) for path and file resolution."""
    logger = LoggerSetup.get_logger(__qualname__)

    def __init__(self, home_path: str | None = None) -> None:
        """Initializes the FS with an optional home path override."""
        self._home = Path(home_path or Path.home()).resolve()

    def get_home_path(self) -> Path:
        """Returns the absolute path to the user's home directory."""
        return self._home

    def get_android_sdk_path(self) -> Path:
        """Returns the absolute path to the Android Sdk directory."""
        return self._home / "Android" / "Sdk"

    def get_android_cmdline_tools_path(self) -> Path:
        """Returns the path where cmdline-tools are installed."""
        return self.get_android_sdk_path() / "cmdline-tools" / "latest"

    def get_antigravity_app_path(self) -> Path:
        """Returns the absolute path to the Antigravity application directory."""
        return self._home / ".antigravity-app"

    def get_antigravity_launcher_path(self) -> Path:
        """Returns the absolute path to the Antigravity launcher binary."""
        return self._home / ".local" / "bin" / "antigravity"

    def get_bashrc_path(self) -> Path:
        """Returns the path to ~/.bashrc."""
        return self._home / ".bashrc"

    def get_zshrc_path(self) -> Path:
        """Returns the path to ~/.zshrc."""
        return self._home / ".zshrc"

    def get_downloads_path(self) -> Path:
        """Returns the path to the user's Downloads folder."""
        return self._home / "Downloads"

    def check_exists(self, path: Path) -> bool:
        """Checks if a file or directory exists."""
        return path.exists()

    def create_dir(self, path: Path) -> None:
        """Creates a directory and its parent directories if they don't exist."""
        try:
            path.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Created directory: {path}")
        except OSError as e:
            self.logger.error(f"Failed to create directory {path}: {e}")
            raise

    def write_text(self, path: Path, text: str) -> None:
        """Writes text content to a file."""
        try:
            path.write_text(text, encoding="utf-8")
        except OSError as e:
            self.logger.error(f"Failed to write text to {path}: {e}")
            raise

    def read_text(self, path: Path) -> str:
        """Reads text content from a file, returning empty string if not found."""
        if not path.exists():
            return ""
        try:
            return path.read_text(encoding="utf-8")
        except OSError as e:
            self.logger.error(f"Failed to read text from {path}: {e}")
            raise
