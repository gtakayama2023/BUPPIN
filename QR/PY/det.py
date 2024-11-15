# generate_qrcodes.py

import qrcode

# Base URL for the pages
base_url = "https://vdg.phys.sci.osaka-u.ac.jp/BUPPIN/NIM-CAMAC/"

# Loop to generate QR codes for 019 to 029
for i in range(47,48):
    # Construct the full URL
    url = f"{base_url}{i:03}.html"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image
    img_filename = f"qrcode_{i:03}.png"
    img.save(img_filename)
    print(f"QR code saved as {img_filename}")

