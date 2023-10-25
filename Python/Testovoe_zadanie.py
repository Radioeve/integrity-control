import hashlib
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sqlite3 as sl
import logging
import logging.handlers
import getopt
import sys
import subprocess
import os

con = sl.connect('dev.db')
data = con.execute("select count(*) from sqlite_master where type='table' and name='control sum'")

with con:
    con.execute ('''
        create table IF NOT EXISTS contol_sum (
            name longtext not null,
            md5 varchr(40) primary key not null
            );
        ''')
    
data = [
    ('text.txt', 'd41d8cd98f00b204e9800998ecf8427e'),
    ('test.txt', '597693667b0cc84a221a583f46d42df2'),
    ('log.txt', '8dc66ea72f761950aa24bf431c22679e'),
    ('super file.txt', 'ce178dbe32b7b6d01e874a34f399c170')
]
with con:
    con.executemany('INSERT or IGNORE into contol_sum VALUES (?,?)',data)
con.commit()

argumentList = sys.argv[1:]
options = "hdu:"
long_options = ["Help", "Duplicate", "Initialization"]
data2 = []

def keys(): 
    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)

        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--Help"):
                print ("ПО 'Контроля целостности объектов файловой системы' Отслеживает изменения в файловой системе")
                print("Также в программе имеются и другие ключи:")
                print("-d - проверка элементов на дубликаты файлов в БД с учетом типа (режима) постановки на КЦ")
                print("-u - инициализация БД данными для постановки объектов на контроль целостности")
                
            elif currentArgument in ("-d", "--Duplicate"):
                                cursor = con.cursor()
                                cursor.execute("SELECT * FROM contol_sum \
                                GROUP BY name, md5 \
                                HAVING COUNT() > 1;")
                                print('Дубликатов файлов:')              
                                for row in cursor.fetchall(): print(row)
            
            elif currentArgument in ("-u", "--Initialization"):
                    print("База данных инициализирована ")
                    file_named = input("Укажите какой файл вы хотите добавить для наблюдения(с раширением): ") 
                    with open(file_named, 'rb') as file_to_check:
                        data = file_to_check.read()    
                        md5_return = hashlib.md5(data).hexdigest()
                    global data2
                    data2 = [
                    (file_named,md5_return)
                    ]
                    with con:                    
                        con.executemany('INSERT or IGNORE into contol_sum VALUES (?,?)',data2)
                    con.commit()     
    
    except getopt.error as err:
        print (str(err))  


keys()
lst = data.copy()+data2.copy()
new_lst = (str(lst)[1:-1].replace(", ", ""))
choise = input("Какой режим проверки:")

if choise in ("Первый режим", "Первый","1","первый режим","первый"):

    file_name = input("Укажите название файла(с расширением): ")

    with open(file_name, 'rb') as file_to_check:
        data = file_to_check.read()    
        md5_returned = hashlib.md5(data).hexdigest()

    print(md5_returned)
    if md5_returned in new_lst :
        print ("Контрольная сумма файла не изменена.")
    else:
        print ("Контрольная сумма файла изменена.")

elif choise in ("Второй режим","Второй","2","второй режим","второй"):

    class MyHandler(FileSystemEventHandler):

        def on_modified(self, event):
            print(f'event type: {event.event_type}  path : {event.src_path}')
        def on_created(self,event):
            print(f'event type: {event.event_type}  path : {event.src_path}')
        def on_deleted(self,event):
            print(f'event type: {event.event_type}  path : {event.src_path}')
        def on_moved(self,event):
            print(f'event type: {event.event_type}  path : {event.src_path}')

    if __name__ == "__main__":
        event_handler = MyHandler()
        observer = Observer()
        observer.schedule(event_handler, path=input("Введите путь до каталога: "), recursive=False)
        observer.start()

        flag = True 
        while flag == True:        
            time.sleep(10)
            question = input("Закончить выполнение программы?:")
            if question == "Да":
                flag = False
                exit(0)
            elif question =="Нет":
                flag = True

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
else:
    print("Ошибка, попробуйте еще раз!")
    subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])




my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)
logging.basicConfig(filename='example.txt',level=logging.DEBUG )
logging.basicConfig(format='%(asctime)s %(message)s')

handler = logging.handlers.SysLogHandler(address = '/dev/log')

my_logger.addHandler(handler)

my_logger.debug('this is debug')
my_logger.info('this is info')
my_logger.warning('this is warning')
my_logger.critical('this is critical')
my_logger.error('this is ERROR')