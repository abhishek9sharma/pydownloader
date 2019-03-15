from abc import abstractmethod, ABC
import  os
from  urllib.parse import urlparse

class BaseDownloader(ABC):

    def __init__(self, resourceurl, path_download_dir):
        self._resourceurl = resourceurl
        self._path_download_dir = path_download_dir
        self._parsed_url = urlparse(self._resourceurl)
        self._org_file_name = self.set_org_file_name()
        self._path_downloaded_file = None
        self._size_of_file_to_download = None
        self._size_of_file_downloaded = 0

    # Check Late if path and file name can be specified while calling fucnction
    # def download_resource(self, download_path_dir = None, download_file_name = None):
    #     pass

    def set_org_file_name(self):
        try:
            return os.path.basename(self._parsed_url.path)
        except:
            return  None

    #may be make prooperty
    def set_download_file_path(self):
        try:
            netloc = self._parsed_url.netloc.replace('.','_')# may be move to utils
            self._path_downloaded_file = os.path.join(self._path_download_dir, netloc+ '_'+ self._org_file_name)
        except:
            self._path_downloaded_file = None

    def download_resource(self):
        try:
            self._path_downloaded_file = self.set_download_file_path()
        except:
            pass

    def delete_file(self):
        if self._path_downloaded_file is None:
            pass
        else:
            if  os.path.exists(self._path_downloaded_file):
                print( " Deleteting file {0} downladed with respect to URL {0}", self._path_downloaded_file, self._resourceurl )
                os.remove(self._path_downloaded_file)

    def get_state(self):
        pass




