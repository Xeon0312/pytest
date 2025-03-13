import pandas as pd
import os

# ------ 新增：将字符串转为简单 Title Case 的函数 ------
def to_title_case(s: str) -> str:
    """
    将给定字符串转成简单的标题格式（每个单词首字母大写，其余小写）。
    例如：
      "TEAM HR" -> "Team Hr"
      "it development team" -> "It Development Team"
    """
    return ' '.join(word.capitalize() for word in s.split())

# Paths
excel_file_path = "excel_input/Updated_KEY_ORGANIZERS.xlsx"
ts_output_file = "ts_output/teams.ts"
log_file = "ts_output/missing_profiles.log"

# Ensure output directories exist
os.makedirs(os.path.dirname(ts_output_file), exist_ok=True)

# Load Excel file
excel_data = pd.ExcelFile(excel_file_path)
sheet_names = excel_data.sheet_names  # Get all team names

# Create or clear the log file
with open(log_file, "w", encoding="utf-8") as log:
    log.write("Missing Profile Photo & LinkedIn Profile Log\n")

# Prepare the TypeScript file content
ts_content = "const teams = [\n"

for sheet in sheet_names:
    # 将工作表名称转为简单 Title Case，仅在 teamName 与 teamDescription 中使用
    title_sheet = to_title_case(sheet)

    df = excel_data.parse(sheet)

    # Ensure required columns exist
    required_columns = {'Name', 'Email', 'Role'}
    if not required_columns.issubset(df.columns):
        print(f"Skipping sheet '{sheet}' due to missing essential columns.")
        continue

    # If 'Profile Photo' or 'LinkedIn Profile' is missing, add empty columns
    if 'Profile Photo' not in df.columns:
        df['Profile Photo'] = ""
    if 'LinkedIn Profile_y' not in df.columns:
        df['LinkedIn Profile_y'] = ""

    # Add team information
    ts_content += (
        f"  {{\n"
        f"    teamName: \"{title_sheet}\",\n"
        f"    teamDescription: \"This is {title_sheet}'s description.\",\n"
        f"    members: [\n"
    )

    for _, row in df.iterrows():
        name = row['Name']
        email = row['Email']
        role = row['Role']
        profile_photo = row['Profile Photo']
        linkedin_profile = row['LinkedIn Profile_y']

        # Extract email prefix for naming images
        email_prefix = email.split('@')[0]

        # **保留原本的路径**（使用原始 sheet 名替换空格为下划线，且不做大小写调整）
        image_src = f"../photo_output/{sheet.replace(' ', '_')}/{email_prefix}.jpg"

        # Record missing information in the log
        with open(log_file, "a", encoding="utf-8") as log:
            if not profile_photo or pd.isna(profile_photo) or profile_photo.lower() in ["nan", "none", ""]:
                log.write(f"Missing Profile Photo: {name} ({email})\n")
            if not linkedin_profile or pd.isna(linkedin_profile) or linkedin_profile.lower() in ["nan", "none", ""]:
                log.write(f"Missing LinkedIn Profile: {name} ({email})\n")

        # Format LinkedIn profile link
        social_links = ""
        if linkedin_profile and not pd.isna(linkedin_profile) and linkedin_profile.lower() not in ["nan", "none", ""]:
            social_links = f"        {{ icon: FaLinkedin, url: \"{linkedin_profile}\" }}"

        # Append member data
        ts_content += f"""      {{
        imageSrc: "{image_src}",
        name: "{name}",
        description: "{role}",
        socialLinks: [
{social_links}
        ]
      }},\n"""

    # Close team section
    ts_content += "    ]\n  },\n"

# Close the TypeScript array
ts_content += "];\n\nexport default teams;\n"

# Write to the TypeScript file
with open(ts_output_file, "w", encoding="utf-8") as file:
    file.write(ts_content)

print(f"✅ TypeScript file generated: {ts_output_file}")
print(f"⚠️ Missing information log saved: {log_file}")
