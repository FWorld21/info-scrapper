#!/usr/bin/env python3
import sqlite3


class DBWorkClass:
    def __init__(self):
        self.con = sqlite3.connect('db.sqlite3')
        self.cursor = self.con.cursor()

    def show_all_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return self.cursor.fetchall()

    def show_columns(self, table):
        self.cursor = self.con.execute(f'select * from {table}')
        names = [description[0] for description in self.cursor.description]
        return names

    def show_table(self, table):
        self.cursor.execute(f'SELECT * FROM {table}')
        return self.cursor.fetchall()

    def write_to_db(self, data):
        params = (self.show_table('products_product')[-1][0] + 1 if len(self.show_table('products_product')) != 0 else 0,
                  data['name'], data['slug'], data['price'], data['photo'], data['desc'], data['article'], data['subcategory'], data[datas])

        self.cursor.execute(f"INSERT INTO {table} VALUES (?,?,?,?,?,?,?,?)", params)
        self.con.commit()
        print("Record inserted successfully into SqliteDb_developers table ", self.cursor.rowcount)
        self.cursor.close()


#  ('products_subcategories',), ('products_product',)
testobj = DBWorkClass()
# print(testobj.show_all_tables())
print(testobj.show_table('products_product'))
# print(testobj.show_table('news_comments'))
# print(testobj.show_columns('products_product'))
# testobj.write_to_db()\