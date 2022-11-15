import mysql.connector as mcon

try:
    config = {
        "host": "localhost",
        "username": "suryaagung",
        "password": "sury44gung123",
        "database": "tpl_tugasakhir"
    }
    conn = mcon.connect(**config)
except mcon.Error as err:
    conn = f"Terdapat error : {err}"