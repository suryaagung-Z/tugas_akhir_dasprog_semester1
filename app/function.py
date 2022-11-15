from .connect_db import conn
from prettytable import PrettyTable

class MyFunction:
    def __init__(self):
        self.tableName = 'pendaftaran_bis'

    # Function Tampilkan semua data kedalam table
    def showTable(self):
        query  = f"SELECT * FROM {self.tableName}"
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()

        pt = PrettyTable()
        pt.align = "l"
        pt.field_names = ["No.", "Nama Penumpang", "Alamat", "No.Telp", "Tanggal Pemesanan"]
        
        no = 1
        for row in result:
            pt.add_row([no, row["nama_penumpang"], row["alamat"], row["no_telp"], row["tgl_pemesanan"]])
            no+=1
        print(f"{pt} \n")
    
    def getByRow(self, row):
        row    = int(row)-1
        query  = f"SELECT * FROM {self.tableName} LIMIT {row}, 1"

        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchone()

        return result

    # Function Tambah data
    def add(self, **vals):
        query = f"INSERT INTO {self.tableName} (nama_penumpang, alamat, no_telp, tgl_pemesanan) VALUES ('{vals['nama']}', '{vals['alamat']}', {vals['noTelp']}, '{vals['tglPesan']}')"

        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()

        if cursor.rowcount == 1:
            print("\nData Berhasil Ditambah!!!\n")
            self.showTable()
            self.nextstep()

    def delete(self, row):
        getRow = self.getByRow(row)
        queryDelete = f"DELETE FROM {self.tableName} WHERE id={getRow['id']}"

        cursor = conn.cursor()
        cursor.execute(queryDelete)
        conn.commit()

        if cursor.rowcount == 1:
            print("\nData Berhasil Dihapus!!!\n")
            self.showTable()
            self.nextstep()
            
    def update(self, row):
        getRow = self.getByRow(row)
        d = "skip"
        # for val in getRow:
        #     print(getRow[val], type(getRow[val]))
        
        nama     = input(f"Nama : {getRow['nama_penumpang']} -> ")
        alamat   = input(f"Alamat : {getRow['alamat']} -> ")
        noTelp   = input(f"No.Telp : {getRow['no_telp']} -> ")
        tglPesan = input(f"Tanggal Pesan : {getRow['tgl_pemesanan']} -> ")

        nama     = nama if (nama != d) else getRow['nama_penumpang']
        alamat   = alamat if (alamat != d) else getRow['alamat']
        noTelp   = int(noTelp) if (noTelp != d) else getRow['no_telp']
        tglPesan = tglPesan if (tglPesan != d) else getRow['tgl_pemesanan']

        # print(nama, alamat, noTelp, tglPesan)

        queryUpdate = f"UPDATE {self.tableName} SET nama_penumpang='{nama}', alamat='{alamat}', no_telp={noTelp}, tgl_pemesanan='{tglPesan}' WHERE id={getRow['id']}"

        # print(queryUpdate)

        cursor = conn.cursor()
        cursor.execute(queryUpdate)
        conn.commit()

        if cursor.rowcount == 1:
            print("\nData Berhasil Diperbarui!!!\n")
            self.showTable()
            self.nextstep()

    # Function step
    def nextstep(self):
        _next = input("Aksi => (TAMBAH | PERBARUI | HAPUS) : ").lower()
        if _next == "tambah":
            print("\n~~~~~~~~~~~~~TAMBAH DATA~~~~~~~~~~~~~\n")
            nama     = input("Nama : ").strip()
            alamat   = input("Alamat : ").strip()
            noTelp   = int(input("No.telp : ").strip())
            tglPesan = input("Tanggal Pemesanan : ").strip()

            self.add(nama=nama, alamat=alamat, noTelp=noTelp, tglPesan=tglPesan)
            print("\n")

        elif _next == "perbarui":
            print("\n~~~~~~~~~~~~~PERBARUI DATA~~~~~~~~~~~~~\n")
            rowNum = input("Masukan nomor : ")
            print("\nNOTE : masukan \"skip\" jika tidak ingin diperbarui\n")
            self.update(rowNum)
            print("\n")

        elif _next == "hapus":
            print("\n~~~~~~~~~~~~~HAPUS DATA~~~~~~~~~~~~~\n")
            rowNum = input("Masukan nomor : ")
            self.delete(rowNum)
            print("\n")