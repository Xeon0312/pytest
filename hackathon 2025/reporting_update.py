import psycopg2
import pandas as pd

def fetch_hackathon_team_data(host, port, database, user, password) -> pd.DataFrame:

    # 1) 连接数据库
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=database,
        user=user,
        password=password
    )
    cursor = conn.cursor()

    # 2) 构造查询语句
    #    关联表：participants, team_members, teams, school, seneca_programs
    query = """
        SELECT 
            p.participant_id AS "MemberNumber",
            p.firstname      AS "FirstName",
            p.lastname       AS "LastName",
            p.email          AS "Email",
            t.team_name      AS "TeamName",
            tm.is_leader     AS "IsLeader",
            p.shirt_size     AS "ShirtSize",
            p.from_seneca    AS "FromSeneca",
            p.is_alumni      AS "IsAlumni",
            s.school_name    AS "SchoolName",
            p.graduation_year   AS "GraduationYear",
            p.semester_number   AS "SemesterNumber",
            p.study_field_name  AS "StudyFieldName",
            sp.program_name     AS "ProgramName",
            p.degree_type       AS "DegreeType",
            p.is_solo           AS "IsSolo",
            p.having_team       AS "HavingTeam",
            p.registered_at     AS "RegisterTime(UTC0)"
        FROM public.participants p
        LEFT JOIN public.team_members tm
            ON tm.participant_id = p.participant_id
        LEFT JOIN public.teams t
            ON t.team_id = tm.team_id
        LEFT JOIN public.school s
            ON s.school_id = p.school_id
        LEFT JOIN public.seneca_programs sp
            ON sp.program_id = p.seneca_program_id
        ORDER BY p.participant_id;
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # 3) 关闭连接
    cursor.close()
    conn.close()
    
    # 4) 将结果转为 DataFrame
    columns = [
        "MemberNumber",
        "FirstName",
        "LastName",
        "Email",
        "TeamName",
        "IsLeader",
        "ShirtSize",
        "FromSeneca",
        "IsAlumni",
        "SchoolName",
        "GraduationYear",
        "SemesterNumber",
        "StudyFieldName",
        "ProgramName",
        "DegreeType",
        "IsSolo",
        "HavingTeam",
        "RegisterTime(UTC0)"
    ]
    df = pd.DataFrame(rows, columns=columns)
    
    # 如果 "RegisterTime(UTC0)" 等时间列带 tzinfo，需要去掉，否则写入Excel时 openpyxl会报错
    if not df.empty and pd.api.types.is_datetime64tz_dtype(df["RegisterTime(UTC0)"]):
        df["RegisterTime(UTC0)"] = df["RegisterTime(UTC0)"].dt.tz_localize(None)
    
    return df

def main():
    # 数据库连接参数
    host = "aws-0-us-west-1.pooler.supabase.com"
    port = 6543
    database = "postgres"
    user = "postgres.autrxhhiehfmziavcryj"
    password = "sSaGxHLwJtoiEcYY"
    
    # 获取 DataFrame
    df = fetch_hackathon_team_data(host, port, database, user, password)
    
    # 查看前几行
    print(df.head())
    
    # 写入 Excel
    excel_path = "excel_input\Hackathon 2025 teams.xlsx"
    df.to_excel(excel_path, index=False)
    print(f"已将 18 列团队信息写入 {excel_path}")
    
if __name__ == "__main__":
    main()




