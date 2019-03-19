import pytest
import os
from unittest.mock import patch
from unittest.mock import Mock
from resourcedownloader.downloadservice.ftp_downloader import FTPDownloader


class TestFTPDownloader(object):

    downloaded_file = ''

    @classmethod
    def setup_class(self):
        self.url = 'ftp://speedtest:speedtest@ftp.otenet.gr/test100k.db'

    @classmethod
    def teardown_class(self):
        if os.path.exists(TestFTPDownloader.downloaded_file):
            os.remove(TestFTPDownloader.downloaded_file)

    def test_download_file_success(self, tmpdir):
        ftp_downloader = FTPDownloader(self.url, str(tmpdir))
        ftp_downloader.download_resource('id1')
        TestFTPDownloader.downloaded_file = ftp_downloader.path_downloaded_file
        assert os.path.exists(ftp_downloader.path_downloaded_file)

    def test_download_file_failure(self, tmpdir):
        with patch('resourcedownloader.downloadservice.ftp_downloader.FTP') as mockedFTPServer:
            mock_object = mockedFTPServer.return_value
            mock_object.retrbinary.side_effect = Mock(side_effect=Exception())
            ftp_downloader = FTPDownloader(self.url, str(tmpdir))
            with pytest.raises(Exception):
                 ftp_downloader.download_resource('id2')
            assert not os.path.exists(ftp_downloader.path_downloaded_file)
