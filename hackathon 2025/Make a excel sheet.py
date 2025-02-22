import pandas as pd

# Define the columns for the workbook
columns = [
    "Task Description",
    "Assigned to",
    "Notes",
    "Status",
    "Planned Start Date",
    "Planned Finish Date",
    "Estimated Duration"
]

# Define the departments
departments = [
    "Operations Team",
    "Finance Team",
    "Partner Experience Team",
    "Success Team",
    "IT Development Team",
    "Marketing & Communications Team",
    "Creatives Team"
]

# Create an Excel writer
file_path = "D:\pytest\Organizational_Tasks.xlsx"
with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
    for department in departments:
        # Create an empty DataFrame for each department
        df = pd.DataFrame(columns=columns)
        df.to_excel(writer, sheet_name=department, index=False)

# Provide the download link
file_path