import setuptools
from pathlib import Path


setuptools.setup(
    name='lsm_params_env',
    version='0.0.6',
    description="A openAI Gym Params-Env for lsm",
    long_description = Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="lsm_params_env*"),
    install_requires=['gym'],  # And any other dependencies foo needs
)