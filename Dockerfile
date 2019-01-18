FROM python:3.7

RUN pip install es_data_export

EXPOSE 9145

ENTRYPOINT ["es_data_exporter"]