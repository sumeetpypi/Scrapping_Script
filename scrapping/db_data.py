import os
import sqlite3
import uuid
import time


def read_file():
    file_path = os.path.dirname(__file__)
    file_ = os.path.join(file_path, "database", "books_new.db")
    return file_


def read_file_():
    file_path = os.path.dirname(__file__)
    file_ = os.path.join(file_path, "database", "books.db")
    return file_


def create_db():
    data = read_file()
    conn = sqlite3.connect(data)
    cur = conn.cursor()
    print uuid.uuid1()
    create_db_query = "create table books_db(id varchar(300), title varchar(300), image varchar(500), pages varchar(100), size varchar(100), language varchar(100), download_url varchar(400) not null primary key, categories varchar(100), description varchar(100), authors varchar(100), year varchar(100), time_stamp datetime default current_timestamp);"
    cur.execute(create_db_query)


def download_section():
    data_dict = list()
    data = read_file_()
    conn = sqlite3.connect(data)
    cur = conn.cursor()
    database_exits = True

    if not os.path.exists(data):
        database_exits = False

    # year_ = "{}-year".format(title)
    try:
        if database_exits:
            select_query = "select * from books_db"
            get_data = cur.execute(select_query)
            fetch_data = get_data.fetchall()
            print len(fetch_data)
            for x in fetch_data:
                print  x
                title = x[1]
                image = x[2]
                pages = x[3]
                size = x[4]
                language = x[5]
                download = x[6]
                categories = x[7]
                description = x[8]
                authors = x[9]
                years = x[10]

                time.sleep(1)
                insert(title=title, image=image, pages=pages, size=size, language=language, download_url=download, categories=categories,
                       description=description, authors=authors, year=years)
                # data_dict.append(x)

        # return data_dict

    except Exception as e:
        pass


def insert(title=None, image=None, pages=None, size=None, language=None, download_url=None, categories=None,
           description=None, authors=None, year=None):
    try:
        id = uuid.uuid1()
        data = read_file()
        conn = sqlite3.connect(data)
        cur = conn.cursor()
        select_query = """insert into books_db(title,image,pages, size, language, download_url,categories, description, authors, year) values (?, ?, ?, ?,?,?,?,?,?,?);"""
        data_tuple = (title, image, pages, size, language, download_url, categories, description, authors, year)
        cur.execute(select_query, data_tuple)
        conn.commit()

    except Exception:
        pass


download_section()
# create_db()
