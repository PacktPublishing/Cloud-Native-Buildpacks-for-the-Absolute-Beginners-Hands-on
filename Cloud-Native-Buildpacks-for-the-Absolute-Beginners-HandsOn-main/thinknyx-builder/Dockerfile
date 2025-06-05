# Define the base image
FROM ubuntu:noble

# Install packages that we want to make available at build time
RUN apt-get update && \
  apt-get install -y xz-utils ca-certificates wget && \
  rm -rf /var/lib/apt/lists/*

# Set required CNB user information
ARG cnb_uid=1010
ARG cnb_gid=1010
ENV CNB_USER_ID=${cnb_uid}
ENV CNB_GROUP_ID=${cnb_gid}

# Create user and group
RUN groupadd cnb --gid ${CNB_GROUP_ID} && \
  useradd --uid ${CNB_USER_ID} --gid ${CNB_GROUP_ID} -m -s /bin/bash cnb

# Set user and group
USER ${CNB_USER_ID}:${CNB_GROUP_ID}

# Set required CNB target information
LABEL io.buildpacks.base.distro.name="Linux"
LABEL io.buildpacks.base.distro.version="AMD64"
