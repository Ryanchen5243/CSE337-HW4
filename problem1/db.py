import sys
import os
import sqlite3
from contextlib import closing

from objects import Category
from objects import Movie

conn = None

def connect():
    global conn
    if not conn:
        if sys.platform == "win32":
            print("Windows")
            DB_FILE = "movies.sqlite"
        else:
            print("Linux")
            HOME = os.environ["HOME"]
            DB_FILE = "movies.sqlite"

        ''' to remove later'''
        DB_FILE = ":memory:"
        ''' end to remove later'''
        
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

def initialize_database():
    with closing(conn.cursor()) as c:
        # create category table
        c.execute('''
            CREATE TABLE IF NOT EXISTS Category(
                categoryID INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        c.execute('''
            INSERT INTO Category (name) VALUES (?)
        ''', ('Animation',))
        c.execute('''
            INSERT INTO Category (name) VALUES (?)
        ''', ('Comedy',))
        c.execute('''
            INSERT INTO Category (name) VALUES (?)
        ''', ('History',))

        # create Movie table
        c.execute('''
            CREATE TABLE IF NOT EXISTS Movie(
                movieID INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                year INTEGER NOT NULL,
                minutes INTEGER NOT NULL,
                categoryID INTEGER NOT NULL
            )
        ''')
        
        c.execute('''INSERT INTO Movie (name, year, minutes, categoryID) VALUES (?,?,?,?)''',
                  ("John doe",2012,87,1))
        c.execute('''INSERT INTO Movie (name, year, minutes, categoryID) VALUES (?,?,?,?)''',
            ("The epic story of my hero",1999,120,2))
        c.execute('''INSERT INTO Movie (name, year, minutes, categoryID) VALUES (?,?,?,?)''',
            ("Who even knows? 199",2000,63,1))
        c.execute('''INSERT INTO Movie (name, year, minutes, categoryID) VALUES (?,?,?,?)''',
            ("Good ending.",1989,68,3))

        conn.commit()

def close():
    if conn:
        conn.close()

def make_category(row):
    return Category(row["categoryID"], row["categoryName"])

def make_movie(row):
    return Movie(row["movieID"], row["name"], row["year"], row["minutes"],
            make_category(row))

def get_categories():
    query = '''SELECT categoryID, name as categoryName
               FROM Category'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

        '''testing ehrere'''
        print(results)

    categories = []
    for row in results:
        categories.append(make_category(row))
    return categories

def get_category(category_id):
    query = '''SELECT categoryID, name AS categoryName
               FROM Category WHERE categoryID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (category_id,))
        row = c.fetchone()
        if row:
            return make_category(row)
        else:
            return None

def get_movies_by_category(category_id):
    query = '''SELECT movieID, Movie.name, year, minutes,
                      Movie.categoryID as categoryID,
                      Category.name as categoryName
               FROM Movie JOIN Category
                      ON Movie.categoryID = Category.categoryID
               WHERE Movie.categoryID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (category_id,))
        results = c.fetchall()

    movies = []
    for row in results:
        movies.append(make_movie(row))
    return movies

def get_movies_by_year(year):
    query = '''SELECT movieID, Movie.name, year, minutes,
                      Movie.categoryID as categoryID,
                      Category.name as categoryName
               FROM Movie JOIN Category
                      ON Movie.categoryID = Category.categoryID
               WHERE year = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (year,))
        results = c.fetchall()

    movies = []
    for row in results:
        movies.append(make_movie(row))
    return movies

def add_movie(movie):
    sql = '''INSERT INTO Movie (categoryID, name, year, minutes) 
             VALUES (?, ?, ?, ?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (movie.category.id, movie.name, movie.year,
                        movie.minutes))
        conn.commit()

def delete_movie(movie_id):
    sql = '''DELETE FROM Movie WHERE movieID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (movie_id,))
        test = conn.commit()
        print("Test", test)

def get_movie(movie_id):
    with closing(conn.cursor()) as c:
        c.execute('''
            SELECT Movie.*, Category.name as categoryName 
            FROM Movie INNER JOIN Category ON Movie.categoryID
                  = Category.categoryID
            WHERE movieID = ?
        ''', (movie_id,))
        result = c.fetchone()
        return make_movie(result) if result else None

def get_movies_by_minutes():
    '''
    5. In the db module, add a get_movies_by_minutes() function that gets a list of Movie
objects that have a running time that's less than the number of minutes passed to it as
an argument.
    '''
    pass