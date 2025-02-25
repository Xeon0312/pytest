import pandas as pd
import os
import requests
from http.cookiejar import MozillaCookieJar
from urllib.parse import urlparse

def download_images_from_excel(file_path, output_folder, cookie_file):
    # Load the Excel file
    excel_data = pd.ExcelFile(file_path)
    sheet_names = excel_data.sheet_names  # Get all sheet names
    
    # Load cookies from file
    cookie_jar = MozillaCookieJar(cookie_file)
    cookie_jar.load(ignore_discard=True, ignore_expires=True)
    
    for sheet in sheet_names:
        print(f"Processing sheet: {sheet}")
        df = excel_data.parse(sheet)
        
        # Ensure the sheet contains the necessary columns
        if 'Profile Photo' not in df.columns or 'Email' not in df.columns:
            print(f"Skipping sheet '{sheet}' due to missing columns.")
            continue
        
        # Create a folder for each sheet
        sheet_folder = os.path.join(output_folder, sheet.replace(" ", "_"))
        if not os.path.exists(sheet_folder):
            os.makedirs(sheet_folder)
        
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
                        file_name = f"{email.split('@')[0]}{file_extension}"
                        file_path = os.path.join(sheet_folder, file_name)
                        
                        with open(file_path, 'wb') as file:
                            for chunk in response.iter_content(1024):
                                file.write(chunk)
                        print(f"Downloaded: {file_name} in {sheet_folder}")
                    else:
                        print(f"Failed to download {image_url} - Status Code: {response.status_code}")
                except Exception as e:
                    print(f"Error downloading {image_url}: {e}")

def update_key_organizers(hackathon_file_path, key_organizers_file_path, updated_file_path):
    # Load the Hackathon file
    hackathon_data = pd.ExcelFile(hackathon_file_path)
    hackathon_df = hackathon_data.parse(hackathon_data.sheet_names[0])
    
    # Load the Key Organizers file
    key_organizers_data = pd.ExcelFile(key_organizers_file_path)
    updated_sheets = {}
    
    # Ensure email is used as a lookup value
    if 'Email' not in hackathon_df.columns:
        print("Email column missing in Hackathon file.")
        return
    
    for sheet in key_organizers_data.sheet_names:
        key_organizers_df = key_organizers_data.parse(sheet)
        
        if 'Profile Photo' in key_organizers_df.columns and 'LinkedIn Profile' in key_organizers_df.columns and 'Email' in key_organizers_df.columns:
            key_organizers_df = key_organizers_df.merge(hackathon_df[['Email', 'Upload Your Profile Photo', 'LinkedIn Profile']], on='Email', how='left')
            key_organizers_df.rename(columns={'Upload Your Profile Photo': 'Profile Photo'}, inplace=True)
        
        updated_sheets[sheet] = key_organizers_df
    
    with pd.ExcelWriter(updated_file_path, engine='xlsxwriter') as writer:
        for sheet_name, df in updated_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"Updated KEY ORGANIZERS file saved at: {updated_file_path}")

hackathon_file_path = r"D:\pytest\excel_input\Hackathon 2025 Organizing Team Member Profile Submission.xlsx"
key_organizers_file_path = r"D:\pytest\excel_input\KEY ORGANIZERS.xlsx"
updated_file_path = r"D:\pytest\excel_input\Updated_KEY_ORGANIZERS.xlsx"

update_key_organizers(hackathon_file_path, key_organizers_file_path, updated_file_path)


