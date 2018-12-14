import os
import subprocess

class SystemController:
    def __init__(self, linux_user, jupyter_name, port, ip='127.0.0.1'):
        """ Initializes the System controller class
        :type ip: Str
        """
        self.ip = ip
        self.linux_user = linux_user
        self.jupyter_name = jupyter_name
        self.port = port

        """ Passes the linux username to create a new user """
        os.system("adduser --disabled-password --force-badname --gecos \"\" {0}".format(self.linux_user))

    def init_files(self, data):
        """ Initializes all files and folders for the cert and jupyter
        :type data: Str
        """
        # Initializes folders and files
        self.init_cert()
        self.init_jupyter(data)
        self.run_jupyter()

    def run_jupyter(self):
        """ Runs jupyter nootebook with the specified name"""
        os.mkdir(self.jupyter_name)
        os.system("chmod 777 {0}".format(self.jupyter_name))
        os.chdir(self.jupyter_name)
        os.system("echo \"screen -d -m jupyter notebook && exit\" > run.sh && chmod 777 run.sh && echo DONE...")
        os.system("sudo -H -u {0} bash -c ./run.sh".format(self.linux_user))
        os.system("rm /home/{0}/certs/{0}/run.sh".format(self.jupyter_name))

    def init_cert(self):
        """ Initializes the cert folder and files """
        # Creates the directory for the cert
        dir = '/home/{0}'.format(self.linux_user)
        os.chdir(dir)
        os.mkdir('certs')
        os.chdir(os.path.join(dir, 'certs'))

        # Initializes the cert files
        self.init_cert_file()

    def init_cert_file(self):
        """ Generates certificate file for the cert """
        os.system('openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mykey.key -out mycert.pem -subj \"/CN=www.mydom.com/O=My Company Name LTD./C=US\"')

    def init_jupyter(self, data):
        """ Inializes Jupyter notebook setting files with the data
        :type data: Str
        """
        linux_user_path = "/home/{0}".format(self.linux_user)   
        os.system("cp -r /home/ubuntu/.jupyter {0}".format(linux_user_path))

        # Writes data to file
        path = '/home/{0}/.jupyter/jupyter_notebook_config.py'.format(self.linux_user)
        os.system("chmod 777 /home/{0}/.jupyter".format(self.linux_user))
        with open(path, "a") as file:
            file.write("\n{0}".format(data))