from  urllib.parse import urlparse
from resourcedownloader.downloadservice.ftp_downloader import  FTPDownloader
from resourcedownloader.downloadservice.sftp_downloader import  SFTPDownloader
from resourcedownloader.downloadservice.http_downloader import  HTTPDownloader

#TODO : Make Configurable

class DownloadProtocolFactory:

    @staticmethod
    def get_protocol(url):
        parsed_url = urlparse(url)
        protocol = parsed_url.scheme
        if protocol =='http':
            return HTTPDownloader
        elif protocol =='ftp':
            return FTPDownloader
        elif protocol =='sftp':
            return HTTPDownloader
        else:
            raise NotImplementedError ('the network protocol {0} is not supported yet'.format(protocol))
