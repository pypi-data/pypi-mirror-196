import setuptools
from pathlib import Path

setuptools.setup(
    name='all_params_env',
    version='0.0.1',
    description="A 0penAI Gym Env for Lsm",
    long_description=Path("README.md" ).read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="all_params_env*"),
    install_requires=['gym']  # And any other dependencies foo needs
)