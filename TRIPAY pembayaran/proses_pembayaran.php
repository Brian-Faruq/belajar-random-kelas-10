<?php

// 1. Konfigurasi Kredensial TriPay Sandbox / Dev
$apiKey     = 'DEV-I2nRxqZX4WE3IwdGAaD4OxVivJMjpmVX28z5gEue';
$privateKey = 'C7CSX-ds62g-l2IXl-KqYbx-w5YcE';
$merchantCode = 'T24264';

// 2. Ambil data dari form POST
$nama   = $_POST['nama'] ?? '';
$email  = $_POST['email'] ?? '';
$hp     = $_POST['hp'] ?? '';
$method = $_POST['method'] ?? 'QRIS';

// Detail Produk & Harga
$harga = 50000;
$merchantRef = 'INV-' . time(); // Format Kode Transaksi Unik

// 3. Buat Signature TriPay
$signature = hash_hmac('sha256', $merchantCode . $merchantRef . $harga, $privateKey);

// 4. Data Payload request ke API TriPay
$data = [
    'method'         => $method,
    'merchant_ref'   => $merchantRef,
    'amount'         => $harga,
    'customer_name'  => $nama,
    'customer_email' => $email,
    'customer_phone' => $hp,
    'order_items'    => [
        [
            'sku'         => 'EBK-001',
            'name'        => 'E-Book Belajar Web Dev',
            'price'       => $harga,
            'quantity'    => 1
        ]
    ],
    'return_url'   => 'http://localhost/PHPBrian/phpk10/Belajar%20random/TRIPAY%20pembayaran/index.php',
    'expired_time' => (time() + (24 * 60 * 60)), // Expired dalam 24 jam
    'signature'    => $signature
];

// 5. Kirim Request menggunakan cURL ke Endpoint Sandbox TriPay
$curl = curl_init();

curl_setopt_array($curl, array(
    CURLOPT_FRESH_CONNECT  => true,
    CURLOPT_URL            => 'https://tripay.co.id/api-sandbox/transaction/create',
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HEADER         => false,
    CURLOPT_HTTPHEADER     => array(
        'Authorization: Bearer ' . $apiKey
    ),
    CURLOPT_FAILONERROR    => false,
    CURLOPT_POST           => true,
    CURLOPT_POSTFIELDS     => http_build_query($data),
    CURLOPT_IPRESOLVE      => CURL_IPRESOLVE_V4
));

$response = curl_exec($curl);
$error = curl_error($curl);
curl_close($curl);

if ($error) {
    die('cURL Error: ' . $error);
}

// 6. Decode Response JSON dari TriPay
$result = json_decode($response, true);

if (isset($result['success']) && $result['success'] == true) {
    // Jika berhasil, redirect pengguna ke halaman pembayaran resmi TriPay
    $checkoutUrl = $result['data']['checkout_url'];
    header("Location: " . $checkoutUrl);
    exit();
} else {
    // Jika gagal, tampilkan pesan error
    echo "<h3>Gagal membuat transaksi!</h3>";
    echo "<p>Pesan Error: " . ($result['message'] ?? 'Terjadi kesalahan') . "</p>";
    echo "<pre>";
    print_r($result);
    echo "</pre>";
}