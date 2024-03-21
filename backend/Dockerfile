FROM python:3.12.2-slim

# Making container logs displayable
ENV PYTHONUNBUFFERED 1

# Do not attempt to create .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Creating working directory
WORKDIR /usr/src/Dashboard

COPY . .

COPY ./entrypoint.sh /usr/src/Dashboard/backend/

RUN pip3 install -r ./requirements.txt

EXPOSE 8000

# Running the app
ENTRYPOINT ["sh", "/usr/src/Dashboard/backend/entrypoint.sh"]



