import qrcode
import os
from pathlib import Path

def get_user_input():
    # Available categories
    categories = ['VME', 'NIM-CAMAC', 'DET', 'PC', 'TARGET']
    
    # Get category
    while True:
        print("\nAvailable categories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        try:
            choice = int(input("\nSelect category number (1-5): "))
            if 1 <= choice <= len(categories):
                category = categories[choice-1]
                break
            else:
                print("Invalid choice. Please select a number between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get start number
    while True:
        try:
            start = int(input("\nEnter start number (default: 1): ") or "1")
            if start >= 1:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get end number
    while True:
        try:
            end = int(input(f"Enter end number (default: {start}): ") or str(start))
            if end >= start:
                break
            else:
                print(f"End number must be greater than or equal to {start}")
        except ValueError:
            print("Please enter a valid number.")
    
    return category, start, end

def main():
    print("QR Code Generator for BUPPIN System")
    print("===================================")
    
    # Get parameters from user
    category, start, end = get_user_input()
    
    # Base URL for the pages
    base_url = f"https://vdg.phys.sci.osaka-u.ac.jp/BUPPIN/{category}/"
    
    # Create directory path
    output_dir = Path(f"./IMG/{category}")
    
    # Create directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nGenerating QR codes for {category} ({start:03d}-{end:03d})...")
    
    # Loop to generate QR codes
    for i in range(start, end + 1):
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
        img_filename = output_dir / f"qrcode_{i:03}.png"
        img.save(img_filename)
        print(f"Created: {img_filename}")

    print(f"\nComplete! QR codes have been saved in {output_dir}")

if __name__ == "__main__":
    main()
