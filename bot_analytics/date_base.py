import mysql.connector
from utils import read_yaml


class Base:
    """Запросы в базу"""
    config = read_yaml('config\connect_bd.yaml')['BD']

    def __init__(self):
        self.host = self.config['host']
        self.login = self.config['login']
        self.passwd = self.config['passwd']
        self.bd = self.config['bd']

    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.login,
                passwd=self.passwd,
                database=self.bd
            )
        except Exception as e:
            print(f"The error '{e}' occurred")
        return self

    def take_in_base(self):
        """Получаем все лоты из базы buy/sell"""
        cur = self.connection.cursor(dictionary=True)
        cur.execute('SELECT * FROM trade_statistick')

        all = cur.fetchall()
        cur.close()
        return all

    def update_base(self, data):
        """Обновить базу по id_steam"""
        cur = self.connection.cursor()
        # for i in data:
        cur.executemany('INSERT INTO all_lot (ss, status, nowDate) '
                        'VALUES (%s, 1, CURRENT_TIMESTAMP()) ON DUPLICATE KEY '
                        'UPDATE STATUS=VALUES(status), nowDate=VALUES(nowDate)', (data))
        # cur.executemany('UPDATE all_lot SET STATUS = 1, nowDate = CURRENT_TIMESTAMP() '
        #                 'WHERE id_steam = %s', data)
        self.connection.commit()
        print(f'Обновлененно записей: {len(data)}')
        cur.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
