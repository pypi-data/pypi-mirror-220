import setuptools
import os

dev_test_version_file = "dev_pkg_version"
dev_test_version = "1.0.0"

try:
    with open(dev_test_version_file, 'r') as f:
        val = f.readline().split()
        dev_test_version = ".".join(val)
except OSError:
    print('openapi version file not found')

openapi_modules = setuptools.find_packages("openapi_server")
# provide full path for the modules
openapi_modules = ["openapi_server." + module for module in openapi_modules]
openapi_modules.append("openapi_server")

setuptools.setup(
    name="openapi_dev_test",
    version=dev_test_version,
    author="BD Data Sys IE CDN",
    description="Development test package for branch test_branch",
    url="https://code.byted.org/savanna/dingman_api_server",
    packages=openapi_modules,
    include_package_data=True,
    python_requires=">=3.7",
    install_requires = [
        "flask",
        "Flask-Testing"
    ],
)
# files_to_upload = os.listdir("./dist")
# print(f"setup.py: {files_to_upload}")