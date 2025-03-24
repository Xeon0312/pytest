import pdfkit

# 先生成 .html 文件（逻辑不变）
pdfkit.from_file("html_output\all_teams.html", "html_output\all_teams.html")
