import sqlite3


class DataBaseOfPasswordApp:
    def __init__(self):
        self.__connect = sqlite3.connect('app_config.db', check_same_thread=False)
        self.__cursor = self.__connect.cursor()
        self.__login = 'admin-log'
        self.__password = 'admin-pass'

    def __call__(self):
        self.__routine()

    def __routine(self):
        self.__create_table_app_config()
        self.__set_login_and_password()
        self.__create_table_users_data()

    # part of App data
    def __create_table_app_config(self):
        self.__cursor.execute(
            '''CREATE TABLE IF NOT EXISTS appConfig (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                     login TEXT NOT NULL,
                                                     password TEXT NOT NULL)''')

    def __log_and_pass_exists_checker(self):
        self.__cursor.execute('''SELECT COUNT(*) FROM appConfig''')
        rows = self.__cursor.fetchone()[0]
        self.__connect.commit()
        if rows > 0:
            return True
        return False

    def __set_login_and_password(self):
        if not self.__log_and_pass_exists_checker():
            self.__cursor.execute('''INSERT INTO appConfig VALUES (NULL, ?, ?)''', (self.__login, self.__password,))
            self.__connect.commit()

    def get_login(self):
        self.__cursor.execute('''SELECT login FROM appConfig''')
        return self.__cursor.fetchone()[0]

    def get_password(self):
        self.__cursor.execute('''SELECT password FROM appConfig''')
        return self.__cursor.fetchone()[0]

    def get_login_and_password(self):
        """
        Повертає логін і пароль
        :return: tuple - (str, str)
        """
        self.__cursor.execute('''SELECT login, password FROM appConfig''')
        return self.__cursor.fetchone()


    # Part of users data
    def __create_table_users_data(self):
        self.__cursor.execute(
            '''CREATE TABLE IF NOT EXISTS usersData (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                     siteName TEXT NOT NULL,
                                                     login TEXT NOT NULL,
                                                     password TEXT NOT NULL,
                                                     comment TEXT)''')

    def set_data_to_db(self, site_name, login, password, comment=''):
        """
        Принять 4 переменные - Имя сайта, логин, пароль, комментарии и записать их в таблицу
        :param site_name: str - урл сайта
        :param login: str - логін
        :param password: str - пароль
        :param comment: str - can be empty field
        :return:
        """
        if not self.__check_exists_data_by_name(site_name):
            self.__cursor.execute('''INSERT INTO usersData VALUES (NULL, ?, ?, ?, ?)''',
                                  (site_name, login, password, comment,))
            self.__connect.commit()
        else:
            print('error: __check_exists_data_by_name() - false in et_data_to_db()')

    def update_data_to_db(self, site_name, login, password, comment=''):
        pass

    def get_data_by_site_name(self, site_name_param):
        """
        Принять 1 переменную - имя сайта для поиска (Select)
        :param site_name_param:
        :return:
        """
        if self.__check_exists_data_by_name(site_name_param):
            self.__cursor.execute('''SELECT siteName, login, password, comment
                                        FROM usersData
                                        WHERE siteName = ?''', (site_name_param,))
            return self.__cursor.fetchall()
        else:
            return None

    def __check_exists_data_by_name(self, site_name_param):
        self.__cursor.execute('''SELECT COUNT(*)
                                    FROM usersData
                                    WHERE siteName = ?''', (site_name_param,))
        if self.__cursor.fetchone()[0] > 0:
            return True
        else:
            return False


udb = DataBaseOfPasswordApp()
udb()
