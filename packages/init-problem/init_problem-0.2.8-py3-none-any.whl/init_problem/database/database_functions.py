
import os
from sqlite3 import Error
import sqlite3
from ..tex.path_tex import path_chapter

def db_file(chapter, post_type, format_problem):
    chapter_path = path_chapter(chapter.lower(), post_type, format_problem)
    path_database = os.path.join(chapter_path, f'{post_type}_{format_problem.lower()}.db')
    return path_database


def create_connection(db_file):
    """ create a database connection to the SQLite database
        :param db_file: database file
        :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn



def createDatabase(chapter, post_type, format_problem):
    database = create_connection(db_file(chapter, post_type, format_problem))

    #cursor = database.cursor()

    try:
        database.execute(
            """ CREATE TABLE IF NOT EXISTS problem(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chapter TEXT NOT NULL,
                date TEXT,
            ); """
            )
    except:
        print('Error')


    database.close()


