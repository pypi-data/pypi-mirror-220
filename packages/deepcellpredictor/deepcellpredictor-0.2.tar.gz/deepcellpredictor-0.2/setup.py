from setuptools import setup, find_packages
import os

VERSION = '0.2'
DESCRIPTION = "a transfer learning approach that explicitly models changes in transcriptional variance using a combination of variational autoencoders and normalizing flows"

setup(
    name='deepcellpredictor',
    version=VERSION,
    description='transfer learning approach',
    long_description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'numpy==1.21.0',
        'pandas==1.4.2',
        'matplotlib==3.5.2',
        'torch==1.11.0',
        'anndata==0.8.0',
        'pytorch_lightning==1.7.7',
        'scanpy==1.9.1',
        'scipy==1.8.1',
        'scvi==0.19.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires=">=3.6",
)

