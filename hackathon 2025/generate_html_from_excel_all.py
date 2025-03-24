import pandas as pd
import os

# File paths
file_path = "excel_input/Updated_KEY_ORGANIZERS.xlsx"
photo_folder = "photo_output"
output_file = "html_output/all_teams.html"
log_file = "html_output/missing_profiles.log"

# Load Excel file
excel_data = pd.ExcelFile(file_path)
sheet_names = excel_data.sheet_names  # Get all sheet names

# Ensure output directories exist
output_dir = os.path.dirname(output_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Start HTML template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All Team Members</title>
    <style>
        .team-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
        }
        .team-member {
            width: 250px;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            background: #f9f9f9;
        }
        .team-member img {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            object-fit: cover;
        }
        .team-member h3 {
            margin: 10px 0 5px;
        }
        .team-member p {
            color: #555;
            margin: 5px 0;
        }
        .linkedin {
            text-decoration: none;
            color: #0e76a8;
            font-weight: bold;
        }
        .team-section {
            margin-bottom: 40px;
        }
        h2 {
            border-bottom: 2px solid #ccc;
            padding-bottom: 5px;
        }
    </style>
</head>
<body>
    <h1>All Team Members</h1>
"""

# Create or clear the log file
with open(log_file, "w", encoding="utf-8") as log:
    log.write("Missing Profile Photo & LinkedIn Profile Log\n")

# Process each sheet and generate HTML sections
for sheet in sheet_names:
    df = excel_data.parse(sheet)

    # 确保 Name, Email, Role 至少存在
    required_columns = {'Name', 'Email', 'Role'}
    if not required_columns.issubset(df.columns):
        print(f"Skipping sheet '{sheet}' due to missing essential columns.")
        continue

    # 如果 `Profile Photo` 或 `LinkedIn Profile_y` 不存在，添加空列
    if 'Profile Photo' not in df.columns:
        df['Profile Photo'] = ""
    if 'LinkedIn Profile_y' not in df.columns:
        df['LinkedIn Profile_y'] = ""

    html_template += f"<div class='team-section'><h2>{sheet} Team</h2><div class='team-container'>"
    
    for _, row in df.iterrows():
        name = row['Name']
        email = row['Email']
        role = row['Role']
        profile_photo = row['Profile Photo Y']
        linkedin_profile = row['LinkedIn Profile_y']

         # 第三个功能：如果 LinkedIn Profile 缺少 'https://'，则补全
        if linkedin_profile and str(linkedin_profile).lower() not in ["nan", "none", ""]:
            # 若不以 http:// 或 https:// 开头，就加上 https://
            if not (linkedin_profile.startswith("http://") or linkedin_profile.startswith("https://")):
                linkedin_profile = "https://" + linkedin_profile

        # 记录缺失信息到日志
        with open(log_file, "a", encoding="utf-8") as log:
            if not linkedin_profile or pd.isna(linkedin_profile) or linkedin_profile.lower() in ["nan", "none", ""]:
                log.write(f"{name}: {email};\n")

        # Extract email prefix for photo naming
        print(profile_photo)
        email_prefix = email.split('@')[0]
        

        # Construct relative photo path
        relative_photo_path = f"../photo_output/{sheet.replace(' ', '_')}/{email_prefix}.jpg"
        if profile_photo and str(profile_photo).lower()  in ["nan", "none", ""]:
            relative_photo_path = f"../photo_output/null.jpg"
        # 默认 LinkedIn 为空时不生成链接
        linkedin_html = f'<a class="linkedin" href="{linkedin_profile}" target="_blank">LinkedIn</a>' if linkedin_profile else ""

        html_template += f"""
        <div class="team-member">
            <img src="{relative_photo_path}" alt="{name}">
            <h3>{name}</h3>
            <p>{role}</p>
            {linkedin_html}
        </div>
        """
    
    html_template += "</div></div>"

html_template += """
</body>
</html>
"""

# Save the single HTML file containing all teams
with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_template)

print(f"✅ HTML file generated: {output_file}")
print(f"⚠️ Missing information log saved: {log_file}")
