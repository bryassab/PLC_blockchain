class Config:
    #llave privada sirve para manejar datos de sesion, envio de mensaje por flash
    SECRET_KEY = 'hrxkasd'

#configuracion de la base de datos para verificacion de usuario
class DevelopmentConfig(Config):
    DEBUG = True
    #puerto local a BD mysql
    MYSQL_HOST = "localhost"
    #Usuario mysql
    MYSQL_USER = "root"
    #contraseña mysql
    MYSQL_PASSWORD = "cc1233903743*"
    #nombre de la BD(base de datos)
    MYSQL_DB = "per"
    
config = {
    'development' : DevelopmentConfig
}