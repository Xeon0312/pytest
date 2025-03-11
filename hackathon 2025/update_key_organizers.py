import pandas as pd
from http.cookiejar import MozillaCookieJar
from urllib.parse import urlparse

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
        
        if 'Name' in key_organizers_df.columns:
            key_organizers_df.drop_duplicates(subset=['Name'], keep='first', inplace=True)
        
        updated_sheets[sheet] = key_organizers_df
    
    with pd.ExcelWriter(updated_file_path, engine='xlsxwriter') as writer:
        for sheet_name, df in updated_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"Updated KEY ORGANIZERS file saved at: {updated_file_path}")

hackathon_file_path = r"D:\pytest\excel_input\Hackathon 2025 Organizing Team Member Profile Submission.xlsx"
key_organizers_file_path = r"D:\pytest\excel_input\KEY ORGANIZERS.xlsx"
updated_file_path = r"D:\pytest\excel_input\Updated_KEY_ORGANIZERS.xlsx"

update_key_organizers(hackathon_file_path, key_organizers_file_path, updated_file_path)


