from abc import abstractmethod, ABC
import  os
from  urllib.parse import urlparse


class BaseDownloader(ABC):

    def __init__(self, resourceurl, path_download_dir):
        self.resourceurl = resourceurl
        self.path_download_dir = path_download_dir
        self.parsed_url = urlparse(self.resourceurl)
        self.protocol = self.parsed_url.scheme
        self.org_file_name = self.set_org_file_name()
        self.remotedir = os.path.dirname(self.parsed_url.path)
        self.path_downloaded_file = None
        self.size_of_file_to_download = None
        self.size_of_file_downloaded = 0
        self.chunksize = 1024
        self.chunkunit = 'b'
        self.downloadprogress = None

    # Check Late if path and file name can be specified while calling fucnction
    # def download_resource(self, download_path_dir = None, download_file_name = None):
    #     pass

    def set_org_file_name(self):
        try:
            return os.path.basename(self.parsed_url.path)
        except:
            print("Could not find remote file name for resource {0}", self.resourceurl)
            #return  None

    def get_download_path(self):
        return self.path_downloaded_file

    #may be make prooperty
    def set_download_file_path(self):
        try:
            # may be move to utils 
            #change for all alphanumeric
            # what if file already exists
            hostnamechars =['.',':','@']# Load from Config pleas
            netloc = self.parsed_url.netloc
            for char in hostnamechars:
                netloc = netloc.replace(char,'_')

            self.downloaded_file_name = self.protocol + '_' + netloc+ '_'+ self.org_file_name
            self.path_downloaded_file = os.path.join(self.path_download_dir, self.downloaded_file_name)
            if self.path_downloaded_file is None:
                raise Exception('Cannot set download file path for resource {0}', self.resourceurl)
        except Exception as e:
            print(e)
            raise e

    def download_resource(self):
        try:
            self.set_download_file_path()
        except:
            self.path_downloaded_file = None

    def delete_file(self):
        if self.path_downloaded_file is None:
            pass
        else:
            try:
                if  os.path.exists(self.path_downloaded_file):
                    print( " Deleteting file {0} downladed with respect to URL {0}", self.path_downloaded_file, self.resourceurl )
                    os.remove(self.path_downloaded_file)
            except:
                print (' Error occured while removiing file {0}', self.path_downloaded_file)


    
    def get_download_progress(self):
        description = self.downloaded_file_name# + ' is being downloaded at' + self.path_download_dir + self.downloaded_file_name
        curr_percentage_progress =0
        if self.size_of_file_downloaded and self.size_of_file_to_download and self.size_of_file_to_download!=0:
            curr_percentage_progress= int(100 * float(self.size_of_file_downloaded / self.size_of_file_to_download))
        return description, self.size_of_file_downloaded, self.size_of_file_to_download, curr_percentage_progress




