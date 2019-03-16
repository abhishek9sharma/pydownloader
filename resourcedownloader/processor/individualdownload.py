import  requests

class DownloadWorker(object):

    def __init__(self, resourceurl, path_download_dir):
        self._resourceurl = resourceurl
        self._path_download_dir = path_download_dir
        self.chunk_size = 1024 * 1024  # 1mb
        self.downloaded_parts = 0

    def download(self):
        with open(self._path_download_dir + 'download', 'wb') as fp:
            response = requests.get(self._resourceurl, stream=True)
            for content in response.iter_content(self.chunk_size):
                self.downloaded_parts += 1
                fp.write(content)
                print('#' * self.downloaded_parts)



dr = DownloadWorker('http://speedtest.ftp.otenet.gr/files/test10Mb.db', 'F:\AgodaTest\\')
dr.download()
