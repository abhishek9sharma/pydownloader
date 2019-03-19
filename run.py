import sys
from resourcedownloader.processor.mainprocessor import DownloadsProcessor

urls = [
        'ftp://speedtest:speedtest@ftp.otenet.gr/test1Mb.db',
        'http://speedtest.ftp.otenet.gr/files/test1Mb.db',
        'sftp://demo-user:demo-user@demo.wftpserver.com:2222/download/manual_en.pdf'
        #'ftp://speedtest:speedtest@ftp.otenet.gr/test1Mb.db',
        #'http://speedtest.ftp.otenet.gr/files/test100k.db',
        #'http://speedtest.ftp.otenet.gr/files/test10Mb.db',
        #'sftp://demo:password@test.rebex.net:22/readme.txt'
        ]

download_dir = 'F:\AgodaTest\\'
downloadmodule = DownloadsProcessor(urls, download_dir)
downloadmodule.download_resources()
