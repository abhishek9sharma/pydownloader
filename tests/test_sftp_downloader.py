import pytest
import os
from unittest.mock import patch
from unittest.mock import Mock
import pysftp

from resourcedownloader.downloadservice.sftp_downloader import SFTPDownloader


class TestSFTPDownloader(object):

    downloaded_file = ''

    @classmethod
    def setup_class(self):
        self.url = 'sftp://demo:password@test.rebex.net:22/readme.txt'

    @classmethod
    def teardown_class(self):
        if os.path.exists(TestSFTPDownloader.downloaded_file):
            os.remove(TestSFTPDownloader.downloaded_file)

    def test_download_file_success(self, tmpdir):
        sftp_downloader = SFTPDownloader(self.url, str(tmpdir))
        sftp_downloader.download_resource('id1')
        TestSFTPDownloader.downloaded_file = sftp_downloader.path_downloaded_file
        assert os.path.exists(sftp_downloader.path_downloaded_file)

    def test_download_file_failure(self, tmpdir):
        with patch('resourcedownloader.downloadservice.sftp_downloader.pysftp') as mockedSFTPServer:
            mock_object = mockedSFTPServer.Connection.return_value
            mock_object.get.side_effect = Mock(side_effect=Exception())
            sftp_downloader = SFTPDownloader(self.url, str(tmpdir))
            with pytest.raises(Exception):
               sftp_downloader.download_resource('id2')
            assert not os.path.exists(sftp_downloader.path_downloaded_file)
