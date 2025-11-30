"""
Environment detection module - identifies system capabilities and requirements
Phase 1.1: ENV-01, ENV-02, ENV-04
"""
import sys
import subprocess
from typing import Dict, Tuple, Optional
from pathlib import Path
from src.utils.logger import logger
from src.utils.system_utils import SystemUtils
from src.utils.error_handler import EnvironmentError, DependencyError


class EnvironmentDetector:
    """Detects system environment and capabilities"""

    # Minimum Python versions supported
    MIN_PYTHON_VERSION = (3, 8)
    MAX_PYTHON_VERSION = (3, 10)

    # Recommended hardware specs
    RECOMMENDED_SPECS = {
        "cpu_cores": 8,
        "ram_gb": 16,
        "vram_gb": 12,
        "disk_gb": 50,
    }

    MINIMUM_SPECS = {
        "cpu_cores": 4,
        "ram_gb": 8,
        "vram_gb": 6,
        "disk_gb": 10,
    }

    def __init__(self):
        """Initialize environment detector"""
        self.system_info = SystemUtils.get_system_summary()
        self.checks_passed = {}
        self.warnings = []
        self.errors = []

    def run_all_checks(self) -> bool:
        """Run all environment checks"""
        logger.info("=" * 60)
        logger.info("Starting Environment Detection...")
        logger.info("=" * 60)

        checks = [
            ("OS Compatibility", self.check_os_compatibility),
            ("Python Version", self.check_python_version),
            ("GPU Availability", self.check_gpu),
            ("System Specifications", self.check_system_specs),
        ]

        all_passed = True
        for check_name, check_func in checks:
            try:
                result = check_func()
                self.checks_passed[check_name] = result
                if not result:
                    all_passed = False
            except Exception as e:
                logger.error(f"Error in {check_name}: {e}")
                self.errors.append(f"{check_name}: {e}")
                all_passed = False

        self._print_summary()
        return all_passed

    def check_os_compatibility(self) -> bool:
        """Check if OS is supported (ENV-01)"""
        supported_os = ["Windows", "Linux", "Darwin"]
        current_os = self.system_info["os"]

        if current_os in supported_os:
            logger.info(f"✓ OS Compatibility: {current_os} is supported")
            return True
        else:
            error_msg = f"Unsupported OS: {current_os}"
            logger.error(f"✗ {error_msg}")
            self.errors.append(error_msg)
            return False

    def check_python_version(self) -> bool:
        """Check Python version compatibility (ENV-02)"""
        py_version = self.system_info["python_version"]
        version_tuple = sys.version_info[:2]

        if self.MIN_PYTHON_VERSION <= version_tuple <= self.MAX_PYTHON_VERSION:
            logger.info(f"✓ Python Version: {py_version} is compatible")
            return True
        else:
            error_msg = (
                f"Python {py_version} not supported. "
                f"Required: {self.MIN_PYTHON_VERSION[0]}.{self.MIN_PYTHON_VERSION[1]}"
                f"-{self.MAX_PYTHON_VERSION[0]}.{self.MAX_PYTHON_VERSION[1]}"
            )
            logger.error(f"✗ {error_msg}")
            self.errors.append(error_msg)
            return False

    def check_gpu(self) -> bool:
        """Check GPU availability and specs (ENV-01, ENV-04)"""
        gpu_info = self.system_info["gpu"]

        if gpu_info["has_gpu"]:
            logger.info(f"✓ GPU Detected: {gpu_info['gpu_type']}")
            logger.info(f"  - VRAM: {gpu_info['vram_gb']:.2f} GB")
            logger.info(f"  - CUDA Version: {gpu_info['cuda_version']}")

            if gpu_info["vram_gb"] < self.MINIMUM_SPECS["vram_gb"]:
                warning_msg = (
                    f"GPU VRAM ({gpu_info['vram_gb']:.2f}GB) below recommended "
                    f"({self.RECOMMENDED_SPECS['vram_gb']}GB). Performance may be degraded."
                )
                logger.warning(f"⚠ {warning_msg}")
                self.warnings.append(warning_msg)

            return True
        else:
            warning_msg = "No GPU detected. Training will be significantly slower (CPU-only mode)"
            logger.warning(f"⚠ {warning_msg}")
            self.warnings.append(warning_msg)
            return True  # CPU-only is acceptable but degraded

    def check_system_specs(self) -> bool:
        """Check system specifications against minimums (ENV-01)"""
        specs = self.system_info
        all_good = True

        # Check CPU cores
        cpu_cores = specs["cpu"]["cores"]
        if cpu_cores >= self.MINIMUM_SPECS["cpu_cores"]:
            logger.info(f"✓ CPU Cores: {cpu_cores} (minimum: {self.MINIMUM_SPECS['cpu_cores']})")
        else:
            warning_msg = f"CPU cores ({cpu_cores}) below minimum ({self.MINIMUM_SPECS['cpu_cores']})"
            logger.warning(f"⚠ {warning_msg}")
            self.warnings.append(warning_msg)

        # Check RAM
        ram_available = specs["memory"]["available_gb"]
        if ram_available >= self.MINIMUM_SPECS["ram_gb"]:
            logger.info(f"✓ Available RAM: {ram_available:.2f} GB (minimum: {self.MINIMUM_SPECS['ram_gb']})")
        else:
            error_msg = f"Available RAM ({ram_available:.2f}GB) below minimum ({self.MINIMUM_SPECS['ram_gb']}GB)"
            logger.error(f"✗ {error_msg}")
            self.errors.append(error_msg)
            all_good = False

        # Check disk space
        disk_free = specs["disk"]["free_gb"]
        if disk_free >= self.MINIMUM_SPECS["disk_gb"]:
            logger.info(f"✓ Free Disk Space: {disk_free:.2f} GB (minimum: {self.MINIMUM_SPECS['disk_gb']})")
        else:
            error_msg = f"Free disk space ({disk_free:.2f}GB) below minimum ({self.MINIMUM_SPECS['disk_gb']}GB)"
            logger.error(f"✗ {error_msg}")
            self.errors.append(error_msg)
            all_good = False

        return all_good

    def get_device_recommendation(self) -> str:
        """Get recommended device for training (cuda or cpu)"""
        gpu_info = self.system_info["gpu"]
        if gpu_info["has_gpu"] and gpu_info["vram_gb"] >= self.MINIMUM_SPECS["vram_gb"]:
            return "cuda"
        else:
            return "cpu"

    def _print_summary(self) -> None:
        """Print detection summary"""
        logger.info("-" * 60)
        logger.info("SYSTEM SUMMARY:")
        logger.info(f"  OS: {self.system_info['os']} ({self.system_info['os_version']})")
        logger.info(f"  Python: {self.system_info['python_version']}")
        logger.info(f"  CPU: {self.system_info['cpu']['cores']} cores, {self.system_info['cpu']['threads']} threads")
        logger.info(f"  RAM: {self.system_info['memory']['total_gb']:.2f} GB ({self.system_info['memory']['available_gb']:.2f} GB available)")
        
        gpu = self.system_info["gpu"]
        if gpu["has_gpu"]:
            logger.info(f"  GPU: {gpu['gpu_type']} ({gpu['vram_gb']:.2f} GB VRAM)")
        else:
            logger.info(f"  GPU: None (CPU-only mode)")
        
        logger.info(f"  Disk: {self.system_info['disk']['free_gb']:.2f} GB free")
        logger.info("-" * 60)

        if self.errors:
            logger.error(f"\n❌ {len(self.errors)} Critical Errors:")
            for err in self.errors:
                logger.error(f"  - {err}")

        if self.warnings:
            logger.warning(f"\n⚠️  {len(self.warnings)} Warnings:")
            for warn in self.warnings:
                logger.warning(f"  - {warn}")

        if not self.errors:
            logger.info("\n✅ Environment detection passed!")

    def get_report(self) -> Dict:
        """Get detailed detection report"""
        return {
            "system_info": self.system_info,
            "checks_passed": self.checks_passed,
            "warnings": self.warnings,
            "errors": self.errors,
            "device_recommendation": self.get_device_recommendation(),
        }
