from cassandra.cluster import Cluster
import uuid
from decimal import Decimal

# Подключаемся к кластеру Cassandra
def connect_cassandra():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()

    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS my_keyspace 
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
    """)

    session.set_keyspace('my_keyspace')
    return session

def create_fill_tables(session):
    session.execute("DROP TABLE IF EXISTS operation_types;")

    session.execute("drop table if exists work_activity;")

    session.execute("drop table if exists medical_staff;")

    session.execute("drop table if exists workplaces;")

    session.execute("""
        CREATE TABLE work_activity (
            contract INT PRIMARY KEY,
            date TEXT,
            staff_id INT,
            workplace_id INT,
            operation_id INT,
            quantity INT,
            payment DECIMAL
        );
    """)

    operations1=[
        (51040, 'Понедельник', 1, 1, 7, 4, 20000),
        (51041, 'Понедельник', 3, 3, 6, 1, 30000),
        (51042, 'Понедельник', 4, 3, 4, 3, 33000),
        (51043, 'Понедельник', 4, 5, 1, 2, 36000),
        (51044, 'Понедельник', 4, 4, 6, 1, 30000),
        (51045, 'Среда', 2, 2, 5, 3, 30000),
        (51046, 'Четверг', 3, 6, 4, 4, 44000),
        (51047, 'Четверг', 4, 6, 2, 1, 28000),
        (51048, 'Четверг', 5, 3, 3, 4, 44000),
        (51049, 'Пятница', 2, 4, 5, 1, 10000),
        (51050, 'Пятница', 3, 6, 4, 2, 22000),
        (51051, 'Пятница', 3, 3, 1, 2, 36000),
        (51052, 'Пятница', 5, 3, 2, 1, 14000),
        (51053, 'Суббота', 3, 2, 7, 2, 10000),
        (51054, 'Суббота', 4, 6, 4, 1, 11000),
        (51055, 'Суббота', 5, 5, 4, 2, 22000),
        (51056, 'Суббота', 3, 6, 3, 2, 22000)
    ]

    for contract, date, staff_id, workplace_id, operation_id, quantity, payment in operations1:
        session.execute("""
            INSERT INTO work_activity (contract, date, staff_id, workplace_id, operation_id, quantity, payment)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (contract, date, staff_id, workplace_id, operation_id, quantity, Decimal(payment) ))

    print("Данные успешно добавлены!")
    session.execute("""
        CREATE TABLE medical_staff (
            id INT PRIMARY KEY,
            surname TEXT,
            address TEXT,
            tax_percent DECIMAL
        );
    """)

    operations2=[
        ('Медина', 'Вознесенское', 14),
        ('Севастьянов', 'Навашино', 14),
        ('Бессонов', 'Выкса', 10),
        ('Губанов', 'Выкса', 10),
        ('Боева', 'Починки', 5)
    ]
    id1=1
    for surname, address, tax_percent in operations2:
        session.execute("""
            INSERT INTO medical_staff (id, surname, address, tax_percent)
            VALUES (%s, %s, %s, %s)
        """, (id1, surname, address, Decimal(tax_percent)))
        id1+=1
    print("Данные успешно добавлены!")

    session.execute("""
        CREATE TABLE workplaces (
            id INT PRIMARY KEY,
            institution TEXT,
            location TEXT,
            local_tax_percent DECIMAL
        );
    """)

    operations3=[
        ('Районная больница', 'Вознесенское', 10),
        ('Травм. пункт', 'Выкса', 3),
        ('Больница', 'Навашино', 4),
        ('Род. дом', 'Вознесенское', 12),
        ('Больница', 'Починки', 4),
        ('Травм. пункт', 'Лукояново', 3)
    ]

    id2=1
    for institution, location, local_tax_percent in operations3:
        session.execute("""
            INSERT INTO workplaces (id, institution, location, local_tax_percent)
            VALUES (%s, %s, %s, %s)
        """, (id2, institution, location, Decimal(local_tax_percent)))
        id2+=1
    print("Данные успешно добавлены!")

    session.execute("""
        CREATE TABLE operation_types (
            id INT PRIMARY KEY,
            name TEXT,
            strong_point TEXT,
            stocks DECIMAL,
            price DECIMAL
        );
    """)

    operations4 = [
        ('Наложение гипса', 'Выкса', 2000, 18000),
        ('Блокада', 'Навашино', 10000, 14000),
        ('Инъекция поливитаминов', 'Навашино', 20000, 11000),
        ('Инъекция алоэ', 'Навашино', 12000, 11000),
        ('ЭКГ', 'Вознесенское', 115, 10000),
        ('УЗИ', 'Вознесенское', 20, 30000),
        ('Флюорография', 'Выкса', 1000, 5000)
    ]

    id3=1
    for name, strong_point, stocks, price in operations4:
        session.execute("""
            INSERT INTO operation_types (id, name, strong_point, stocks, price)
            VALUES (%s, %s, %s, %s, %s)
        """, (id3, name, strong_point, Decimal(stocks), Decimal(price)))
        id3+=1

    print("Данные успешно добавлены!")





