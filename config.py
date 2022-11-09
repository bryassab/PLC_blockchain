class Config:
    #llave privada sirve para manejar datos de sesion, envio de mensaje por flash
    SECRET_KEY = 'hrxkasd'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "cc1233903743*"
    MYSQL_DB = "per"
    
config = {
    'development' : DevelopmentConfig
}