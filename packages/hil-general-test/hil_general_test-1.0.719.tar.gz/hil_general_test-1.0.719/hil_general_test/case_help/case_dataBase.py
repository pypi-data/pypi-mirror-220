
import os ,sys

r=os.path.abspath(os.path.dirname(__file__))
rootpath= os.path.split(r)[0]
sys.path.append(rootpath)

from hil_general_test.case_help.case_Logger import case_log
import pymysql


class HileDataBase():
    def __init__(self):
        self._connect = pymysql.connect(
            host='192.168.5.43',
            user='kunyitest',
            password='password',
            database='hil',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self._cursor = self._connect.cursor()

    def inset_db(self, table_name, insert_data):
        try:
            data = self.get_mysql_data(data=insert_data)
            fields = data[0]
            values = data[1]

            sql = "INSERT INTO {table_name}({fields}) values ({values})".format(table_name=table_name, fields=fields,
                                                                                values=values)
            self._cursor.execute(sql)
            self._connect.commit()
        except Exception as e:
            self._connect.rollback()
            case_log.error(f"Data insertion failed, and the cause of the failure:{ e}")
        else:
            # self.db_close()
            return self._cursor.lastrowid

    def update_db(self, table_name, update_data, wheres=None):
        try:
            if wheres is not None:
                sql = "UPDATE {table_name} SET {update_data} WHERE {wheres}".format(
                    table_name=table_name,
                    update_data=update_data,
                    wheres=wheres
                )
            else:
                sql = "UPDATE {table_name} SET {update_data}".format(
                    table_name=table_name,
                    update_data=update_data)
            self._cursor.execute(sql)
            self._connect.commit()
        except Exception as e:
            case_log.error("Update failure:", e)
            return False
        else:
            return True

    def delete_db(self, table_name, wheres):
        try:
            sql = "DELETE FROM {table_name} WHERE {wheres}".format(table_name=table_name, wheres=wheres)
            self._cursor.execute(sql)
            self._connect.commit()
        except Exception as e:
            case_log.error('Delete failure:：', e)
            return False
        else:
            return True

    def select_db(self, table_name, fields, wheres=None, get_one=False):
        try:
            if wheres is not None:
                sql = "SELECT {fields} FROM {table_name} WHERE {wheres}".format(
                    fields=fields,
                    table_name=table_name,
                    wheres=wheres
                )
            else:
                sql = "SELECT {fields} FROM {table_name}".format(fields=fields, table_name=table_name)
            self._cursor.execute(sql)
            self._connect.commit()
            if get_one:
                result = self._cursor.fetchone()
            else:
                result = self._cursor.fetchall()
        except Exception as e:
            case_log.error("Select failure", e)
            return None
        else:
            return result

    def get_mysql_data(self, data):
        fields = ""
        insert_data = ""
        for k, v in data.items():
            fields = fields + k + ','
            insert_data = insert_data + "'" + str(v) + "'" + ','
        fields = fields.strip(',')
        insert_data = insert_data.strip(',')
        return [fields, insert_data]

    def db_close(self):
        self._cursor.close()
        self._connect.close()


