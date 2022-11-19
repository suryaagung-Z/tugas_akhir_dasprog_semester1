import mysql.connector as mcon

class Database:
    def __init__(self):
        self.tableName = 'pendaftaran_bis'
        try:
            config = {
                "host": "localhost",
                "username": "suryaagung",
                "password": "sury44gung123",
                "database": "tpl_tugasakhir"
            }
            self._conn = mcon.connect(**config)
        except mcon.Error as err:
            self._conn = f"Terdapat error : {err}"

    def execute(self, **params):
        cursor = self._conn.cursor(dictionary=params['dict'])
        cursor.execute(params['query'])
        return cursor

    def fetchAll(self, cursor):
        return cursor.fetchall()

    def fetchOne(self, cursor):
        return cursor.fetchone()
    
    def commit(self):
        self._conn.commit()

    def getAll(self):
        query  = f"SELECT * FROM {self.tableName}"
        exe = self.execute(query=query, dict=True)
        return self.fetchAll(exe)

    def getByRow(self, row):
        row    = int(row)-1
        query  = f"SELECT * FROM {self.tableName} LIMIT {row}, 1"
        exe = self.execute(query=query, dict=True)
        return self.fetchOne(exe)

    def addData(self, **vals):
        query = (
            f"INSERT INTO {self.tableName}"
            f"(nama_penumpang, alamat, no_telp, tgl_pemesanan)"
            f"VALUES"
            f"('{vals['nama']}', '{vals['alamat']}', {vals['noTelp']}, '{vals['tglPesan']}')"
        )

        exe = self.execute(query=query, dict=False)
        self.commit()
        return exe

    def deleteData(self, row):
        getRow = self.getByRow(row)
        if getRow == None:
            return
            
        queryDelete = f"DELETE FROM {self.tableName} WHERE id={getRow['id']}"

        exe = self.execute(query=queryDelete, dict=False)
        self.commit()
        return exe

    def updateData(self, **vals):
        queryUpdate = f"UPDATE {self.tableName} SET nama_penumpang='{vals['nama']}', alamat='{vals['alamat']}', no_telp={vals['noTelp']}, tgl_pemesanan='{vals['tglPesan']}' WHERE id={vals['id']}"

        exe = self.execute(query=queryUpdate, dict=False)
        self.commit()
        return exe