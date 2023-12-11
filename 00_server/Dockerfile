FROM python:3.6-alpine

# Set environment variables
ENV DIRPATH /server
ENV VIRTUAL_ENV /venv

# Create working directory
WORKDIR $DIRPATH

# 
RUN apk update && apk upgrade --no-cache && apk add --no-cache build-base linux-headers

# CREATE VIRTUAL ENV
RUN mkdir $VIRTUAL_ENV

# Create virtual environment and set python path
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy files into working directory
COPY . .

# Upgrade pip, setuptools and wheel
RUN pip install --upgrade pip setuptools wheel

# Install all requirements from requirements.txt
RUN pip install -r requirements.txt

# Delete build-base and linux-headers
RUN apk del build-base linux-headers

# Expose the port on UDP
EXPOSE 5000/udp

# Start
CMD ["python", "server.py"]
