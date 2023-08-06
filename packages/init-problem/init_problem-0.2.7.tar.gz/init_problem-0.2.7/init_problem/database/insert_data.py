import click
import os
import time
import sqlite3

from ..tex.path_tex import path_mechanics
from ..tex.path_tex import path_electrodynamics
from .database_functions import db_file
from .database_functions import create_connection
from .database_functions import createDatabase

time_date = int(time.strftime("%H%M%S%d%m%Y"))

def insertData(chapter, post_type, format_problem):
    database = create_connection(db_file(chapter, post_type, format_problem))
    cursor = database.cursor()

    try:
        execute_statement = f'INSERT INTO problem(chapter, date) VALUES("{chapter}", "{time_date}");'
        cursor.execute(execute_statement)
        database.commit()
        database.close()

    except:
        print('Error')





