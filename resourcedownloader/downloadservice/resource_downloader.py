from abc import abstractmethod, ABC

class BaseDownloader(ABC):

    def __init__(self, resourceuri, path_download_dir):
        self.resourceuri = resourceuri
        self._path_download_dir = path_download_dir
        self._name_of_file_to_download = None
        self._size_of_file_to_download = None
        self._size_of_file_downloaded = None
    

    
    



