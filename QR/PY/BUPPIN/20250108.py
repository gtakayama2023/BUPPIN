import qrcode
import os
from pathlib import Path
import subprocess

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
    categories = ['VME', 'NIM-CAMAC', 'DET', 'PC', 'TARGET']
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

    while True:
        try:
            start = int(input("\nEnter start number (default: 1): ") or "1")
            if start >= 1:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")

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
    """Get Google Form URLs in bulk input."""
    print("\nEnter Google Form URLs in bulk (one per line, matching the numbers in order). Finish input with an empty line:")
    urls = []
    while True:
        url = input().strip()
        if url == "":
            break  # 空行が入力されるまで待機
        urls.append(url)
        
    # URLの数が足りない場合の補完処理
    if len(urls) < (end - start + 1):
        print(f"\nWarning: Only {len(urls)} URLs provided for range {start}-{end}. Missing URLs will be skipped.")

    # 開始番号から順番に辞書を作成
    form_urls = {start + i: url for i, url in enumerate(urls) if url}
    return form_urls

def sync_to_server():
    """Sync HTML directory to server using rsync."""
    print("\nSyncing files to server...")
    try:
        cmd = ['rsync', '-arve', 'ssh', '--progress', './HTML/', 
               'IV_web:/System/Volumes/Data/Sites/Default/BUPPIN/']
        process = subprocess.run(cmd, text=True, check=True, capture_output=True)
        print("Sync completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during sync: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error during sync: {e}")
        return False

def main():
    print("QR Code and Redirect Page Generator for BUPPIN System")
    print("==================================================")
    category, start, end = get_user_input()
    form_urls = get_form_urls(start, end)
    qr_dir = Path(f"./IMG/{category}")
    html_dir = Path(f"./HTML/{category}")
    qr_dir.mkdir(parents=True, exist_ok=True)
    html_dir.mkdir(parents=True, exist_ok=True)
    base_url = f"https://vdg.phys.sci.osaka-u.ac.jp/BUPPIN/{category}/"
    
    print(f"\nGenerating files for {category} ({start:03d}-{end:03d})...")
    for i in range(start, end + 1):
        url = f"{base_url}{i:03}.html"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        qr_filename = qr_dir / f"qrcode_{i:03}.png"
        img.save(qr_filename)
        print(f"Created QR code: {qr_filename}")

        if i in form_urls:
            html_code = generate_html(form_urls[i])
            html_filename = html_dir / f"{i:03}.html"
            with open(html_filename, "w") as f:
                f.write(html_code)
            print(f"Created redirect page: {html_filename}")

    print(f"\nFile generation complete!")
    sync_success = sync_to_server()
    if sync_success:
        print("\nAll operations completed successfully!")
    else:
        print("\nFile generation completed, but sync to server failed.")

if __name__ == "__main__":
    main()
