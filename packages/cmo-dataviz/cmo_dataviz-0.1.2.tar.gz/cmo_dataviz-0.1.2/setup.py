from setuptools import setup, find_packages
from pathlib import Path

# read the contents of the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="cmo_dataviz",
    version="0.1.2",
    python_requires='>=3.6',
    description='Easily create graphs using custom styling',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jeanine Schoonemann',
    author_email='service@cmotions.nl',
    url='https://Cmotions@dev.azure.com/Cmotions/Packages/_git/cmo_dataviz',
    packages=find_packages(),
    install_requires=[
        "matplotlib>=3.4.2",
        "pandas>=1.2.4",
        "seaborn>=0.11.1",
        "networkx>=2.6.3"
    ],
    extras_require={
        'dev': [
            'black', 
            'jupyterlab', 
            'pytest==7.4.0',
            'ipykernel',
            'twine',
            'pydataset==0.2.0',
            'pytest-mpl==0.16.1',
            'matplotlib==3.7.1',
            'pillow==9.5.0',
            'networkx==3.1',
            'pandas==2.0.0',
        ],
    },
    # files to be shipped with the installation
    # after installation, these can be found with the functions in resources.py
    package_data={
        "cmo_dataviz": [
            "data/*.csv",
            "notebooks/*tutorial*.ipynb",
        ]
    },
)