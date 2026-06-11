# Tensor Void: High-Voltage Workspace Provisioner
**Target Stack**: Python 3.10+ | click | rich | prompt-toolkit

`tensorvoid` is a cyber-mechanical terminal setup utility designed to bootstrap a fresh Linux workstation for electronics hacking, 3D printing, and high-performance AI development. It automates the installation, permission configuration, and shell-variable integration of:
1. **Google Cloud SDK (`gcloud` CLI)**
2. **Vertex AI Credentials & Quota Project Assignment** (targeting the `PROJECT_NAME` project billing pool)
3. **Java Development Kit (OpenJDK 17)**
4. **Android Command-line Tools / ADT** (`sdkmanager`, platforms-34, build-tools)
5. **Antigravity IDE** (tarball extraction, SUID sandbox security setup, and global wrappers)

---

## 🛠️ Quick Installation (Terminal Walkthrough)

To set up the project locally on your workstation, execute the following commands in order from your terminal inside the `tensorvoid` directory:

### Step 1: Create a Python Virtual Environment
```bash
python3 -m venv venv
```

### Step 2: Activate the Virtual Environment
```bash
source venv/bin/activate
```

### Step 3: Install the Package in Editable (`-e`) Mode
This registers the global binary `tensorvoid` inside your virtual environment's bin folder, so you can run it from anywhere while maintaining active development links:
```bash
pip install -e .
```

---

## 🚀 Running the Wizard

Once installed and activated, start the wizard directly by typing its name in the terminal:

```bash
tensorvoid
```

### Options

* `--project`: Defines the Google Cloud Project ID to configure for active ADC and default cloud paths. Defaults to `PROJECT_NAME`.

## 📦 Extensibility

If you want to configure the environment for a different Google Cloud project (instead of the default `PROJECT_NAME` billing account), pass it via the `--project` flag:

```bash
tensorvoid --project my-custom-gcp-project
```

---

## 🧬 System Architecture

This tool has been built using rigorous design paradigms ensuring total modularity, safety, and visual power:

### 1. Backend Core & Services
* **Composition Root Pattern (Dependency Injection):** No internal hardcoded instantiations. Every service receives its file system references via injection.
* **One Class, One File:** File structure mirrors code namespaces (e.g., `FS` in `fs.py`, `JavaInstaller` in `java_installer.py`).
* **VFS Centralization (`fs.py`):** Path resolutions are delegated strictly to the central `FS` class. Raw path-string manipulation and manual pathlib/os checks are heavily restricted outside `fs.py`.
* **The Bouncer Pattern:** All logic is flattened to avoid indentation depth debt, validating pre-conditions early and exiting immediately.
* **Strongly Typed DTOs:** No raw dictionaries are returned. All interfaces speak in immutable `InstallationStatus` data transfer objects.

### 2. Terminal UI
* **Terminal Emulator Awareness:** Rejects static stdout. Instead, it crafts a physical dashboard feeling inside standard ANSI/True-color shells.
* **Cyber-Mechanical Aesthetic:** Styled using pitch-black backgrounds (`#000000`), neon cyber-greens (`#00ff66`), and electric-cyan accents (`#00e5ff`).
* **Interactive prompt-toolkit Dialogs:** Features arrow-key and keyboard-responsive select dialogs, auto-completes, and checkboxes built with zero external screen-buffer leakage.
* **Subprocess Redirection Safety:** Ensures that all system interactive processes (e.g. `sudo`, web oauth redirects) run without terminal freezes, maintaining absolute terminal scrollback history upon script exit.
