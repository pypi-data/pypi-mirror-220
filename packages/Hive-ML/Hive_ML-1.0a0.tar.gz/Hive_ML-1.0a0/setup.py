import os

import setuptools
from setuptools import setup

with open(os.path.join('VERSION')) as version_file:
    version = version_file.read().strip()


def resolve_requirements(file):
    requirements = []
    with open(file) as f:
        req = f.read().splitlines()
        for r in req:
            if r.startswith("-r"):
                requirements += resolve_requirements(os.path.join(os.path.dirname(file), r.split(" ")[1]))
            else:
                requirements.append(r)
    return requirements


def read_file(file):
    with open(file) as f:
        content = f.read()
    return content


setup(
    name="Hive_ML",
    version=version,
    url="https://github.com/MAIA-KTH/Hive_ML.git",
    license="GPLv3",
    project_urls={
        "Documentation": "https://hive-ml.readthedocs.io",
        "Source": "https://github.com/MAIA-KTH/Hive_ML",
        "Tracker": "https://github.com/MAIA-KTH/Hive_ML/issues",
    },
    author="Bendazzoli Simone",
    author_email="simben@kth.se",
    long_description=read_file(os.path.join(os.path.dirname(__file__), "README.md")),
    long_description_content_type="text/markdown",
    description="Python package to run Machine Learning Experiments, within the Hive Framework.",  # noqa: E501
    packages=setuptools.find_packages(),
    package_data={
        "": ["configs/*.yml", "configs/*.json"],
    },
    data_files=[('', ['VERSION', "requirements.txt"]), ],
    # package_dir={"": "src"},
    install_requires=resolve_requirements(os.path.join(os.path.dirname(__file__), "requirements.txt")),
    entry_points={
        "console_scripts": [
            "Hive_ML_extract_radiomics = Hive_ML_scripts.Hive_ML_extract_radiomics:main",
            "Hive_ML_feature_selection = Hive_ML_scripts.Hive_ML_feature_selection:main",
            "Hive_ML_generate_perfusion_maps = Hive_ML_scripts.Hive_ML_generate_perfusion_maps:main",
            "Hive_ML_model_fitting = Hive_ML_scripts.Hive_ML_model_fitting:main",

        ],
    },
    keywords=["machine learning", "image classification", "PCR", "medical image analysis", "DCE MRI", "radiomics",
              "feature selection", "radiodynamics"],
)
