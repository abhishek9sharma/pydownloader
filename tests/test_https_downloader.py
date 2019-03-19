import pytest
import os
from unittest.mock import patch
from unittest.mock import Mock
from resourcedownloader.downloadservice.http_downloader import HTTPDownloader


class TestHTTPSDownloader(object):
    downloaded_file = ''

    @classmethod
    def setup_class(self):
        self.url = 'https://www.python.org/static/community_logos/python-logo-master-v3-TM.png'

    @classmethod
    def teardown_class(self):
        if os.path.exists(TestHTTPSDownloader.downloaded_file):
            os.remove(TestHTTPSDownloader.downloaded_file)

    def test_download_https_file_success(self, tmpdir):
        https_downloader = HTTPDownloader(self.url, str(tmpdir))
        https_downloader.download_resource('id1')
        TestHTTPSDownloader.downloaded_file = https_downloader.path_downloaded_file
        assert os.path.exists(https_downloader.path_downloaded_file)

    def test_download_https_file_failure(self, tmpdir):
        with patch('resourcedownloader.downloadservice.http_downloader.requests') as mock:
            mock.get.side_effect = Mock(side_effect=Exception())
            https_downloader = HTTPDownloader(self.url, str(tmpdir))
            with pytest.raises(Exception):
                https_downloader.download_resource('id2')
            assert not os.path.exists(https_downloader.path_downloaded_file)
