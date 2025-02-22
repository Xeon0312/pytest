import pandas as pd

def generate_html_from_excel(file_path, output_file):
    # Load the Excel file
    df = pd.read_excel(file_path, sheet_name='IT TEAM')
    
    # HTML Template
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Team Members</title>
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
        </style>
    </head>
    <body>
        <div class="team-container">
    """
    
    for _, row in df.iterrows():
        if pd.notna(row['Profile Photo']) and pd.notna(row['LinkedIn Profile']):
            html_template += f"""
            <div class="team-member">
                <img src="{row['Profile Photo']}" alt="{row['Name']}">
                <h3>{row['Name']}</h3>
                <p>{row['Role']}</p>
                <a class="linkedin" href="{row['LinkedIn Profile']}" target="_blank">LinkedIn</a>
            </div>
            """
    
    html_template += """
        </div>
    </body>
    </html>
    """
    
    # Save the HTML file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_template)
    
    print(f"HTML file generated: {output_file}")


# Example usage
input_file = r"D:\Users\caobo\Downloads\KEY ORGANIZERS.xlsx"

generate_html_from_excel(input_file, r"D:\Users\caobo\Downloads\team_members.html")