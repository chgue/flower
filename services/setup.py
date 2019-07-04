from setuptools import setup, find_packages

setup(
    name="flower-backend",
    packages=find_packages(),
    install_requires=[],
    entry_points = {
        "console_scripts": [
            "flower-import = import:main",
            "flower-webserver = webservice:main"
        ]
    }
)
