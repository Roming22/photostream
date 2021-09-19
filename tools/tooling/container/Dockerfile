# TODO: Freeze version and automate versions update
FROM docker.io/python:3.9 AS builder

# Make sure we don't get notifications we can't answer during building.
ENV DEBIAN_FRONTEND noninteractive

#
# Default config
#
COPY tools/tooling/container/builder /opt/container
RUN groupadd -g 9999 user \
    && useradd --create-home --gid user --shell /bin/bash --system --uid 9999 user \
    && apt-get update \
    && for PACKAGE in `cat /opt/container/packages.txt`; do {\
        echo "Installing $PACKAGE"; \
        apt-get install -y "${PACKAGE}" \
        || { echo "Cannot install $PACKAGE"; exit 1; }; \
    }; done \
    && apt-get clean \
    && rm -rf /opt/container \
    && mkdir /opt/app \
    && chown user:user /opt/app
USER user
ENV PATH="/home/user/.local/bin:/usr/local/bin:/usr/bin:/bin"



################################################################################
FROM builder AS release

WORKDIR /opt/app

COPY --chown=user:user Makefile poetry.lock poetry.toml pyproject.toml src/ /opt/app/
RUN make app

CMD ["bin/server.sh"]
HEALTHCHECK --start-period=10s --interval=30s --timeout=5s --retries=3 \
    CMD healthcheck.sh || exit 1

################################################################################
FROM builder AS dev

COPY tools/tooling/container/dev /opt/container
USER root
RUN apt-get update \
    && for PACKAGE in `cat /opt/container/packages.txt`; do {\
        apt-get install -y "${PACKAGE}" \
        || { echo "Cannot install $PACKAGE"; exit 1; }; \
    }; done \
    && apt-get clean \
    && rm -rf /opt/container
USER user
