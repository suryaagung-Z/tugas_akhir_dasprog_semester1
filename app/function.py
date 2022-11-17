from .Database import Database
from prettytable import PrettyTable
import os

class MyFunction(Database):
    # Contructor
    def __init__(self):
        Database.__init__(self)

    def start(self):
        self.showTable()
        self.nextstep()

    # Function Tampilkan Semua Data Kedalam Tabel
    def showTable(self):
        result = super().getAll()

        pt = PrettyTable()
        pt.align = "l"
        pt.field_names = ["No.", "Nama Penumpang", "Alamat", "No.Telp", "Tanggal Pemesanan"]
        
        no = 1
        for row in result:
            pt.add_row([no, row["nama_penumpang"], row["alamat"], row["no_telp"], row["tgl_pemesanan"]])
            no+=1
        print(f"{pt} \n")

    # Function Tambah Data
    def add(self):
        print("\n~~~~~~~~~~~~~~~~~~~~~~TAMBAH DATA~~~~~~~~~~~~~~~~~~~~~~\n")
        nama     = input("Nama : ").strip()
        alamat   = input("Alamat : ").strip()
        noTelp   = input("No.telp : ").strip()
        tglPesan = input("Tanggal Pemesanan : ").strip()

        result = super().addData(nama=nama, alamat=alamat, noTelp=noTelp, tglPesan=tglPesan)

        if result.rowcount == 1:
            print("\nData Berhasil Ditambah!!!\n")
            self.start()
        print("\n")
            
    # Function Perbarui Data
    def update(self):
        print("\n~~~~~~~~~~~~~~~~~~~~~~PERBARUI DATA~~~~~~~~~~~~~~~~~~~~~~\n")
        rowNum = input("Masukan nomor : ")
        print("\nNOTE : \"ENTER\" jika tidak ingin diperbarui\n")

        getRow = self.getByRow(rowNum)
        
        nama     = input(f"Nama : {getRow['nama_penumpang']} -> ")
        alamat   = input(f"Alamat : {getRow['alamat']} -> ")
        noTelp   = input(f"No.Telp : {getRow['no_telp']} -> ")
        tglPesan = input(f"Tanggal Pesan : {getRow['tgl_pemesanan']} -> ")

        d = ""
        nama     = nama if (nama != d) else getRow['nama_penumpang']
        alamat   = alamat if (alamat != d) else getRow['alamat']
        noTelp   = int(noTelp) if (noTelp != d) else getRow['no_telp']
        tglPesan = tglPesan if (tglPesan != d) else getRow['tgl_pemesanan']

        result = super().updateData(id=getRow['id'], nama=nama, alamat=alamat, noTelp=noTelp, tglPesan=tglPesan)

        if result.rowcount == 1:
            print("\nData Berhasil Diperbarui!!!\n")
            self.start()
        print("\n")

    # Function Hapus Data
    def delete(self):
        print("\n~~~~~~~~~~~~~~~~~~~~~~HAPUS DATA~~~~~~~~~~~~~~~~~~~~~~\n")
        rowNum = input("Masukan nomor : ")
        
        result = super().deleteData(rowNum)

        if result.rowcount == 1:
            print("\nData Berhasil Dihapus!!!\n")
            self.start()
        print("\n")

    # Function step
    def nextstep(self):
        _next = input("Aksi => (TAMBAH | PERBARUI | HAPUS | KELUAR) : ").lower()
        if _next == "tambah":
            self.add()
        elif _next == "perbarui":
            self.update()
        elif _next == "hapus":
            self.delete()
        elif _next == "keluar":
            os.system("cls")
            quit()
        elif _next == "":
            self.nextstep()