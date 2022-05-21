FROM postgres:9.6.21
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin
EXPOSE 5432
VOLUME ["/etc/postgresql", "/var/lib/postgresql"]
CMD ["postgres", "-c", "log_destination=stderr", "-c", "logging_collector=on", "-c", "log_directory=/tmp"]
