import pandas as pd
import os

# 路径配置
excel_file_path = "excel_input/Updated_KEY_ORGANIZERS.xlsx"
ts_output_file = "ts_output/teams.ts"
log_file = "ts_output/missing_profiles.log"

# 确保输出目录存在
os.makedirs(os.path.dirname(ts_output_file), exist_ok=True)

# 读取 Excel 文件
excel_data = pd.ExcelFile(excel_file_path)
sheet_names = excel_data.sheet_names

# 清空并创建缺失信息日志文件
with open(log_file, "w", encoding="utf-8") as log:
    log.write("Missing Profile Photo & LinkedIn Profile Log\n")

# 用于存放所有表的成员信息
all_members = {}

for sheet in sheet_names:
    df = excel_data.parse(sheet)

    # 确保必要的列存在
    required_columns = {'Name', 'Email', 'Role'}
    if not required_columns.issubset(df.columns):
        print(f"Skipping sheet '{sheet}' due to missing essential columns.")
        continue

    # 若缺失 'Profile Photo' 或 'LinkedIn Profile_y' 则补空列
    if 'Profile Photo' not in df.columns:
        df['Profile Photo'] = ""
    if 'LinkedIn Profile_y' not in df.columns:
        df['LinkedIn Profile_y'] = ""

    # 存放当前 sheet 的成员列表
    members_list = []

    for _, row in df.iterrows():
        name = row['Name']
        email = row['Email']
        role = row['Role']
        profile_photo = row['Profile Photo']
        linkedin_profile = row['LinkedIn Profile_y']

        # 记录缺失信息到日志
        with open(log_file, "a", encoding="utf-8") as log:
            if not profile_photo or pd.isna(profile_photo) or profile_photo.lower() in ["nan", "none", ""]:
                log.write(f"Missing Profile Photo: {name} ({email})\n")
            if not linkedin_profile or pd.isna(linkedin_profile) or linkedin_profile.lower() in ["nan", "none", ""]:
                log.write(f"Missing LinkedIn Profile: {name} ({email})\n")

        # 提取 email 前缀，用于生成图片名称
        email_prefix = email.split('@')[0]
        image_src = f"/images/our_teams/{sheet.replace(' ', '_')}/{email_prefix}.jpg"

        members_list.append({
            "name": name,
            "email": email,
            "role": role,
            "imageSrc": image_src,
            "profilePhotoMissing": (not profile_photo or pd.isna(profile_photo) or profile_photo.lower() in ["nan", "none", ""]),
            "linkedin": linkedin_profile
        })

    all_members[sheet] = members_list

# ---------- 合并 "Registration Team" 到 "Student Success" ------------
if "Registration Team" in all_members and "Student Success" in all_members:
    all_members["Student Success"].extend(all_members["Registration Team"])
    del all_members["Registration Team"]

# ---------- 对团队名称进行 Title Case，并对 "IT" 特殊处理 ----------
def to_title_case_team_name(s: str) -> str:
    words = s.split()
    words = [w.capitalize() for w in words]
    if len(words) >= 1 and words[0].lower() == "it":
        words[0] = "IT"
    return " ".join(words)

# ---------- 生成最终的 TypeScript 文件 ----------
ts_content = "export const teams = [\n"

for sheet in sheet_names:
    if sheet not in all_members:
        continue

    title_sheet = to_title_case_team_name(sheet)
    ts_content += f"  {{\n"
    ts_content += f"    teamName: \"{title_sheet}\",\n"
    ts_content += f"    teamDescription: \"This is {title_sheet}'s description.\",\n"
    ts_content += f"    members: [\n"

    for member in all_members[sheet]:
        name = member["name"]
        role = member["role"]
        linkedin_profile = member["linkedin"]

        # 若 LinkedIn 为空，则不输出 socialLinks
        social_links = ""
        if linkedin_profile and str(linkedin_profile).lower() not in ["nan", "none", ""]:
            social_links = f"        {{ icon: FaLinkedin, url: \"{linkedin_profile}\" }}"

        
        image_src_line = f"imageSrc: \"{member['imageSrc']}\","

        ts_content += f"""      {{
        {image_src_line}
        name: "{name}",
        description: "{role}",
        socialLinks: [
{social_links}
        ]
      }},\n"""

    ts_content += f"    ]\n  }},\n"

ts_content += "];\n"

# 写出到目标文件
with open(ts_output_file, "w", encoding="utf-8") as file:
    file.write(ts_content)

print(f"✅ TypeScript file generated: {ts_output_file}")
print(f"⚠️ Missing information log saved: {log_file}")
