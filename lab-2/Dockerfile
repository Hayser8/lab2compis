FROM ubuntu:latest

# 1) Instala dependencias del sistema y Python3 + pip + venv
RUN apt-get update && apt-get install -y \
      curl \
      bash-completion \
      openjdk-17-jdk \
      fontconfig \
      fonts-dejavu-core \
      software-properties-common \
      python3 \
      python3-venv \
      python3-pip \
  && rm -rf /var/lib/apt/lists/*

# 2) Crea un virtualenv y prepáralo en el PATH
ENV VENV_PATH=/opt/venv
RUN python3 -m venv ${VENV_PATH}
ENV PATH="${VENV_PATH}/bin:$PATH"

# 3) Copia y instala las dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Instala ANTLR (jar + wrappers)
COPY antlr-4.13.1-complete.jar /usr/local/lib/antlr-4.13.1-complete.jar

COPY commands/antlr /usr/local/bin/antlr
COPY commands/grun  /usr/local/bin/grun
RUN chmod +x /usr/local/bin/antlr /usr/local/bin/grun

# 5) Crea un usuario no-root
ARG USER=appuser
ARG UID=1001
RUN adduser \
      --disabled-password \
      --gecos "" \
      --home /home/${USER} \
      --no-create-home \
      --uid "${UID}" \
      "${USER}"

USER ${USER}

# 6) Define el directorio de trabajo donde montarás tu código
WORKDIR /program
