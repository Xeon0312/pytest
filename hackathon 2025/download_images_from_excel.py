import pandas as pd
import os
import requests
from http.cookiejar import MozillaCookieJar
from urllib.parse import urlparse, parse_qs
import re

def convert_drive_link_to_direct(url: str) -> str:
    """
    将常见的 Google Drive 链接转换为可直接下载的地址。
    目前支持:
      1) https://drive.google.com/file/d/<FILE_ID>/view?usp=sharing
      2) https://drive.google.com/open?id=<FILE_ID>
    转换后生成:
      https://drive.google.com/uc?export=download&id=<FILE_ID>

    如果链接不符合这两种模式，则直接返回原链接。
    """
    if not isinstance(url, str):
        return url
    
    pattern_file_d = r"https://drive\.google\.com/file/d/([^/]+)/view"
    match = re.search(pattern_file_d, url)
    if match:
        file_id = match.group(1)
        direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        return direct_url

    parsed = urlparse(url)
    if "drive.google.com" in parsed.netloc and parsed.path == "/open":
        query_params = parse_qs(parsed.query)
        if "id" in query_params:
            file_id = query_params["id"][0]
            direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            return direct_url

    return url

def download_images_from_excel(file_path, output_folder, cookie_file):
    # 加载 Excel
    excel_data = pd.ExcelFile(file_path)
    sheet_names = excel_data.sheet_names

    # 加载 cookies
    cookie_jar = MozillaCookieJar(cookie_file)
    cookie_jar.load(ignore_discard=True, ignore_expires=True)

    for sheet in sheet_names:
        print(f"Processing sheet: {sheet}")
        df = excel_data.parse(sheet)

        # 确保必要列存在
        if 'Email' not in df.columns:
            print(f"Skipping sheet '{sheet}' due to missing 'Email' column.")
            continue

        # 识别 profile photo 列名
        profile_photo_col = 'Profile Photo'
        if 'Profile Photo.1' in df.columns:
            profile_photo_col = 'Profile Photo.1'

        if profile_photo_col not in df.columns:
            print(f"Skipping sheet '{sheet}' due to missing profile photo column.")
            continue

        # 创建输出文件夹
        sheet_folder = os.path.join(output_folder, sheet.replace(" ", "_"))
        if not os.path.exists(sheet_folder):
            os.makedirs(sheet_folder)

        for _, row in df.iterrows():
            image_url = row[profile_photo_col]
            image_url = convert_drive_link_to_direct(image_url)
            email = row['Email']

            # 只有image_url和email都非空才进行下载
            if pd.notna(image_url) and pd.notna(email):
                try:
                    file_extension = os.path.splitext(urlparse(image_url).path)[-1]
                    if not file_extension or file_extension == "":
                        file_extension = ".jpg"
                    file_name = f"{email.split('@')[0]}{file_extension}"
                    file_path = os.path.join(sheet_folder, file_name)

                    # 在下载前先判断是否已经存在同名文件
                    if os.path.exists(file_path):
                        print(f"Skipping download of {file_name} (file already exists in {sheet_folder}).")
                        continue

                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                      "(KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"
                    }
                    response = requests.get(image_url, cookies=cookie_jar, headers=headers, stream=True)

                    if response.status_code == 200:
                        with open(file_path, 'wb') as file:
                            for chunk in response.iter_content(1024):
                                file.write(chunk)
                        print(f"Downloaded: {file_name} in {sheet_folder}")
                    else:
                        print(f"Failed to download {image_url} - Status Code: {response.status_code}")
                except Exception as e:
                    print(f"Error downloading {image_url}: {e}")

if __name__ == "__main__":
    # 示例用法
    input_file = r"D:\pytest\excel_input\Updated_KEY_ORGANIZERS.xlsx"  
    output_folder = r"D:\pytest\photo_input" 
    cookie_file = r"D:\cookies.txt"

    download_images_from_excel(input_file, output_folder, cookie_file)
