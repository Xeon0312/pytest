import pandas as pd
import requests
import io  # 用于读取 CSV 数据

def download_google_sheet(sheet_id: str, sheet_gid: str):
    """
    从 Google Sheets 下载 CSV 数据。
    """
    export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={sheet_gid}"
    response = requests.get(export_url)
    if response.status_code == 200:
        return pd.read_csv(io.StringIO(response.text))  # 修正点
    else:
        raise Exception(f"❌ 无法下载 Google Sheets ({response.status_code})")

def clean_and_convert_google_sheet(sheet_id: str, sheet_gid: str, output_file: str):
    """
    下载 Google Sheet 数据，清理并转换为 Excel 文件。
    """
    staff_list_df = download_google_sheet(sheet_id, sheet_gid)

    valid_teams = {
        "LEADERS", "OPERATIONS TEAM", "FINANCE TEAM", "PARTNER EXPERIENCE TEAM",
        "STUDENT SUCCESS TEAM", "REGISTRATION TEAM","IT DEVELOPMENT TEAM", "MARKETING & COMMUNICATIONS TEAM",
        "CREATIVES TEAM", "CONSULTANTS", "ISSUE MANAGEMENT TEAM"
    }

    sheets_data = {}
    current_team = None
    ignore_section = False

    # 遍历数据，按团队拆分
    for _, row in staff_list_df.iterrows():
        first_col_value = str(row.iloc[0]).strip()

        # 忽略 TEAM STRUCTURE RECOMMENDATION 及以下内容
        if first_col_value == "TEAM STRUCTURE RECOMMENDATION":
            ignore_section = True
            break

        # 识别新的团队标题（如果是有效团队，则切换 current_team）
        # print(first_col_value)
        if first_col_value in valid_teams:
            current_team = first_col_value
            sheets_data[current_team] = []
            continue

        # 记录团队成员数据（跳过表头 "Name"）
        if current_team and row.iloc[0] != "Name":
            person_data = row.iloc[:6].tolist()

            # 如果 Name 和 Email 为空，则跳过
            if pd.isna(person_data[0]) and pd.isna(person_data[1]):
                continue

            # 新增的列数据（可以在实际数据源中调整获取方式）
            person_data += [None, None]  # 添加 "Profile Photo" 和 "LinkedIn Profile" 列，暂时设置为空值

            sheets_data[current_team].append(person_data)

    # 移除无人员数据的团队（如 ISSUE MANAGEMENT TEAM）
    sheets_data = {team: data for team, data in sheets_data.items() if data}

    # 生成 Excel 文件
    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        for team, data in sheets_data.items():
            df = pd.DataFrame(data, columns=["Name", "Email", "Team", "Role", "Course Background", "Role Description", "Profile Photo", "LinkedIn Profile"])
            df.to_excel(writer, sheet_name=team[:31], index=False)

    print(f"✅ 转换完成，文件已保存至 {output_file}")

# 示例调用
google_sheet_id = "1WCAsZj_nxYFwO01Zzaxko2WBjWXT7ekJ"
sheet_gid = "496782016"
output_file_path = "excel_input\KEY ORGANIZERS.xlsx"

clean_and_convert_google_sheet(google_sheet_id, sheet_gid, output_file_path)
