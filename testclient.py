from resourcedownloader.processor.mainprocessor import  DownloadsProcessor
from resourcedownloader import processor

urls = [
        #''
        'ftp://speedtest:speedtest@ftp.otenet.gr/test1Mb.db',
        'http://speedtest.ftp.otenet.gr/files/test1Mb.db',
        'sftp://demo-user:demo-user@demo.wftpserver.com:2222/download/manual_en.pdf'
        #'ftp://speedtest:speedtest@ftp.otenet.gr/test1Mb.db',
        #'http://speedtest.ftp.otenet.gr/files/test100k.db',
        #'http://speedtest.ftp.otenet.gr/files/test10Mb.db',
        #'sftp://demo:password@test.rebex.net:22/readme.txt',
        #'http://speedtest.ftp.otenet.gr/files/test1Gb.db',
        #'ftp://speedtest:speedtest@ftp.otenet.gr/test10Gb.db',
        #'ftp://speedtest:speedtest@ftp.otenet.gr/test5Gb.db',
        #'ftp://speedtest:speedtest@ftp.otenet.gr/test1Gb.db'
        ]

opdir = 'F:\AgodaTest\\devtests\\'
#dm = DownloadsProcessor(urls,opdir,'config\config.ini')
try:
        dm = DownloadsProcessor(urls,opdir)
        dm.download_resources()
except Exception as e:
        print(e)
#dm2 = DownloadsProcessor(urls,opdir,'C:\\Users\\Chetana\Dropbox\JHUNTING\Applications\Jan4Afterwards\Agoda\pydownloader\\resourcedownloader\\config\\config.ini')

#dm2.download_resources()
#print("Debug")
