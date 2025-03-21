from initialize import connect_cassandra, create_fill_tables

from maria import (
    task_4a,
    task_5b,
    task_7a,
    task_10a,
    task_11b,
    task_13a,
    task_14a,
    task_15a
)

from daria import (
    task_4b,
    task_5c,
    task_7b,
    task_10b,
    task_11c,
    task_13b,
    task_14b,
    task_15b
)

from nina import (
    task_4c,
    task_6a,
    task_7c,
    task_10c,
    task_11d,
    task_13c,
    task_14c,
    task_15c
)

from tema import (
    task_5a,
    task_6b,
    task_7d,
    task_11a,
    task_12,
    task_13d,
    task_14d,
    task_15d
)
def main():
    # Подключаемся к Cassandra
    session = connect_cassandra()
    # Создаём таблицы и заполняем их данными
    create_fill_tables(session)
    text = f"Выберете номер задания: 4,5,6,7,10,11,12,13,14,15: "
    while True:
        n = int(input(text))
        if n==4:
            let = input("Выберете подпункт: a,b,c: ")
            if let=="a":
                task_4a(session)
            elif let=="b":
                task_4b(session)
            elif let=="c":
                task_4c(session)
            else:
                print("Smth went wrong...")
        elif n==5:
            let = input("Выберете подпункт: a,b,c: ")
            if let == "a":
                task_5a(session)
            elif let == "b":
                task_5b(session)
            elif let == "c":
                task_5c(session)
            else:
                print("Smth went wrong...")
        elif n==6:
            let = input("Выберете подпункт: a,b: ")
            if let == "a":
                task_6a(session)
            elif let == "b":
                task_6b(session)
            else:
                print("Smth went wrong...")
        elif n==7:
            let = input("Выберете подпункт: a,b,c,d: ")
            if let == "a":
                task_7a(session)
            elif let == "b":
                task_7b(session)
            elif let == "c":
                task_7c(session)
            elif let == "d":
                task_7d(session)
            else:
                print("Smth went wrong...")
        elif n==10:
            let = input("Выберете подпункт: a,b,c: ")
            if let == "a":
                task_10a(session)
            elif let == "b":
                task_10b(session)
            elif let == "c":
                task_10c(session)
            else:
                print("Smth went wrong...")
        elif n==11:
            let = input("Выберете подпункт: a,b,c,d: ")
            if let == "a":
                task_11a(session)
            elif let == "b":
                task_11b(session)
            elif let == "c":
                task_11c(session)
            elif let == "d":
                task_11d(session)
            else:
                print("Smth went wrong...")
        elif n==12:
            task_12(session)
        elif n==13:
            let = input("Выберете подпункт: a,b,c,d: ")
            if let == "a":
                task_13a(session)
            elif let == "b":
                task_13b(session)
            elif let == "c":
                task_13c(session)
            elif let == "d":
                task_13d(session)
            else:
                print("Smth went wrong...")
        elif n==14:
            let = input("Выберете подпункт: a,b,c,d: ")
            if let == "a":
                task_14a(session)
            elif let == "b":
                task_14b(session)
            elif let == "c":
                task_14c(session)
            elif let == "d":
                task_14d(session)
            else:
                print("Smth went wrong...")
        elif n==15:
            let = input("Выберете подпункт: a,b,c,d: ")
            if let == "a":
                task_15a(session)
            elif let == "b":
                task_15b(session)
            elif let == "c":
                task_15c(session)
            elif let == "d":
                task_15d(session)
            else:
                print("Smth went wrong...")
        else:
            print("Smth went wrong...")

if __name__ == "__main__":
    main()
