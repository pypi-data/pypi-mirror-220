# test_pip_package_custom_installer.py
import subprocess
import requests
import unittest
from unittest.mock import MagicMock, patch
from PipPackageInstaller.pip_custome_package_installer import PipPackageCustomInstaller

class TestPipPackageCustomInstaller(unittest.TestCase):

    def test_package_exists_on_pypi_found(self):
        package_name = "test_package"
        version = "1.0"
        installer = PipPackageCustomInstaller(package_name, version)
        installer.package_exists_on_pypi = MagicMock(return_value=("test_package==1.0", ["1.0", "1.1", "1.2"]))
        result = installer.package_exists_on_pypi()
        self.assertEqual(result, ("test_package==1.0", ["1.0", "1.1", "1.2"]))

    def test_package_exists_on_pypi_not_found(self):
        package_name = "nonexistent_package"
        installer = PipPackageCustomInstaller(package_name)
        installer.package_exists_on_pypi = MagicMock(return_value=(False, False))
        result = installer.package_exists_on_pypi()
        self.assertEqual(result, (False, False))

    def test_package_exists_on_pypi_version_not_found(self):
        package_name = "test_package"
        version = "2.0"
        installer = PipPackageCustomInstaller(package_name, version)
        installer.package_exists_on_pypi = MagicMock(return_value=("test_package==1.0", ["1.0", "1.1", "1.2"]))
        result = installer.package_exists_on_pypi()
        self.assertEqual(result, ("test_package==1.0", ["1.0", "1.1", "1.2"]))

    def test_package_exists_on_pypi_latest_version(self):
        package_name = "test_package"
        installer = PipPackageCustomInstaller(package_name)
        installer.package_exists_on_pypi = MagicMock(return_value=("test_package==1.2", ["1.0", "1.1", "1.2"]))
        result = installer.package_exists_on_pypi()
        self.assertEqual(result, ("test_package==1.2", ["1.0", "1.1", "1.2"]))

    @patch('requests.get')
    def test_package_exists_on_pypi_connection_error(self, mock_get):
        package_name = "test_package"
        installer = PipPackageCustomInstaller(package_name)
        mock_get.side_effect = ConnectionError
        result = installer.package_exists_on_pypi()
        self.assertEqual(result, (False, False))

    def test_get_local_version_package_found(self):
        package_name = "test_package"
        version = "1.0"
        installer = PipPackageCustomInstaller(package_name, version)
        installer.get_local_version_package = MagicMock(return_value="test_package==1.0")
        result = installer.get_local_version_package()
        self.assertEqual(result, "test_package==1.0")

    def test_get_local_version_package_not_found(self):
        package_name = "nonexistent_package"
        installer = PipPackageCustomInstaller(package_name)
        installer.get_local_version_package = MagicMock(return_value="Package not found")
        result = installer.get_local_version_package()
        self.assertEqual(result, "Package not found")

    def test_get_local_version_package_version_not_found(self):
        package_name = "test_package"
        installer = PipPackageCustomInstaller(package_name)
        installer.get_local_version_package = MagicMock(return_value="Version not found")
        result = installer.get_local_version_package()
        self.assertEqual(result, "Version not found")

    def test_get_local_version_package_multiple_versions(self):
        package_name = "test_package"
        installer = PipPackageCustomInstaller(package_name)
        installer.get_local_version_package = MagicMock(return_value="test_package==1.2")
        result = installer.get_local_version_package()
        self.assertEqual(result, "test_package==1.2")

    @patch('subprocess.check_output')
    def test_get_local_version_package_subprocess_error(self, mock_check_output):
        package_name = "test_package"
        installer = PipPackageCustomInstaller(package_name)
        mock_check_output.side_effect = subprocess.CalledProcessError(1, "pip show")
        result = installer.get_local_version_package()
        self.assertEqual(result, "Package not found")
        
if __name__ == '__main__':
    unittest.main()