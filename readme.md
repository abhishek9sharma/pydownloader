A set of scripts to download files using various protocols.

##Steps to run
1. You need to have *Python 3* installed on your system ( the code has been verified on *Python 3.6.3* )
2. Using command line go navigate to the folder *pydownloader*( make sure this folder contains the files *README.md* and folder *resourcedownloader*)

2. Install/Configure a virtual Environment as follows from the command line (if you want you may skip but it may cause dependency issues on your system) (If configured already go to Step 3)
    a. Installation 
        -- Linux : python3 -m pip install --user virtualenv (*sudo* rights may be required)
        -- windows     : pip install --user virtualenv

    b.Configuration
        i. Create
            -- windows      : python -m virtualenv testassignment
            -- Linux        : python3 -m virtualenv env (*sudo* rights may be required)
        
        ii.  Activate 
            -- windows      : .\testassignment\Scripts\activate
            -- Linux        :  source testassignment/bin/activate (*sudo* rights may be required)
        
        iii. Install dependencies
            --windows : pip install -r requirements.txt
            --Linux   : pip install -r requirements.txt (*sudo* rights may be required)
        
 3. Activate environment (*testassignment* is the environment name)
        -- windows      : .\testassignment\Scripts\activate
        -- Linux        :  source testassignment/bin/activate (*sudo* rights may be required)
 
 4. Create a file *resourceurls.txt* in *pydownloader* folder, which should contain the links which you want to download. Currently protocols *http, ftp, sftp* are supported. Each link should be in different lines. Example shown below
    ```
    ftp://speedtest:speedtest@ftp.otenet.gr/test1Mb.db
    http://speedtest.ftp.otenet.gr/files/test1Mb.db
    sftp://demo-user:demo-user@demo.wftpserver.com:2222/download/manual_en.pdf
    ```


5. From command prompt run the following command
    -- Windows : python run resourceurls.txt destfolderpath
    -- Linux   : python run resourceurls.txt destfolderpath (*sudo* rights may be required)






