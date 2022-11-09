import bcrypt 
password= "uwu"
password = password.encode()
asa = bcrypt.gensalt()
hash = bcrypt.hashpw(password, asa)
print(hash)
password_hash= '$2b$12$Np.oHcbiyXqyLcJs5srxuepWwxMXQ2JFIPyXzNlKhSqaeFx.v470m'
password_hash = password_hash.encode()
print(bcrypt.checkpw(password, password_hash))