from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'SharePoint Interaction Tool - A package that allows users to interact with files & Folders in a SharePoint Website.'

# Setting up
setup(
    name="sharemint",
    version=VERSION,
    author="Varun Mhatre",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['Office365-REST-Python-Client'],
    keywords=['python', 'sharepoint', 'download', 'upload', 'office365-sharepoint'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)