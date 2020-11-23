import shutil
from pathlib import Path

from setuptools import setup, find_packages

# Delete previous build files to prevent removed files from remaining
if Path.is_dir(Path('build')):
    print("Cleaning up previous build..")
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("sitecheck.egg-info", ignore_errors=True)


with open("sitecheck/docs/README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sitecheck',
    version='0.8.3.6',
    description='Sitecheck toolkit for Geo-Instruments',
    long_description="long_description",
    long_description_content_type="markdown",
    author='Dan.Edens',
    author_email='Dan.Edens@geo-instruments.com',
    url='https://github.com/DanEdens/Sitecheck_Scrapper',
    packages=find_packages(),
    scripts=['sitecheck/bin/Scanner.cmd'],
    script_args=["bdist_wheel"],
    license='',
    keywords=["geo-instruments"],
    include_package_data=True,
    package_data={
        "": ["*.cmd", "*.md", "*.ini", "*.png",
             "*.jpg", "*.json", "*.url", "*.zip"]
        },
    setup_requires=[
        "appdirs >= 1.4.4",
        "pyee >= 7.0.2",
        "pyppeteer >= 0.2.2",
        "python-dateutil >= 2.8.1",
        "six >= 1.10.0",
        "urllib3 >= 1.25.9",
        "websockets >= 8.1",
        "texttable >=1.6.2"
        ],
    install_requires=[
        "appdirs >= 1.4.4",
        "pyee >= 7.0.2",
        "pyppeteer >= 0.2.2",
        "python-dateutil >= 2.8.1",
        "six >= 1.10.0",
        "urllib3 >= 1.25.9",
        "websockets >= 8.1",
        "texttable >=1.6.2"
        ],
    python_requires='>=3.6'
    )
