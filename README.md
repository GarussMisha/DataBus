Система для передачи данных между БД

Основые компаненты:
1) БД
2) Producer
3) Consumer


Описание:
1) БД - Используется PostgreSQL
   DB
     - init-script
       - consumer_1 - Потребитель данных
         Таблицы:
           - users
           - country

       - source_1 - Источник данных
         Таблицы:
           - users

       - source_2 - Источник данных
         Таблицы:
           - country

