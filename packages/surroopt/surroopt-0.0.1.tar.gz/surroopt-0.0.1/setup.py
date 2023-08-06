import importlib.util
from setuptools import setup, find_packages

NAME = "surroopt"


def get_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


def get_version():
    spec = importlib.util.spec_from_file_location(NAME, f"./{NAME}/__init__.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version__


setup(
    name=NAME,
    version=get_version(),
    description="Python package of SurroOpt.",
    install_requires=get_requirements(),
    packages=find_packages(),
)