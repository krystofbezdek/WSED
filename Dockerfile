# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /WSED

# Install dependencies
COPY requirements.txt /WSED/
RUN pip install -r requirements.txt

# Copy project
COPY . /WSED/

RUN chmod +x /WSED/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/WSED/entrypoint.sh"]
