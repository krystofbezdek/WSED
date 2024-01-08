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

EXPOSE 8000
# Copy project
COPY . /WSED/
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
