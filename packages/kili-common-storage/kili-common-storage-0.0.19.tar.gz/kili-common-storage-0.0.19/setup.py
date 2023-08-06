import os

import setuptools

module = "kili-common-storage"

if module == "kili-common-storage":
    setuptools.setup(
        name="kili-common-storage",
        version="0.0.19",
        author="Ken.Hu",
        author_email="ken.hu@kilimall.com",
        description="A storage package for kilimall lite",
        long_description="",
        long_description_content_type="text/markdown",
        url="",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            "boto3==1.23.10",
            "esdk-obs-python==3.22.2",
            "opencv-python==4.6.0.66",
            "elastic-apm==5.10.1"
        ]
    )
