"""
Environment setup module - installs and configures all dependencies
Phase 1.2: ENV-03, ENV-05, ENV-06, ENV-07
"""
import subprocess
import sys
import json
from pathlib import Path
from typing import Optional, Dict
from src.utils.logger import logger
from src.utils.system_utils import SystemUtils
from src.utils.error_handler import EnvironmentError, DependencyError


class EnvironmentSetup:
    """Handles environment setup and configuration"""

    def __init__(self, config):
        """Initialize environment setup"""
        self.config = config
        self.os_type = SystemUtils.detect_os()
        self.gpu_info = SystemUtils.detect_gpu()
        self.setup_log = []

    def run_complete_setup(self) -> bool:
        """Execute complete environment setup (ENV-03 to ENV-07)"""
        logger.info("=" * 60)
        logger.info("Starting Complete Environment Setup...")
        logger.info("=" * 60)

        steps = [
            ("Virtual Environment", self.setup_virtual_environment),
            ("Dependency Installation", self.install_dependencies),
            ("SO-VITS-SVC Repository", self.clone_so_vits_repository),
            ("Pretrained Models", self.download_pretrained_models),
        ]

        for step_name, step_func in steps:
            logger.info(f"\n[{steps.index((step_name, step_func)) + 1}/{len(steps)}] {step_name}...")
            try:
                if not step_func():
                    logger.error(f"✗ {step_name} setup failed")
                    return False
                logger.info(f"✓ {step_name} completed successfully")
            except Exception as e:
                logger.error(f"✗ {step_name} failed: {e}")
                return False

        logger.info("\n" + "=" * 60)
        logger.info("✅ Environment setup completed successfully!")
        logger.info("=" * 60)
        return True

    def setup_virtual_environment(self) -> bool:
        """Create isolated virtual environment (ENV-03)"""
        logger.info("Creating virtual environment...")

        venv_path = self.config.PROJECT_ROOT / "venv"

        try:
            # Create venv
            subprocess.run(
                [sys.executable, "-m", "venv", str(venv_path)],
                check=True,
                capture_output=True,
            )

            logger.info(f"✓ Virtual environment created at {venv_path}")

            # Get venv Python executable
            if self.os_type == "Windows":
                python_exe = venv_path / "Scripts" / "python.exe"
                pip_exe = venv_path / "Scripts" / "pip.exe"
            else:
                python_exe = venv_path / "bin" / "python"
                pip_exe = venv_path / "bin" / "pip"

            # Upgrade pip
            logger.info("Upgrading pip...")
            subprocess.run(
                [str(pip_exe), "install", "--upgrade", "pip"],
                check=True,
                capture_output=True,
            )

            logger.info("✓ Virtual environment setup complete")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create virtual environment: {e}")
            return False

    def install_dependencies(self) -> bool:
        """Install Python dependencies (ENV-06)"""
        logger.info("Installing Python dependencies...")

        try:
            venv_path = self.config.PROJECT_ROOT / "venv"
            if self.os_type == "Windows":
                pip_exe = venv_path / "Scripts" / "pip.exe"
            else:
                pip_exe = venv_path / "bin" / "pip"

            # Install base requirements
            requirements_file = Path(__file__).parent.parent.parent / "requirements.txt"

            subprocess.run(
                [str(pip_exe), "install", "-r", str(requirements_file)],
                check=True,
            )

            # Install CUDA-enabled PyTorch if GPU available
            if self.gpu_info["has_gpu"]:
                logger.info("Installing CUDA-enabled PyTorch...")
                subprocess.run(
                    [
                        str(pip_exe),
                        "install",
                        "torch",
                        "torchvision",
                        "torchaudio",
                        "--index-url",
                        "https://download.pytorch.org/whl/cu118",
                    ],
                    check=True,
                )
                logger.info("✓ CUDA-enabled PyTorch installed")

            logger.info("✓ All dependencies installed successfully")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False

    def clone_so_vits_repository(self) -> bool:
        """Clone SO-VITS-SVC repository (ENV-05)"""
        logger.info(f"Cloning SO-VITS-SVC repository (branch: {self.config.SO_VITS_BRANCH})...")

        so_vits_path = self.config.SO_VITS_DIR

        try:
            # Skip if already exists
            if so_vits_path.exists():
                logger.warning(f"Repository already exists at {so_vits_path}")
                return True

            subprocess.run(
                [
                    "git",
                    "clone",
                    "--branch",
                    self.config.SO_VITS_BRANCH,
                    self.config.SO_VITS_REPO,
                    str(so_vits_path),
                ],
                check=True,
                capture_output=True,
            )

            logger.info(f"✓ SO-VITS-SVC repository cloned to {so_vits_path}")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to clone SO-VITS-SVC repository: {e}")
            logger.info("Make sure Git is installed and in PATH")
            return False

    def download_pretrained_models(self) -> bool:
        """Download required pretrained models (ENV-07)"""
        logger.info("Downloading pretrained models...")

        models = {
            "hubert_soft.pth": "https://huggingface.co/spaces/innnky/nanami/resolve/main/hubert_soft.pth",
            "G_0.pth": "https://huggingface.co/spaces/innnky/nanami/resolve/main/G_0.pth",
            "D_0.pth": "https://huggingface.co/spaces/innnky/nanami/resolve/main/D_0.pth",
        }

        models_dir = self.config.MODELS_DIR
        models_dir.mkdir(parents=True, exist_ok=True)

        try:
            import urllib.request

            for model_name, url in models.items():
                model_path = models_dir / model_name

                if model_path.exists():
                    logger.info(f"✓ {model_name} already exists")
                    continue

                logger.info(f"Downloading {model_name}...")
                try:
                    urllib.request.urlretrieve(url, str(model_path))
                    logger.info(f"✓ {model_name} downloaded")
                except Exception as e:
                    logger.warning(f"⚠ Failed to download {model_name}: {e}")
                    logger.info("You can download models manually from HuggingFace Hub")

            logger.info("✓ Pretrained models setup complete")
            return True

        except Exception as e:
            logger.error(f"Error downloading pretrained models: {e}")
            return False

    def get_environment_info(self) -> Dict:
        """Get environment setup information"""
        venv_path = self.config.PROJECT_ROOT / "venv"
        if self.os_type == "Windows":
            python_exe = venv_path / "Scripts" / "python.exe"
            pip_exe = venv_path / "Scripts" / "pip.exe"
        else:
            python_exe = venv_path / "bin" / "python"
            pip_exe = venv_path / "bin" / "pip"

        return {
            "venv_path": str(venv_path),
            "python_executable": str(python_exe),
            "pip_executable": str(pip_exe),
            "so_vits_path": str(self.config.SO_VITS_DIR),
            "models_path": str(self.config.MODELS_DIR),
            "device": "cuda" if self.gpu_info["has_gpu"] else "cpu",
        }
