import os
import tkinter.messagebox as popup
from .Database import Database
from prettytable import PrettyTable
from plyer import notification

class Core(Database):
    # Contructor
    def __init__(self):
        super().__init__()
    
    def start(self):
        self.showTable()
        self.nextstep()

    # Function step
    def nextstep(self):
        _next = input("| TAMBAH | PERBARUI | HAPUS | KELUAR | => ").lower()
        if _next == "tambah":
            self.add()
        elif _next == "perbarui":
            self.update()
        elif _next == "hapus":
            self.delete()
        elif _next == "bersihkan":
            os.system("cls")
            self.start()
        elif _next == "keluar":
            os.system("cls")
            quit()
        else:
            self.nextstep()

    # Function Tampilkan Semua Data Kedalam Tabel
    def showTable(self):
        super().createTable()
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
        self.heading("TAMBAH DATA")
        nama     = input("Nama              : ").strip()
        alamat   = input("Alamat            : ").strip()
        noTelp   = input("No.telp           : ").strip()
        tglPesan = input("Tanggal Pemesanan : ").strip()
        
        if (nama=="" or alamat=="" or noTelp=="" or tglPesan==""):
            self.showNotif("Terdapat Data Yang Kosong")
            self.start()
            return

        result = super().addData(nama=nama, alamat=alamat, noTelp=noTelp, tglPesan=tglPesan)

        if result.rowcount == 1:
            self.showNotif("Data Berhasil Ditambah")
            self.start()
        print("\n")
            
    # Function Perbarui Data
    def update(self):
        self.heading("PERBARUI")
        rowNum = input("Masukan nomor : ")
        if ((rowNum == "") or (rowNum.isnumeric() == False)):
            self.showNotif("Data Tidak Ditemukan")
            self.start()
            return

        getRow = self.getByRow(rowNum)
        if getRow == None:
            self.showNotif("Data Tidak Ditemukan")
            self.start()
            return

        self.message("CATATAN : \"ENTER\" jika tidak ingin diperbarui")
        
        nama     = input(f"Nama          : {getRow['nama_penumpang']} -> ")
        alamat   = input(f"Alamat        : {getRow['alamat']} -> ")
        noTelp   = input(f"No.Telp       : {getRow['no_telp']} -> ")
        tglPesan = input(f"Tanggal Pesan : {getRow['tgl_pemesanan']} -> ")

        if (nama=="" and alamat=="" and noTelp=="" and tglPesan==""):
            self.showNotif("Tidak Ada Yang Diperbarui")
            self.start()
            return

        nama     = nama if (nama != "") else getRow['nama_penumpang']
        alamat   = alamat if (alamat != "") else getRow['alamat']
        noTelp   = int(noTelp) if (noTelp != "") else getRow['no_telp']
        tglPesan = tglPesan if (tglPesan != "") else getRow['tgl_pemesanan']

        result = super().updateData(id=getRow['id'], nama=nama, alamat=alamat, noTelp=noTelp, tglPesan=tglPesan)

        if result.rowcount == 1:
            self.showNotif("Data Berhasil Diperbarui")
            self.start()
        print("\n")

    # Function Hapus Data
    def delete(self):
        self.heading("HAPUS DATA")
        rowNum = input("Masukan nomor : ")
        if ((rowNum == "") or (rowNum.isnumeric() == False)):
            self.showNotif("Data Tidak Ditemukan")
            self.start()
            return
        
        result = super().deleteData(rowNum)
        if result == None:
            self.showNotif("Data Tidak Ditemukan")
            self.start()
            return

        if result.rowcount == 1:
            self.showNotif("Data Berhasil Dihapus")
            self.start()
        print("\n")

    def heading(self, val):
        print(f"\n~~~~~~~~~~~~~~~~~~~~~~{val}~~~~~~~~~~~~~~~~~~~~~~\n")

    def message(self, val):
        print(f"\n{val}\n")

    def showNotif(self, message):
        notification.notify(
            title = "Informasi",
            message = message,
            timeout = 2
        )