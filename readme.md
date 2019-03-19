A set of scripts to download files using various protocols.

## Steps to run
### All command may require sudo/admin privileges
1. You need to have *Python 3* installed on your system ( the code has been verified on *Python 3.6.3* )
2. Using command line go navigate to the folder *pydownloader*( make sure this folder contains the files *README.md* and folder *resourcedownloader*)

3. Install/Configure a virtual Environment as follows from the command line (if you want you may skip but it may cause dependency issues on your system) (If configured already go to Step 4)
    
    a. Installation 
        -- Linux : python3 -m pip install --user virtualenv
        -- windows     : pip install --user virtualenv

    b. Configuration
        
        i. Create
            -- windows      : python -m virtualenv testassignment
            -- Linux        : python3 -m virtualenv env 
        
        ii.  Activate 
            -- windows      : .\testassignment\Scripts\activate
            -- Linux        :  source testassignment/bin/activate 
        
        iii. Install dependencies
            --windows : pip install -r requirements.txt
            --Linux   : pip install -r requirements.txt 
        
 4. Activate environment (*testassignment* is the environment name)
        ```
        -- windows      : .\testassignment\Scripts\activate
        -- Linux        :  source testassignment/bin/activate 
        ```
5. Create a file *resourceurls.txt* in *pydownloader* folder, which should contain the links which you want to download. Currently protocols *http, ftp, sftp* are supported. Each link should be in different lines. Example shown below
    ```
    ftp://speedtest:speedtest@ftp.otenet.gr/test1Mb.db
    http://speedtest.ftp.otenet.gr/files/test1Mb.db
    sftp://demo-user:demo-user@demo.wftpserver.com:2222/download/manual_en.pdf
    ```


5. From command prompt run the following command
    -- Windows : python run resourceurls.txt destfolderpath
    -- Linux   : python run resourceurls.txt destfolderpath 






