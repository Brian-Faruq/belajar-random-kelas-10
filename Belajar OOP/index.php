<!-- Belajar OOP (Object-Oriented Programming) -->

<!-- 1. Class & Object -->
<!-- Penjelasan: Bayangkan sebuah Class itu seperti denah rumah, sedangkan Objek adalah rumah asli 
yang dibangun berdasarkan denah tersebut. Dari satu denah yang sama, kita bisa membangun banyak rumah (objek). -->
<?php
// 1. Membuat Class
class Mobil {
    // Property (atribut/data)
    public $merk;
    public $warna;

    // Method (fungsi/perilaku)
    public function infoMobil() {
        return "Mobil ini bermerk $merk dengan warna $warna.";
    }
}

// 2. Membuat Objek (Instisiasi)
$mobil1 = new Mobil();
$mobil1->merk = "Toyota";
$mobil1->warna = "Hitam";

// Memanggil method dari objek
echo $mobil1->infoMobil(); 
// Output: Mobil ini bermerk Toyota dengan warna Hitam.
?>

<!-- 2. Property & Method -->
<!-- Penjelasan: Property adalah variabel yang dideklarasikan di dalam sebuah class. Fungsinya untuk menyimpan data atau 
informasi dari objek (contohnya: $merk, $warna, $kecepatan).
Method adalah fungsi yang dideklarasikan di dalam sebuah class. Fungsinya untuk melakukan tindakan atau perilaku yang 
bisa dikerjakan oleh objek (contohnya: jalan(), rem(), infoMobil()). -->
<?php
class Mobil {
    // Property
    public $merk;
    public $warna;
    public $kecepatan = 0; // Property dengan nilai default

    // Method untuk menampilkan info
    public function infoMobil() {
        return "Mobil $this->merk berwarna $this->warna sedang berjalan.";
    }

    // Method untuk menambah kecepatan
    public function gas() {
        $this->kecepatan += 20;
        return "Kecepatan bertambah! Sekarang: " . $this->kecepatan . " km/jam.<br>";
    }
}

// Membuat objek
$mobil1 = new Mobil();
$mobil1->merk = "Honda";
$mobil1->warna = "Merah";

// Memanggil method
echo $mobil1->infoMobil() . "<br>";
echo $mobil1->gas(); // Memanggil method gas()
echo $mobil1->gas(); // Memanggil method gas() lagi
?>

<!-- 3. Constructor -->
<!-- Penjelasan: Constructor adalah sebuah method khusus yang otomatis dijalankan (dipanggil) saat sebuah objek pertama kali 
dibuat dari class. -->
<!-- Ciri2: Menggunakan nama method khusus yaitu __construct()
Otomatis berjalan begitu perintah new NamaClass() dipanggil. -->
<?php
class Mobil {
    public $merk;
    public $warna;
    public $kecepatan;

    // Ini adalah Constructor
    public function __construct($merkMobil, $warnaMobil, $kecepatanMobil) {
        $this->merk = $merkMobil;
        $this->warna = $warnaMobil;
        $this->kecepatan = $kecepatanMobil;
    }

    public function infoMobil() {
        return "Mobil $this->merk berwarna $this->warna melaju dengan kecepatan $this->kecepatan km/jam.<br>";
    }
}

// Saat membuat objek, kita langsung kirim data ke constructor di dalam tanda kurung ( )
$mobil1 = new Mobil("Toyota", "Hitam", 60);
$mobil2 = new Mobil("Honda", "Merah", 80);

// Memanggil method
echo $mobil1->infoMobil();
echo $mobil2->infoMobil();
?>

<!-- 4. Encapsulation -->
<!-- Penjelasan: Pembatasan akses ke properti atau method menggunakan modifier 
(public, private, protected) agar data di dalam class lebih aman dan tidak bisa diubah sembarangan dari luar. -->
<?php
class Mobil {
    private $kecepatan = 0; // Hanya bisa diakses dari dalam class ini saja

    public function setKecepatan($nilai) { // Setter untuk mengubah nilai private
        if ($nilai > 0) { $this->kecepatan = $nilai; }
    }

    public function getKecepatan() { // Getter untuk mengambil nilai private
        return $this->kecepatan;
    }
}

$mobil1 = new Mobil();
$mobil1->setKecepatan(100); // Mengubah data lewat method
echo $mobil1->getKecepatan(); // Output: 100
?>

<!-- 5. Inheritance -->
<!-- Penjelasan: Pewarisan sifat di mana class anak dapat mewarisi properti dan method dari class induk agar kode bisa digunakan kembali tanpa menulis ulang. -->
<?php
class Kendaraan { // Class Induk
    public $merk;
    public function info() { return "Ini adalah kendaraan merk $this->merk."; }
}

class Mobil extends Kendaraan { // Class Anak mewarisi Kendaraan
    public $pintu;
}

$mobil1 = new Mobil();
$mobil1->merk = "Toyota";
echo $mobil1->info(); // Output: Ini adalah kendaraan merk Toyota.
?>

<!-- 6. Polymorphism -->
<!-- Penjelasan: Kemampuan class anak untuk mengubah atau menyesuaikan ulang method yang diwarisi dari class induk agar sesuai dengan kebutuhannya sendiri. -->
<?php
class Kendaraan {
    public function suara() { return "Suara kendaraan..."; }
}

class Mobil extends Kendaraan {
    // Override method suara() dari class induk
    public function suara() { return "Brum brum!"; }
}

$mobil1 = new Mobil();
echo $mobil1->suara(); // Output: Brum brum!
?>

<!-- 7. Abstraction -->
<!-- Penjelasan: Menyembunyikan detail rumit dan memaksa class anak untuk mengimplementasikan method tertentu menggunakan abstract class atau interface. -->
<?php
abstract class Kendaraan {
    // Method abstract wajib di-override oleh class anak
    abstract public function nyalakanMesin();
}

class Motor extends Kendaraan {
    public function nyalakanMesin() {
        return "Mesin motor dinyalakan dengan electric starter.";
    }
}

$motor1 = new Motor();
echo $motor1->nyalakanMesin(); // Output: Mesin motor dinyalakan dengan electric starter.
?>