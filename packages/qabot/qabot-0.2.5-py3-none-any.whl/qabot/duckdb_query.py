import duckdb


def run_sql_catch_error(conn, sql: str):
    # Remove any backtics from the string
    sql = sql.replace("`", "")

    # If there are multiple statements, only run the first one
    sql = sql.split(";")[0]

    try:

        output = conn.sql(sql)

        if output is None:
            rendered_output = "No output"
        else:
            try:
                rendered_data = '\n'.join(str(row) for row in output.fetchall())
                rendered_output = ','.join(output.columns) + '\n' + rendered_data
            except AttributeError:
                rendered_output = str(output)
        return rendered_output
    except duckdb.ProgrammingError as e:
        return str(e)
    except duckdb.Error as e:
        return str(e)
    # except Exception as e:
    #     return str(e)