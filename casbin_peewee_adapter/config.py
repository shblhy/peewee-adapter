import peewee as pw
import yaml
import os
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'settings.yml')
with open(config_path, 'r') as f:
    settings = yaml.load(f)
DATABASES = settings['db']
DEFAULT_MYSQL_DATABAEE = pw.MySQLDatabase(
    host=DATABASES['host'],
    user=DATABASES['user'],
    passwd=DATABASES['password'],
    database=DATABASES['dbname'],
    charset='utf8',
    port=DATABASES['port']
)