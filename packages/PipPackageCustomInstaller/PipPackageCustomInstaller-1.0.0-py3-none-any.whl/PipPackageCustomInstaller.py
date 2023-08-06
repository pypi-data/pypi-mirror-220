import subprocess
import requests

class PipPackageInstaller:
    
    def __init__(self, package_name: str, version:int= None):
        
        self.package_name = package_name.lower()
        self.version = version
    
    def package_exists_on_pypi(self) -> tuple[str or False, list[str] or False]:
        """
        Checks if a package exists on PyPI and returns the package name to install and the available versions.

        Returns:
            tuple[str or False, list[str] or False]: A tuple containing the package name to install if available,
            and a list of available versions. Returns False, False if the package is not found.
        """
        url = f"https://pypi.org/pypi/{self.package_name}/json"
        response = requests.get(url)

        if response.status_code == 200:
            package_info = response.json()
            version_list = list(package_info["releases"].keys())
            latest_version = version_list[-1]
            package_to_install = f"{self.package_name}=={latest_version}"

            if self.version and self.version not in version_list:
                message = f"The package {self.package_name} is not available in the requested version, but it is available on PyPI in the following versions:\n{version_list}."
                print(message)
                latest_version_message = f"For package {self.package_name}, this is the latest available version: {package_to_install}"
                print(latest_version_message)
                return package_to_install, version_list

            message = f"The installation of {self.package_name}=={self.version} has been requested. Please note that {package_to_install} is the latest version available on PyPI."
            print(message)
            return package_to_install, version_list
        else:
            message = f"The package {self.package_name} is not available on PyPI."
            print(message)
            return False, False
        
    def get_local_version_package(self) -> str:
        """
        Retrieves the locally installed version of a package.
        Returns:
            str: The package name and version if found.
            "Version not found": If the version is not found.
            "Package not found": If the package is not found.

        """
        try:
            result = subprocess.check_output(['pip', 'show', self.package_name]).decode('utf-8')
            lines = result.strip().split('\n')
            for line in lines:
                if line.startswith('Version:'):
                    version = line.split(': ')[-1].strip()
                    print(f"{self.package_name}=={version} is the locally installed version of the package")
                    return f"{self.package_name}=={version}"
            return "Version not found"
        except subprocess.CalledProcessError:
            return "Package not found"

    def install_package(self, environment='local') -> str or None:
            """
            Installs a package from PyPI if it exists and is not already installed locally.

            Returns:
                str or None: A success message if the package is installed successfully.
                An error message if an error occurs during installation.
                None if the package is already installed locally or does not exist on PyPI.

            """
            
            self.package_name = self.package_name.lower()
            package_to_install_info = self.package_exists_on_pypi()
            package_to_install = package_to_install_info[0]
            package_to_install_version = package_to_install_info[1]
            latest_package_version = package_to_install.split("==")[1]
                    
            if not package_to_install:
                return f"The package {self.package_name} does not exist on PyPI."
            
            if self.version not in package_to_install_version:
                
                print(f"The version {self.version} does not exist for package {self.package_name} on PyPI")
                print(f"now the version package for install is the last version {package_to_install}")
                self.version = latest_package_version

            package_to_install_locally = f'{self.package_name}=={self.version}' if self.version else package_to_install
            locally_installed = self.get_local_version_package()
            
            # Check if the package is already installed locally
            if locally_installed == package_to_install_locally:
                message = f"{package_to_install_locally} is already installed, the required package."
                print(message)
                return None
            else:
                print(f"Installing the package {package_to_install_locally} ...")
                try:
                    import pip
                except ImportError:
                    return "pip is not installed. Please install pip to continue."
                try:
                    if environment =='virtualenv':
                        installation = pip.main(['install', package_to_install_locally])
                    else:
                        installation = pip.main(['install', '--user', package_to_install_locally])
                    self.version = self.get_local_version_package()
                    return f"The package {package_to_install_locally} has been installed successfully."
                except Exception as e:
                    return f"An error occurred during the installation of {self.package_name}: {str(e)}"