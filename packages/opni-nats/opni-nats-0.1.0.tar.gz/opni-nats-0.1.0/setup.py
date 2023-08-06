from setuptools import find_packages, setup
import os

setup(
  name="opni-nats",
  version="0.1.0",
  install_requires=["nats-py>=2.2.0","nkeys"],
  packages=find_packages(),
)
