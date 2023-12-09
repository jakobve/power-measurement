FROM python:3.9-alpine

# Set environment variables
ENV DIRPATH /exporter
ENV VIRTUAL_ENV /venv

# Set the working directory
WORKDIR $DIRPATH

# Update the package manager and install dependencies
RUN apk update && apk add --no-cache bash && pip install --upgrade pip

# Create a non-root user for running the application
RUN adduser --disabled-password --home $DIRPATH --shell /bin/bash user_exporter

# Create and activate a virtual environment
RUN mkdir $VIRTUAL_ENV
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the port on which the application will run
EXPOSE 8000

# Switch to the non-root user
USER user_exporter

# Command to run the application
CMD ["python", "-u", "exporter.py"]