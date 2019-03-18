from  urllib.parse import urlparse
from configparser import ConfigParser
from resourcedownloader.downloadservice.ftp_downloader import  FTPDownloader
from resourcedownloader.downloadservice.sftp_downloader import  SFTPDownloader
from resourcedownloader.downloadservice.http_downloader import  HTTPDownloader
import  os

#TODO : Remove COmmented Code

class DownloadProtocolFactory(object):

    @staticmethod
    def get_protocol(url, config_path = 'Config/config.ini'):
        """
        Method which identifies the protocol associated with the url.
        Returns the class whose object should be initiated to download the url.
        Raises error if the protoco is not yet supported
        """
        try:
            parsed_url = urlparse(url)
            protocol = parsed_url.scheme
            configpath = os.path.join(os.path.dirname(config_path), os.path.basename(config_path))
            try:
                protocol_config_parser = ConfigParser()
                protocol_config_parser.read(configpath)
                protocol_dict = {k:v for k,v in protocol_config_parser.items('protocol_selector')}
                if protocol in protocol_dict:
                     return eval(protocol_dict[protocol])
                else:
                    raise NotImplementedError('the network protocol {0} is not supported yet'.format(protocol))
            except:
                raise NotImplementedError('the network protocol {0} is not supported yet'.format(protocol))
        except:
            raise NotImplementedError('the network protocol for url {0} could not be determined'.format(url))

    # if protocol =='http' or protocol =='https':
        #     return HTTPDownloader
        # elif protocol =='ftp':
        #     return FTPDownloader
        # elif protocol =='sftp':
        #     return SFTPDownloader
        # else:
        #     raise NotImplementedError ('the network protocol {0} is not supported yet'.format(protocol))
