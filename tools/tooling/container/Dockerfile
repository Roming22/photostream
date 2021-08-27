# TODO: Freeze version and automate versions update
FROM python:3.8-slim

# Make sure we don't get notifications we can't answer during building.
ENV DEBIAN_FRONTEND noninteractive

#
# Add module and packages
# TODO: Freeze versions and automate versions update
#
COPY tools/tooling/container /opt/container
RUN apt-get update \
    && for PACKAGE in `cat /opt/container/packages.txt`; do apt-get install -y "${PACKAGE}"; done \
    && apt-get clean

#
# Default config
#
RUN groupadd -g 9999 dev \
    && useradd --create-home --gid dev --shell /bin/bash --system --uid 9999 dev \
    && rm /home/dev/.profile

USER dev

ENV PATH="/home/dev/.local/bin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"