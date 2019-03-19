import pytest
from resourcedownloader.downloadservice.download_factory import DownloadProtocolFactory
from resourcedownloader.downloadservice.ftp_downloader import FTPDownloader
from resourcedownloader.downloadservice.sftp_downloader import SFTPDownloader
from resourcedownloader.downloadservice.http_downloader import HTTPDownloader


class TestDownloadFactory(object):

    def test_configured_protocols(self):
        downloader1 = DownloadProtocolFactory.get_protocol('http://dummyhost/dir/file.txt')
        assert isinstance(downloader1, HTTPDownloader.__class__)
        downloader2 = DownloadProtocolFactory.get_protocol('ftp://user:password@dummyhost/dir/file.txt')
        assert isinstance(downloader2, FTPDownloader.__class__)
        downloader3 = DownloadProtocolFactory.get_protocol('sftp://user:password@dummyhost/dir/file.txt')
        assert isinstance(downloader3, SFTPDownloader.__class__)
        downloader4 = DownloadProtocolFactory.get_protocol('https://dummyhost/dir/file.txt')
        assert isinstance(downloader4, HTTPDownloader.__class__)

    def test_unsupported_protocol(self):
        with pytest.raises(NotImplementedError):
            DownloadProtocolFactory.get_protocol('invalid://dummyhost/dir/file.txt')


