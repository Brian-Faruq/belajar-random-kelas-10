<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Landing Page - Belajar TriPay</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f6f9;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
        }
        .container {
            background-color: #fff;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            max-width: 400px;
            width: 100%;
        }
        h2 { text-align: center; color: #333; }
        .product-card {
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            background-color: #fafafa;
        }
        .product-title { font-weight: bold; font-size: 18px; }
        .price { color: #27ae60; font-size: 20px; font-weight: bold; margin-top: 5px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-size: 14px; font-weight: bold; }
        input[type="text"], input[type="email"], select {
            width: 100%;
            padding: 10px;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            width: 100%;
            background-color: #007bff;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover { background-color: #0056b3; }
    </style>
</head>
<body>

<div class="container">
    <h2>E-Shop Sederhana</h2>
    
    <!-- Detail Produk -->
    <div class="product-card">
        <div class="product-title">E-Book Belajar Web Dev</div>
        <div class="price">Rp 50.000</div>
    </div>

    <!-- Form Checkout -->
    <form action="proses_pembayaran.php" method="POST">
        <div class="form-group">
            <label for="nama">Nama Pembeli:</label>
            <input type="text" id="nama" name="nama" placeholder="Masukkan nama kamu" required>
        </div>

        <div class="form-group">
            <label for="email">Email Pembeli:</label>
            <input type="email" id="email" name="email" placeholder="contoh@gmail.com" required>
        </div>

        <div class="form-group">
            <label for="hp">Nomor WhatsApp/HP:</label>
            <input type="text" id="hp" name="hp" placeholder="08123456789" required>
        </div>

        <div class="form-group">
            <label for="method">Metode Pembayaran:</label>
            <select name="method" id="method" required>
                <option value="QRIS">QRIS (Semua E-Wallet/Bank)</option>
                <option value="BRIVA">BRI Virtual Account</option>
                <option value="BNIVA">BNI Virtual Account</option>
                <option value="BCAVA">BCA Virtual Account</option>
                <option value="ALFAMART">Alfamart</option>
            </select>
        </div>

        <button type="submit">Beli & Bayar Sekarang</button>
    </form>
</div>

</body>
</html>