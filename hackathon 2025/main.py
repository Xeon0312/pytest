import os
import subprocess

# 定义脚本路径（假设所有脚本都放在当前目录）
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

# 设置文件路径
EXCEL_INPUT_DIR = os.path.join(SCRIPTS_DIR, "excel_input")
PHOTO_INPUT_DIR = os.path.join(SCRIPTS_DIR, "photo_input")
PHOTO_OUTPUT_DIR = os.path.join(SCRIPTS_DIR, "photo_output")
HTML_OUTPUT_DIR = os.path.join(SCRIPTS_DIR, "html_output")

# 确保必要的目录存在
os.makedirs(EXCEL_INPUT_DIR, exist_ok=True)
os.makedirs(PHOTO_INPUT_DIR, exist_ok=True)
os.makedirs(PHOTO_OUTPUT_DIR, exist_ok=True)
os.makedirs(HTML_OUTPUT_DIR, exist_ok=True)

# Google Sheets 参数
GOOGLE_SHEET_ID = "1WCAsZj_nxYFwO01Zzaxko2WBjWXT7ekJ"
SHEET_GID = "496782016"
KEY_ORGANIZERS_FILE = os.path.join(EXCEL_INPUT_DIR, "KEY ORGANIZERS.xlsx")
UPDATED_KEY_ORGANIZERS_FILE = os.path.join(EXCEL_INPUT_DIR, "Updated_KEY_ORGANIZERS.xlsx")
COOKIE_FILE = os.path.join(SCRIPTS_DIR, "cookies.txt")

def run_script(script_name, *args):
    """ 运行指定 Python 脚本 """
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    command = ["python", script_path] + list(args)
    
    print(f"🚀 正在执行: {script_name} ...")
    result = subprocess.run(command, capture_output=True, text=True)
    
    # 打印输出结果
    if result.returncode == 0:
        print(f"✅ {script_name} 执行成功!\n")
    else:
        print(f"❌ {script_name} 运行失败:\n{result.stderr}\n")

# **1️⃣ 获取最新 Master File**
run_script("get_latest_master_file.py", GOOGLE_SHEET_ID, SHEET_GID, KEY_ORGANIZERS_FILE)

# **2️⃣ 更新 KEY ORGANIZERS**
run_script("update_key_organizers.py", KEY_ORGANIZERS_FILE, UPDATED_KEY_ORGANIZERS_FILE)

# **3️⃣ 下载人员照片**
run_script("download_images_from_excel.py", UPDATED_KEY_ORGANIZERS_FILE, PHOTO_INPUT_DIR, COOKIE_FILE)

# **4️⃣ 裁剪人脸**
run_script("crop_face.py", PHOTO_INPUT_DIR, PHOTO_OUTPUT_DIR)

# **5️⃣ 生成 HTML 页面**
run_script("generate_html_from_excel_all.py")

print("🎉 所有任务完成!")
