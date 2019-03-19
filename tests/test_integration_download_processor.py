import pytest
import os
from resourcedownloader.processor.mainprocessor import DownloadsProcessor
import time
import requests
from unittest.mock import patch
from unittest.mock import Mock


class TestIntegrationDownloadProcessor(object):
    temp_directory = ''

    @classmethod
    def teardown_class(self):
        if os.path.exists(TestIntegrationDownloadProcessor.temp_directory):
            for file in os.listdir(TestIntegrationDownloadProcessor.temp_directory):
                file_path = os.path.join(TestIntegrationDownloadProcessor.temp_directory, file)
                try:
                    os.remove(file_path)
                except Exception as e:
                    pass

    def test_downloads(self, tmpdir):
        urls = [
            'ftp://speedtest.tele2.net/1KB.zip',
            'https://www.python.org/static/community_logos/python-logo-master-v3-TM.png'
        ]
        TestIntegrationDownloadProcessor.temp_directory = tmpdir
        downloadmodule = DownloadsProcessor(urls, tmpdir)
        downloadmodule.download_resources()
        time.sleep(5)
        count_files_downloaded = len(next(os.walk(tmpdir))[2])
        assert (count_files_downloaded == 2)

    def test_invalid_urls(self, tmpdir):
        urls = [
            'ftp://invalid_hostname/1KB.zip',
            'https://something/test.png',
            'sftp://demo-user:wrong_password@demo.wftpserver.com:2222/download/manual_en.pdf'
        ]
        downloadmodule = DownloadsProcessor(urls, tmpdir)
        downloadmodule.download_resources()
        count_files_downloaded = len(next(os.walk(tmpdir))[2])
        assert (count_files_downloaded == 0)

    def test_exception_scenario(self, tmpdir):
        urls = [
            'ftp://speedtest.tele2.net/1KB.zip',
            'https://www.python.org/static/community_logos/python-logo-master-v3-TM.png'
        ]
        with patch('resourcedownloader.downloadservice.http_downloader.requests') as mock:
            downloadmodule = DownloadsProcessor(urls, tmpdir)
            mock.get.side_effect = Mock(side_effect=Exception())
            downloadmodule.download_resources()
        time.sleep(5)
        count_files_downloaded = len(next(os.walk(tmpdir))[2])
        assert (count_files_downloaded == 1)
