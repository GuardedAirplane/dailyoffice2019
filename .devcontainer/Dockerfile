FROM debian:stable-slim

ARG USERNAME=devcontainer
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash-completion \
        ca-certificates \
        curl \
        git \
        sudo \
        unzip \
        vim \
        fish \
        ssh \
        gpg \
        gpg-agent \
        pinentry-curses \
        python3 \
        python3-pip \
        python3-venv \
        postgresql \
        postgresql-contrib \
        memcached \
        libmemcached-tools \
    && rm -rf /var/lib/apt/lists/*

# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 LTS
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://raw.githubusercontent.com/dylanaraps/neofetch/master/neofetch -o /usr/local/bin/neofetch \
    && chmod +x /usr/local/bin/neofetch

RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} --shell /usr/bin/fish \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

# Switch to the target user
USER ${USERNAME}
ENV PATH="/home/${USERNAME}/.local/bin:/home/${USERNAME}/.cargo/bin:${PATH}"

# Install uv package manager as the target user
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Install spec-kit using uv
RUN uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

ENV DEBIAN_FRONTEND=dialog
