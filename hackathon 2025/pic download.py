import pandas as pd
import os
import requests
from http.cookiejar import MozillaCookieJar
from urllib.parse import urlparse

def download_images_from_excel(file_path, sheet_name, output_folder, cookie_file):
    # Load the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Load cookies from file
    cookie_jar = MozillaCookieJar(cookie_file)
    cookie_jar.load(ignore_discard=True, ignore_expires=True)
    
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for _, row in df.iterrows():
        image_url = row['Profile Photo']
        email = row['Email']
        
        if pd.notna(image_url) and pd.notna(email):
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"
                }
                response = requests.get(image_url, cookies=cookie_jar, headers=headers, stream=True)
                if response.status_code == 200:
                    file_extension = os.path.splitext(urlparse(image_url).path)[-1] or ".jpg"
                    file_name = f"{email.replace('@', '_').replace('.', '_')}{file_extension}"
                    file_path = os.path.join(output_folder, file_name)
                    
                    with open(file_path, 'wb') as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)
                    print(f"Downloaded: {file_name}")
                else:
                    print(f"Failed to download {image_url} - Status Code: {response.status_code}")
            except Exception as e:
                print(f"Error downloading {image_url}: {e}")


input  = r"D:\pytest\hackathon 2025\KEY ORGANIZERS.xlsx"  
output = r"D:\pytest\tt2" 
cookies = r"D:\pytest\hackathon 2025\cookies.txt"
download_images_from_excel(input, "IT TEAM", output,cookies)