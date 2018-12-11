import os

class SystemController:
    def __init__(self, linux_user, jupyter_name, ip='127.0.0.1'):
        """ Initializes the System controller class
        :type ip: Str
        """
        self.ip = ip
        self.linux_user = linux_user
        self.jupyter_name = jupyter_name

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
        os.chdir(self.jupyter_name)
        print(os.system('pwd'))
        os.system('screen -d -m jupyter notebook')

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
        # Create empty jupyter notebook config file
        os.system("jupyter notebook --generate-config")

        # Writes data to file
        with open('/home/{0}/.jupyter/jupyter_notebook_config.py'.format(self.linux_user), "a") as file:
            file.write("\n{0}".format(data))