from setuptools import setup, find_packages

setup(
    name="mctech_actuator",
    version="1.0.4",
    packages=find_packages(
        include=["mctech_actuator*"],
        exclude=["*.test", ".mctech_cloud", ".mctech_discovery"]
    ),
    install_requires=["log4py", "fastapi"]
)
