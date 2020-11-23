FROM       python:3
RUN        pip install sitecheck
COPY       . /Sitecheck
WORKDIR    /Sitecheck
RUN        python -m sitecheck --help
