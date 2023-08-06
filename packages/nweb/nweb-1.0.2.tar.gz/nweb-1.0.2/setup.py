"""
python -m pip install --upgrade .
"""

import setuptools

version = "1.0.2"

with open("README.md", "r") as fh:
    long_description = fh.read()

if __name__ == '__main__':
    setuptools.setup(
        name="nweb",
        version=version,
        author="Bjoern Salgert",
        author_email="bjoern.salgert@hs-duesseldorf.de",
        description="nweb",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://bsnx.net/4.0/group/pynwebclient",
        packages=setuptools.find_packages(),
        entry_points={
            'console_scripts': [],
            'nweb_web': [
                'd = nweb.web:DocUi'
            ]
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=["usersettings>=1.0.7", "nwebclient>=1.0.263"]
    )
