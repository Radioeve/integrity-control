import configparser

def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("DB")
    config.set("DB", "path","/Python/dev.db" )
    config.add_section("RULES")
    config.set("RULES", "text.txt ","4867707f912599978a3f88942db85153")
    config.set("RULES", "test.txt ","90cac8c3643941c8fd7e542c27f37234")
    config.set("RULES", "log.txt ","8dc66ea72f761950aa24bf431c22679e")
    config.set("RULES", "super file.txt ", "ce178dbe32b7b6d01e874a34f399c170")
    config.set("RULES", "Init.txt ","cda2b50a9a362042efacd1b424080d55")
    config.set("RULES", "Возможные события в отчете", "Контрольная сумма файла не изменена; Контрольная сумма файла изменена;")
    config.set("RULES", "Каталог","Python")
    config.set("RULES", "Возможные события в отчете:","Файл изменен; Файл удален; Добавлены файлы; Файлы перемещены;")
    config.add_section("KEYS")
    config.set("KEYS","-u","инициализация БД данными для постановки объектов на контроль целостности")
    config.set("KEYS","-d"," проверка элементов на дубликаты файлов в БД с учетом типа (режима) постановки на КЦ")
    config.set("KEYS","-h"," вывод краткой справочной информации по работе программы и используемым параметрам запуска")
      
    with open(path, "w") as config_file:
        config.write(config_file)
 
if __name__ == "__main__":
    path = "settings.ini"
    createConfig(path)