import configparser
from os.path import abspath, dirname, join
from os import environ

conf_file_name = 'conf'

path_of_conf = join(abspath(dirname(__file__)), '', conf_file_name)
print(f"Using: {path_of_conf} for config.")

config = configparser.RawConfigParser()

config.read(path_of_conf, encoding='utf-8')

try:
    ENVIRONMENT = environ['ENVIRONMENT']
except Exception as e:
    print(f"No environment variable 'ENVIRONMENT'. Error {e}")
    ENVIRONMENT = 'dev'
