FROM python:3.7

ADD . /es_data_exporter

WORKDIR /es_data_exporter

RUN pip install -r requirements.txt

EXPOSE 9145

VOLUME [ "/es_data_exporter/config/" ]

ENTRYPOINT ["./scripts/run"]
