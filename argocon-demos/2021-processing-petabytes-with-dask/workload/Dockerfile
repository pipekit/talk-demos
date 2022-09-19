FROM python:3.8.8-buster
LABEL authors="D. Severin Ryberg, JP Zivalich"
LABEL contact="s.ryberg@accure.net, jp@pipekit.io"
LABEL description="Deployable image for simple Dask workflow execution"

ARG PACKAGE_DIR=windy_city

COPY requirements.txt ${PACKAGE_DIR}/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r ${PACKAGE_DIR}/requirements.txt && \
    pip cache purge

COPY data ${PACKAGE_DIR}/data
COPY dask_pipeline.py ${PACKAGE_DIR}/dask_pipeline.py

WORKDIR ${PACKAGE_DIR}

# Allows Docker/Kubernetes to access an arbitrary executable (also with venv activation)
RUN cd / && \
    echo \
    "#!/bin/bash\
    exec \"\$@\"" | sed 's/   */\n/g' > entrypoint.sh \
    && chmod +x entrypoint.sh

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
