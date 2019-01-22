#!/usr/bin/env python
"""
HTTP server for metrics
"""

import traceback
from urllib.parse import urlparse
from urllib import parse
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from . import collector


class EsSearchExporterHandler(BaseHTTPRequestHandler):
    def __init__(self, config, kerberos, tls, *args, **kwargs):
        self._config = config
        self._kerberos = kerberos
        self._tls = tls
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_GET(self):
        config = self._config
        url = urlparse(self.path)
        if url.path == "/esdata":
            output = collector.search_es(
                config["searches"]["metricbeat_system_cpu"], self._kerberos, self._tls
            )
            self.send_response(200)
            self.end_headers()
            self.wfile.write(output)
        elif url.path == "/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                b"""<html>
      <head><title>Elasticsearch Data Exporter</title></head>
      <body>
      <h1>Elasticsearch Data Exporter</h1>
      <p>Visit <code>/metrics?search=example</code> to use.</p>
      </body>
      </html>"""
            )
        else:
            self.send_response(404)
            self.end_headers()


def start_http_server(config, port, kerberos, tls):
    GetHandler = lambda *args, **kwargs: EsSearchExporterHandler(
        config, kerberos, tls, *args, **kwargs
    )
    server = HTTPServer(("", port), GetHandler)
    print("Starting server, use <Ctrl-C> to stop\n", config)
    server.serve_forever()
