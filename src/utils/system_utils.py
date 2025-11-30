"""
System utilities for OS detection, GPU detection, and system info
"""
import platform
import subprocess
import psutil
from typing import Dict, Optional, Tuple
from pathlib import Path


class SystemUtils:
    """System information and detection utilities"""

    @staticmethod
    def detect_os() -> str:
        """Detect operating system (Windows, Linux, Darwin)"""
        system = platform.system()
        return system

    @staticmethod
    def detect_os_version() -> str:
        """Detect OS version"""
        return platform.platform()

    @staticmethod
    def detect_gpu() -> Dict[str, any]:
        """
        Detect GPU availability and type
        Returns dict with keys: has_gpu, gpu_type, compute_capability, vram_gb
        """
        gpu_info = {
            "has_gpu": False,
            "gpu_type": None,
            "compute_capability": None,
            "vram_gb": 0,
            "cuda_version": None,
        }

        try:
            import torch

            if torch.cuda.is_available():
                gpu_info["has_gpu"] = True
                gpu_info["gpu_type"] = torch.cuda.get_device_name(0)
                gpu_info["compute_capability"] = torch.cuda.get_device_capability(0)

                # Get VRAM
                vram_bytes = torch.cuda.get_device_properties(0).total_memory
                gpu_info["vram_gb"] = vram_bytes / (1024 ** 3)

                # Get CUDA version
                gpu_info["cuda_version"] = torch.version.cuda

        except Exception:
            pass

        return gpu_info

    @staticmethod
    def get_cpu_info() -> Dict[str, any]:
        """Get CPU information"""
        return {
            "cores": psutil.cpu_count(logical=False),
            "threads": psutil.cpu_count(logical=True),
            "processor": platform.processor(),
        }

    @staticmethod
    def get_memory_info() -> Dict[str, float]:
        """Get memory information in GB"""
        memory = psutil.virtual_memory()
        return {
            "total_gb": memory.total / (1024 ** 3),
            "available_gb": memory.available / (1024 ** 3),
            "used_gb": memory.used / (1024 ** 3),
            "percent": memory.percent,
        }

    @staticmethod
    def get_disk_space(path: str = ".") -> Dict[str, float]:
        """Get disk space information in GB"""
        disk = psutil.disk_usage(path)
        return {
            "total_gb": disk.total / (1024 ** 3),
            "used_gb": disk.used / (1024 ** 3),
            "free_gb": disk.free / (1024 ** 3),
            "percent": disk.percent,
        }

    @staticmethod
    def check_python_version() -> Tuple[int, int, int]:
        """Check Python version"""
        return (
            platform.python_version_tuple()[0],
            platform.python_version_tuple()[1],
            platform.python_version_tuple()[2],
        )

    @staticmethod
    def check_command_exists(command: str) -> bool:
        """Check if a command exists in PATH"""
        result = subprocess.run(
            ["where" if SystemUtils.detect_os() == "Windows" else "which", command],
            capture_output=True,
        )
        return result.returncode == 0

    @staticmethod
    def get_system_summary() -> Dict[str, any]:
        """Get comprehensive system summary"""
        return {
            "os": SystemUtils.detect_os(),
            "os_version": SystemUtils.detect_os_version(),
            "python_version": ".".join(map(str, SystemUtils.check_python_version())),
            "cpu": SystemUtils.get_cpu_info(),
            "memory": SystemUtils.get_memory_info(),
            "gpu": SystemUtils.detect_gpu(),
            "disk": SystemUtils.get_disk_space(),
        }
