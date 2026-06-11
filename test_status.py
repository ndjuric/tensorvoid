from tensorvoid.vfs.fs import FS
from tensorvoid.services.java_installer import JavaInstaller
from tensorvoid.services.gcp_installer import GcpInstaller
from tensorvoid.services.android_sdk_installer import AndroidSdkInstaller
from tensorvoid.services.antigravity_installer import AntigravityInstaller
from tensorvoid.services.profile_configurator import ProfileConfigurator

fs = FS()
print("Java:", JavaInstaller().check_status())
print("GCP:", GcpInstaller().check_status())
print("Android:", AndroidSdkInstaller(fs).check_status())
print("Antigravity:", AntigravityInstaller(fs).check_status())
print("Profile:", ProfileConfigurator(fs).check_is_configured())
