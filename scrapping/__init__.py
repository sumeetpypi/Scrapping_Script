import sqlite3
import os


def read_file():
    path = os.path.dirname(__file__)
    join_path = os.path.join(path, 'database', 'books_.db')
    return join_path


def get_images(title, image, download_url, categories, description):
    data_dict = list()
    data = read_file()
    print data
    conn = sqlite3.connect(data)
    cur = conn.cursor()
    select_query = "insert into books_db(title,image,download_url,categories, description) values('{}','{}','{}','{}','{}')".format(title,image,download_url,categories, description)
    cur.execute(select_query)
    # fetch_data = get_data.fetchall()
    # print len(fetch_data)
    # for x in fetch_data:
    #     print x
    #     data_dict.append(x)




get_images('2010')
