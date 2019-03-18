from abc import abstractmethod, ABC
import  os, errno
from  urllib.parse import urlparse
from datetime import  datetime
from configparser import  ConfigParser
from path import Path

#TODO : Remove commented Code

class BaseDownloader(ABC):

    def __init__(self, resourceurl, path_download_dir, config_path = None):
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
        self.port = 0
        self.delete_successful = False
        self.connectionactive = False
        self.config_path = self.set_config_path(config_path)
        self.configparser = None

        # self.chunkunit = 'b'
        # self.downloadprogress = None

    def set_config_path(self, config_path):
        try:
            if config_path is None:
                return os.path.join(str(Path(__file__).parents[1]),'config','config.ini')
            else:
                return  os.path.join(os.path.dirname(config_path) , os.path.basename(config_path))
        except:
            return  None
        
    def set_config(self):
        try:
            config_parser = ConfigParser()
            config_path = self.config_path
            if config_path is None:
                raise ValueError(' config file is not set ')
            data = config_parser.read(config_path)
            if len(data)==0:
                raise ValueError(' Could not load configuration data ' )
            else:
                self.configparser = config_parser
                self.set_chunksize()
        except:
            # Did not raise error here so as to proceed with default configs
            self.configparser = None


    def set_chunksize(self):
        try:
            if self.configparser:
                chunksizes = self.configparser['chunksizes']
                chunksize = chunksizes.get(self.protocol, 1024)
                self.chunksize = int(chunksize)
            else:
                self.chunksize = 1024
        except:
            self.chunksize = 1024 # default set to continue process

    def set_org_file_name(self):
        try:
            return os.path.basename(self.parsed_url.path)
        except:
            raise ValueError("Could not find remote file name for resource {0}", self.resourceurl)
  
    def get_download_path(self):
        return self.path_downloaded_file

    def get_currtime_str(self):
        timestampformat = '%Y%m%d__%H%M%S'
        currtime_str = str(datetime.now().strftime(timestampformat))
        return  currtime_str

    def set_download_file_path(self, resourceidx):
        try:
            #hostnamechars =['.',':','@']# Load from Config pleas
            #netloc = self.parsed_url.netloc
            #for char in hostnamechars:
            #    netloc = netloc.replace(char,'_')
            #self.downloaded_file_name = resourceidx +'_' + self.get_cuurtime_str() + '_'+ self.protocol + '_' + netloc+ '_'+ self.org_file_name
            self.downloaded_file_name = resourceidx + '_' +self.protocol +'_' + self.get_currtime_str() + '_' + self.org_file_name

            self.path_downloaded_file = os.path.join(self.path_download_dir, self.downloaded_file_name)
            if self.path_downloaded_file is None:
                raise ValueError('Cannot set download file path for resource {0}', self.resourceurl)
        except Exception as e:
            raise

    def download_resource(self, resourceidx):
        try:
            self.set_config()
            self.set_download_file_path(resourceidx)
        except:
            raise

    def delete_file(self):
        if self.path_downloaded_file is None:
            pass
        else:
            try:
                os.remove(self.path_downloaded_file)
                self.deletesuccessful = True
            except OSError as osexcp:
                if osexcp.errno == errno.ENOENT:
                    self.delete_successful = True #check this later
                else:
                    raise

    
    def get_download_progress(self):
        try:
            description = self.downloaded_file_name
            curr_percentage_progress =0
            if self.size_of_file_downloaded and self.size_of_file_to_download and self.size_of_file_to_download!=0:
                curr_percentage_progress= int(100 * float(self.size_of_file_downloaded / self.size_of_file_to_download))
            return description, self.size_of_file_downloaded, self.size_of_file_to_download, curr_percentage_progress
        except:
            return self.downloaded_file_name, 0, 0, 0




