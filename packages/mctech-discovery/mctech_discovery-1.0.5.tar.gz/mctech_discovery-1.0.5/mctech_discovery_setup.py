from setuptools import setup, find_packages

setup(
    name="mctech_discovery",
    version="1.0.5",
    packages=find_packages(
        include=["mctech_discovery**"],
        exclude=["*.test", ".mctech_actuator", ".mctech_cloud"]
    ),
    install_requires=["log4py", "netifaces",
                      "py_eureka_client", "pyyaml", "pyDes", "requests",
                      "mctech-actuator", "websocket-client"]
)
