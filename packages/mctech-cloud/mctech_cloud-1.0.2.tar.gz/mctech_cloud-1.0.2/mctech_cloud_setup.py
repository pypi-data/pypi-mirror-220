from setuptools import setup, find_packages

setup(
    name="mctech_cloud",
    version="1.0.2",
    packages=find_packages(
        include=["mctech_cloud*"],
        exclude=["*.test", ".mctech_actuator", ".mctech_discovery"]
    ),
    install_requires=["log4py", "fastapi", "starlette",
                      "mctech-actuator", "mctech-discovery"]
)
