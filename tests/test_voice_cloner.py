"""
Unit tests for Voice Cloner modules
"""
import unittest
from pathlib import Path
from src.config.config import Config
from src.modules.environment_detector import EnvironmentDetector
from src.utils.system_utils import SystemUtils
from src.utils.error_handler import VoiceClonerError


class TestSystemUtils(unittest.TestCase):
    """Test system utility functions"""

    def test_os_detection(self):
        """Test OS detection"""
        os_type = SystemUtils.detect_os()
        self.assertIn(os_type, ["Windows", "Linux", "Darwin"])

    def test_python_version(self):
        """Test Python version detection"""
        version = SystemUtils.check_python_version()
        self.assertEqual(len(version), 3)  # major, minor, micro
        self.assertGreaterEqual(version[0], 3)

    def test_memory_info(self):
        """Test memory information retrieval"""
        memory = SystemUtils.get_memory_info()
        self.assertIn("total_gb", memory)
        self.assertIn("available_gb", memory)
        self.assertGreater(memory["total_gb"], 0)

    def test_disk_space(self):
        """Test disk space information"""
        disk = SystemUtils.get_disk_space()
        self.assertIn("total_gb", disk)
        self.assertIn("free_gb", disk)
        self.assertGreater(disk["total_gb"], 0)

    def test_system_summary(self):
        """Test complete system summary"""
        summary = SystemUtils.get_system_summary()
        self.assertIn("os", summary)
        self.assertIn("python_version", summary)
        self.assertIn("cpu", summary)
        self.assertIn("memory", summary)
        self.assertIn("gpu", summary)
        self.assertIn("disk", summary)


class TestEnvironmentDetector(unittest.TestCase):
    """Test environment detection"""

    def setUp(self):
        """Set up detector for tests"""
        self.detector = EnvironmentDetector()

    def test_os_compatibility(self):
        """Test OS compatibility check"""
        result = self.detector.check_os_compatibility()
        self.assertIsInstance(result, bool)

    def test_python_version_check(self):
        """Test Python version check"""
        result = self.detector.check_python_version()
        self.assertIsInstance(result, bool)

    def test_gpu_check(self):
        """Test GPU detection"""
        result = self.detector.check_gpu()
        self.assertIsInstance(result, bool)

    def test_system_specs(self):
        """Test system specs check"""
        result = self.detector.check_system_specs()
        self.assertIsInstance(result, bool)

    def test_device_recommendation(self):
        """Test device recommendation"""
        device = self.detector.get_device_recommendation()
        self.assertIn(device, ["cuda", "cpu"])

    def test_complete_detection(self):
        """Test complete detection run"""
        success = self.detector.run_all_checks()
        self.assertIsInstance(success, bool)


class TestConfig(unittest.TestCase):
    """Test configuration management"""

    def setUp(self):
        """Set up config for tests"""
        self.config = Config()

    def test_default_paths(self):
        """Test default paths are created"""
        self.assertTrue(isinstance(self.config.DATA_DIR, Path))
        self.assertTrue(isinstance(self.config.OUTPUT_DIR, Path))
        self.assertTrue(isinstance(self.config.MODELS_DIR, Path))

    def test_audio_settings(self):
        """Test audio configuration"""
        self.assertEqual(self.config.SAMPLE_RATE, 44100)
        self.assertGreater(self.config.N_FFT, 0)
        self.assertGreater(self.config.HOP_LENGTH, 0)

    def test_training_settings(self):
        """Test training configuration"""
        self.assertGreater(self.config.TRAINING_EPOCHS, 0)
        self.assertGreater(self.config.BATCH_SIZE, 0)
        self.assertGreater(self.config.LEARNING_RATE, 0)

    def test_config_to_dict(self):
        """Test config conversion to dictionary"""
        config_dict = self.config.to_dict()
        self.assertIsInstance(config_dict, dict)
        self.assertIn("DATA_DIR", config_dict)
        self.assertIn("SAMPLE_RATE", config_dict)


class TestErrorHandling(unittest.TestCase):
    """Test error handling"""

    def test_voice_cloner_error(self):
        """Test VoiceClonerError"""
        with self.assertRaises(VoiceClonerError):
            raise VoiceClonerError("Test error")

    def test_error_message_formatting(self):
        """Test error message formatting"""
        from src.utils.error_handler import handle_error

        error = Exception("Test")
        message = handle_error(error, "testing")
        self.assertIn("Test", message)
        self.assertIn("testing", message)


class TestIntegration(unittest.TestCase):
    """Integration tests"""

    def test_orchestrator_initialization(self):
        """Test orchestrator can be initialized"""
        from src.orchestrator import VoiceClonerOrchestrator

        orchestrator = VoiceClonerOrchestrator()
        self.assertIsNotNone(orchestrator.config)
        self.assertIsNotNone(orchestrator.detector)

    def test_workflow_state_initialization(self):
        """Test workflow state tracking"""
        from src.orchestrator import VoiceClonerOrchestrator

        orchestrator = VoiceClonerOrchestrator()
        state = orchestrator.workflow_state

        self.assertFalse(state["env_detected"])
        self.assertFalse(state["env_setup"])
        self.assertFalse(state["audio_processed"])
        self.assertFalse(state["model_trained"])


if __name__ == "__main__":
    unittest.main()
