import pandas as pd
import os

# File paths
file_path = "excel_input/Updated_KEY_ORGANIZERS.xlsx"
photo_folder = "photo_input"
output_file = "html_output/all_teams_compare.html"

# Load Excel file
excel_data = pd.ExcelFile(file_path)
sheet_names = excel_data.sheet_names  # Get all sheet names

# Ensure output directory exists
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

# Process each sheet and generate HTML sections
for sheet in sheet_names:
    df = excel_data.parse(sheet)

    # Ensure required columns exist
    if not {'Name', 'Email', 'Role', 'Profile Photo', 'LinkedIn Profile_y'}.issubset(df.columns):
        print(f"Skipping sheet '{sheet}' due to missing columns.")
        continue

    html_template += f"<div class='team-section'><h2>{sheet} Team</h2><div class='team-container'>"
    
    for _, row in df.iterrows():
        if pd.notna(row['Email']) and pd.notna(row['LinkedIn Profile_y']):
            # Extract email prefix
            email_prefix = row['Email'].split('@')[0]

            # Construct relative photo path
            relative_photo_path = f"../photo_input/{sheet.replace(' ', '_')}/{email_prefix}.jpg"

            html_template += f"""
            <div class="team-member">
                <img src="{relative_photo_path}" alt="{row['Name']}">
                <h3>{row['Name']}</h3>
                <p>{row['Role']}</p>
                <a class="linkedin" href="{row['LinkedIn Profile_y']}" target="_blank">LinkedIn</a>
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

print(f"HTML file generated: {output_file}")
