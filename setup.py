from setuptools import setup, find_packages

setup(
    name="gamegen",
    version="0.0.1",
    packages=find_packages(),
    license='MIT',
    install_requires=["gymnasium==0.28.1", "arcade==2.6.17"],
)
