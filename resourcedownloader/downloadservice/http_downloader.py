from resourcedownloader.downloadservice.resource_downloader import BaseDownloader
import os
import  requests
from tqdm import  tqdm
import math

class HTTPDownloader(BaseDownloader):
    
    def __init__(self, resourceurl, path_download_dir):
        super().__init__(resourceurl, path_download_dir)
        self._response = None

    def connect(self):
        # Check Doawnloadable
        try:
            #self._response = requests.head(self._resourceurl, stream = True, timeout = 10)
            #self._size_of_file_to_download = int(self._response.headers.get('content-length', 0))

            self._response = requests.get(self._resourceurl, stream=True)
            self._response.raise_for_status()
            self._size_of_file_to_download = int(self._response.headers.get('content-length', 0))
            if self._size_of_file_to_download == 0:
                raise Exception( " Not Able to determine length of the content to be downloaded for url {0}", self._resourceurl)
        except :
            pass
            #Add code for handling the case where header does not case content length or any other exception that may occur while setting up
            # connection

    def disconnect(self):
        if self._response:
            self._response.close()

    def abortdownload(self):
        try:
            self.delete_file()
            self.disconnect()
        except:
            pass

    def download_resource(self):
        try:
            self.set_download_file_path()
            self.connect()
            #print('donloading file for url', self._resourceurl)
            with open(self._path_downloaded_file, 'wb') as f:
                    for current_chunk in self._response.iter_content(chunk_size = self._chunksize):
                        if current_chunk:
                            #len_current_chunk = len(current_chunk)
                            self._size_of_file_downloaded += f.write(current_chunk)
                            #progressbar.update(len_current_chunk)

            self.disconnect()
        except Exception as e:
            print(e, " aborting download for {0} due to some exception while downloading", self._resourceurl)
            self.abortdownload()

    # def get_download_progress(self):
    #     #description = self._downloaded_file_name + ' is being downloaded at' + self._path_download_dir + self._downloaded_file_name
    #     return self._size_of_file_downloaded, self._size_of_file_to_download



  
    
    


