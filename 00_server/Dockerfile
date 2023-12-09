FROM python:3.6-alpine

ENV DIRPATH /mock_server
ENV VIRTUAL_ENV /venv

# Create working directory
WORKDIR $DIRPATH

RUN apk update && pip install --upgrade pip

#RUN useradd --no-log-init --create-home --shell /bin/bash user_mock_server

# CREATE VIRTUAL ENV
RUN mkdir $VIRTUAL_ENV
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . .
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 5000/udp

# USER user_mock_server

# START
CMD ["python", "server.py"]
