# Pull base image
FROM python:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /DST

# Install dependencies
COPY Pipfile Pipfile.lock /DST/

RUN apt-get update && apt-get upgrade -y
RUN pip install pipenv && pipenv install --system


COPY requirements.txt /DST
RUN pip install --no-cache-dir -r ./requirements.txt
COPY . /DST

# define the port number the container should expose
EXPOSE 8000
# CMD ["python", "/DST/manage.py", "runserver"]
