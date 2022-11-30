import os
from .Database import Database
from prettytable import PrettyTable
from plyer import notification

class Core(Database):
    # Contructor
    def __init__(self):
        # Inisialisasi contructor parent class / Database
        super().__init__()
    
    # Awal mula program
    def start(self):
        self.showTable()
        self.nextstep()

    # Function langkah-langkah
    def nextstep(self):
        _next = input("| TAMBAH | PERBARUI | HAPUS | KELUAR | => ").lower()
        if _next == "tambah":
            self.add()
        elif _next == "perbarui":
            self.update()
        elif _next == "hapus":
            self.delete()
        elif _next == "keluar":
            # Bersihkan console
            os.system("cls")
            # Keluar program
            quit()
        else:
            self.nextstep()

    # Function Tampilkan Semua Data Kedalam Tabel
    def showTable(self):
        # Membuat tabel pendaftaran_bis jika tabel pendaftaran_bis tidak tersedia
        super().createTable()
        # Dapatkan semua data didalam tabel pendaftaran_bis
        result = super().getAll()

        pt = PrettyTable()
        pt.align = "l"
        pt.field_names = ["No.", "Nama Penumpang", "Alamat", "No.Telp", "Tanggal Pemesanan"]
        
        no = 1
        for row in result:
            # Memasukan semua data tabel pendaftaran_bis kedalam tabel
            pt.add_row([no, row["nama_penumpang"], row["alamat"], row["no_telp"], row["tgl_pemesanan"]])
            no+=1
        print(f"{pt} \n")

    # Function Tambah Data
    def add(self):
        self.heading("TAMBAH DATA")
        # Menerima input data dari pengguna
        nama     = input("Nama : ").strip()
        alamat   = input("Alamat : ").strip()
        noTelp   = input("No.telp : ").strip()
        tglPesan = input("Tanggal Pemesanan : ").strip()
        
        # Cek apakah terdapat data kosong, jika true maka gagalkan proses tambah data
        if ((nama=="") or (alamat=="") or (noTelp=="") or (tglPesan=="")):
            self.showNotif("Terdapat Data Kosong")
            self.start()
            return

        # Jalankan proses tambah data dengan memanggil method addData()
        result = super().addData(nama=nama, alamat=alamat, noTelp=noTelp, tglPesan=tglPesan)

        # Memeriksa apakah ada perubahan dari database
        if result.rowcount == 1:
            self.showNotif("Data Berhasil Ditambah")
            self.start()
        print("\n")
            
    # Function Perbarui Data
    def update(self):
        self.heading("PERBARUI")
        # Menerima input nomor baris yang ingin diperbarui
        rowNum = input("Masukan nomor : ")
        # Jika yang dimasukan kosong atau bukan angka maka hentikan proses perbarui
        if ((rowNum == "") or (rowNum.isnumeric() == False)):
            self.showNotif("Gagal : Data Tidak Ditemukan")
            self.start()
            return
        
        # Dapatkan data dari tabel berdasarkan baris yang diinginkan pengguna
        getRow = self.getByRow(rowNum)
        # Cek apakah data tersedia, jika tidak maka hentikan proses perbarui
        if getRow == None:
            self.showNotif("Gagal : Data Tidak Ditemukan")
            self.start()
            return

        self.message("CATATAN : \"ENTER\" jika tidak ingin diperbarui")
        
        # Menerima input data untuk diperbarui
        nama     = input(f"Nama          : {getRow['nama_penumpang']} -> ").strip()
        alamat   = input(f"Alamat        : {getRow['alamat']} -> ").strip()
        noTelp   = input(f"No.Telp       : {getRow['no_telp']} -> ").strip()
        tglPesan = input(f"Tanggal Pesan : {getRow['tgl_pemesanan']} -> ").strip()

        # Cek apakah data kosong semua, jika true maka hentikan proses perbarui
        if ((nama=="") and (alamat=="") and (noTelp=="") and (tglPesan=="")):
            self.showNotif("Tidak Ada Data Yang Diperbarui")
            self.start()
            return

        # Cek data baru apakah kosong, jika kosong maka timpa dengan data lama
        nama     = nama if (nama != "") else getRow['nama_penumpang']
        alamat   = alamat if (alamat != "") else getRow['alamat']
        noTelp   = int(noTelp) if (noTelp != "") else getRow['no_telp']
        tglPesan = tglPesan if (tglPesan != "") else getRow['tgl_pemesanan']

        # Jalankan proses perbarui data dengan memanggil updateData()
        result = super().updateData(id=getRow['id'], nama=nama, alamat=alamat, noTelp=noTelp, tglPesan=tglPesan)

        # Cek apakah ada perubahan dari database
        if result.rowcount == 1:
            self.showNotif("Data Berhasil Diperbarui")
            self.start()
        print("\n")

    # Function Hapus Data
    def delete(self):
        self.heading("HAPUS DATA")

        # Menerima input nomor baris yang ingin dihapus
        rowNum = input("Masukan nomor : ")
        # Jika yang dimasukan kosong atau bukan angka maka hentikan proses hapus
        if ((rowNum == "") or (rowNum.isnumeric() == False)):
            self.showNotif("Data Tidak Ditemukan")
            self.start()
            return
        
        # Jalankan proses hapus data dengan memanggil method deleteData()
        result = super().deleteData(rowNum)
        # Cek apakah data tersedia, jika tidak maka hentikan proses hapus
        if result == None:
            self.showNotif("Data Tidak Ditemukan")
            self.start()
            return

        # Cek apakah ada perubahan dari database
        if result.rowcount == 1:
            self.showNotif("Data Berhasil Dihapus")
            self.start()
        print("\n")


    # FITUR
    def heading(self, val):
        print(f"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~{val}~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    def message(self, val):
        print(f"\n{val}\n")

    def showNotif(self, message):
        notification.notify(
            title = "Informasi",
            message = message,
            timeout = 2
        )
    # END FITUR