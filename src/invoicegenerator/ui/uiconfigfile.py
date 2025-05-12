from configparser import ConfigParser

class Config:
    def __init__(self,config_file="./src/invoicegenerator/ui/uiconfigfile.ini"):
        self.config=ConfigParser()
        self.config.read(config_file)
        print("Config file loaded successfully.")
        
    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE")
    
    