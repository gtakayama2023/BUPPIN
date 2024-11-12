import qrcode
import os
from pathlib import Path

def generate_html(input_url):
    """Generate HTML redirect code."""
    html_code = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0;url={input_url}">
<title>Redirecting...</title>
</head>
<body>
<script type="text/javascript">
    window.location.href = "{input_url}"
</script>
<p>If you are not redirected automatically, follow this <a href='{input_url}'>link to the form</a>.</p>
</body>
</html>"""
    return html_code

def get_user_input():
    """Get user input for category and number range."""
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

def get_form_urls(start, end):
    """Get Google Form URLs for each number."""
    form_urls = {}
    print("\nEnter Google Form URLs for each number (press Enter to skip):")
    for i in range(start, end + 1):
        url = input(f"Form URL for {i:03d}: ").strip()
        if url:  # Only store non-empty URLs
            form_urls[i] = url
    return form_urls

def main():
    print("QR Code and Redirect Page Generator for BUPPIN System")
    print("==================================================")
    
    # Get parameters from user
    category, start, end = get_user_input()
    
    # Get Google Form URLs
    print("\nGoogle Form's URL?")
    form_urls = get_form_urls(start, end)
    
    # Create base directories
    qr_dir = Path(f"./IMG/{category}")
    html_dir = Path(f"./HTML/{category}")
    
    # Create directories if they don't exist
    qr_dir.mkdir(parents=True, exist_ok=True)
    html_dir.mkdir(parents=True, exist_ok=True)
    
    # Base URL for the QR codes
    base_url = f"https://vdg.phys.sci.osaka-u.ac.jp/BUPPIN/{category}/"
    
    print(f"\nGenerating files for {category} ({start:03d}-{end:03d})...")
    
    # Loop to generate QR codes and HTML files
    for i in range(start, end + 1):
        # Generate QR code
        url = f"{base_url}{i:03}.html"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Save QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        qr_filename = qr_dir / f"qrcode_{i:03}.png"
        img.save(qr_filename)
        print(f"Created QR code: {qr_filename}")
        
        # Generate and save HTML redirect file if form URL exists
        if i in form_urls:
            html_code = generate_html(form_urls[i])
            html_filename = html_dir / f"{i:03}.html"
            with open(html_filename, "w") as f:
                f.write(html_code)
            print(f"Created redirect page: {html_filename}")

    print(f"\nComplete!")
    print(f"QR codes have been saved in {qr_dir}")
    print(f"HTML redirect pages have been saved in {html_dir}")

if __name__ == "__main__":
    main()