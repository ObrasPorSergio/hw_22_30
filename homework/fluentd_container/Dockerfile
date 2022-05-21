FROM fluent/fluentd:v1.14.6-debian-1.0
USER root
RUN ["gem", "install", "fluent-plugin-elasticsearch", "--no-document", "--version", "1.5.0"]
RUN ["fluent-gem", "install", "fluent-plugin-grok-parser"]
USER fluent
