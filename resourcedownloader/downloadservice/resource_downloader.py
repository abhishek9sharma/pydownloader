from abc import abstractmethod, ABC
import  os
from  urllib.parse import urlparse


class BaseDownloader(ABC):

    def __init__(self, resourceurl, path_download_dir):
        self._resourceurl = resourceurl
        self._path_download_dir = path_download_dir
        self._parsed_url = urlparse(self._resourceurl)
        self._protocol = self._parsed_url.scheme
        self._org_file_name = self.set_org_file_name()
        self._remotedir = os.path.dirname(self._parsed_url.path)
        self._path_downloaded_file = None
        self._size_of_file_to_download = None
        self._size_of_file_downloaded = 0
        self._status = None
        self._chunksize = 1024
        self._chunkunit = 'b'
        self.downloadprogress = None

    # Check Late if path and file name can be specified while calling fucnction
    # def download_resource(self, download_path_dir = None, download_file_name = None):
    #     pass

    def get_status(self):
        return  self._status

    def set_org_file_name(self):
        try:
            return os.path.basename(self._parsed_url.path)
        except:
            print("Could not find remote file name for resource {0}", self._resourceurl)
            #return  None

    def get_download_path(self):
        return self._path_downloaded_file

    #may be make prooperty
    def set_download_file_path(self):
        try:
            # may be move to utils 
            #change for all alphanumeric
            # what if file already exists
            hostnamechars =['.',':','@']# Load from Config pleas
            netloc = self._parsed_url.netloc
            for char in hostnamechars:
                netloc = netloc.replace(char,'_')

            self._downloaded_file_name = self._protocol + '_' + netloc+ '_'+ self._org_file_name
            self._path_downloaded_file = os.path.join(self._path_download_dir, self._downloaded_file_name)
            if self._path_downloaded_file is None:
                raise Exception('Cannot set download file path for resource {0}', self._resourceurl)
        except Exception as e:
            print(e)
            raise e

    def download_resource(self):
        try:
            self.set_download_file_path()
        except:
            self._path_downloaded_file = None

    def delete_file(self):
        if self._path_downloaded_file is None:
            pass
        else:
            try:
                if  os.path.exists(self._path_downloaded_file):
                    print( " Deleteting file {0} downladed with respect to URL {0}", self._path_downloaded_file, self._resourceurl )
                    os.remove(self._path_downloaded_file)
            except:
                print (' Error occured while removiing file {0}', self._path_downloaded_file)


    
    def get_download_progress(self):
        description = self._downloaded_file_name# + ' is being downloaded at' + self._path_download_dir + self._downloaded_file_name
        curr_percentage_progress =0
        if self._size_of_file_downloaded and self._size_of_file_to_download and self._size_of_file_to_download!=0:
            curr_percentage_progress= int(100 * float(self._size_of_file_downloaded / self._size_of_file_to_download))
        return description, self._size_of_file_downloaded, self._size_of_file_to_download, curr_percentage_progress




