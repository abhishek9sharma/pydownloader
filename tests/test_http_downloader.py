from resourcedownloader.downloadservice.http_downloader import HTTPDownloader
import pytest
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from threading import Thread
import requests
import re


class HTTPRequestHandlerMock(BaseHTTPRequestHandler):

    download_success_case = re.compile(r'successCase')
    mock_server = None

    def do_GET(self):
        if re.search(self.download_success_case, self.path):
            self.send_response(requests.codes.ok)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header("Content-Length", str(8))
            self.end_headers()
            response_content = b'\x00\x00\x00\x00\x00\x00\x00\x00'
            self.wfile.write(response_content)
            return
        else:
            self.send_response(requests.codes.not_found)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            return

    @staticmethod
    def get_free_port():
        server_socket = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
        server_socket.bind(('localhost', 0))
        address, free_port = server_socket.getsockname()
        server_socket.close()
        return free_port

    @staticmethod
    def start_http_server(port):
        HTTPRequestHandlerMock.mock_server = HTTPServer(('localhost', port), HTTPRequestHandlerMock)
        server_thread = Thread(target=HTTPRequestHandlerMock.mock_server.serve_forever)
        server_thread.setDaemon(True)
        server_thread.start()

    @staticmethod
    def stop_http_server():
        HTTPRequestHandlerMock.mock_server.shutdown()


class TestHTTPDownloader(object):
    downloaded_file = ''

    @classmethod
    def setup_class(self):
        self.port = HTTPRequestHandlerMock.get_free_port()
        HTTPRequestHandlerMock.start_http_server(self.port)

    @classmethod
    def teardown_class(self):
        if os.path.exists(TestHTTPDownloader.downloaded_file):
            os.remove(TestHTTPDownloader.downloaded_file)
        HTTPRequestHandlerMock.stop_http_server()

    def test_download_file_success(self, tmpdir):
        url = 'http://localhost:{port}/successCase.txt'.format(port=self.port)
        http_downloader = HTTPDownloader(url, str(tmpdir))
        http_downloader.download_resource('id')
        TestHTTPDownloader.downloaded_file = http_downloader.path_downloaded_file
        assert os.path.exists(http_downloader.path_downloaded_file)
        assert open(http_downloader.path_downloaded_file).read() == b'\x00\x00\x00\x00\x00\x00\x00\x00'.decode('utf-8')

    def test_http_download_return_none(self, tmpdir, monkeypatch):
        url = 'http://localhost:{port}/failureCase.txt'.format(port=self.port)
        http_downloader = HTTPDownloader(url, str(tmpdir))
        with pytest.raises(requests.exceptions.HTTPError):
            http_downloader.download_resource('id')
        assert not os.path.exists(http_downloader.path_downloaded_file)
