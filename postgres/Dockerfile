FROM postgres:16.2

RUN apt-get update
# Set up Ru locale in container
RUN apt-get install locales -y
RUN sed -i 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/g' /etc/locale.gen
ENV LANGUAGE ru_RU.utf8
ENV LANG ru_RU.utf8
ENV LC_ALL ru_RU.utf8
RUN locale-gen ru_RU.utf8 && update-locale LANG=ru_RU.utf8 LANGUAGE=ru_RU.utf8 LC_ALL=ru_RU.utf8

WORKDIR /var/vib/postgres