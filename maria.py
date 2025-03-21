
def task_4a(session):
    # 4a вывести различные адреса всех медработников
    rows = session.execute("""
            select address from medical_staff;
        """)
    unique_addresses = set(row.address for row in rows)
    print("\n4a. Различные адреса всех медработников:")
    for address in unique_addresses:
        print(address)

def task_5b(session):
    # 5b найти размер налога для медперсонала из Выксы или Навашино
    rows_2 = session.execute("""
           select address, surname, tax_percent from medical_staff
           where address IN ('Выкса', 'Навашино') allow filtering;
       """)
    print("\n5b. Налог для медперсонала из Выксы или Навашино:")
    for tax in rows_2:
        print(f"Сотрудник: {tax.surname}, Налоговый процент: {tax.tax_percent}, Адрес: {tax.address}")

def task_7a(session):
    # 7a определить фамилии и места проживания медперсонала, проведших более одного наложения гипса в день
    operation_id = None
    operations = session.execute("""
            select id from operation_types where name = 'Наложение гипса' allow filtering;
        """)
    for operation in operations:
        operation_id = operation.id

    if operation_id is not None:
        rows_3 = session.execute("""
                select staff_id, date, quantity
                from work_activity
                where operation_id = %s and quantity > 1 allow filtering;
            """, (operation_id,))

        staff_ids = {row.staff_id for row in rows_3}

        rows_4 = session.execute("""
                select id, surname, address
                from medical_staff
            """)

        print("\n7a. Фамилии и места проживания медперсонала, проведших более одного наложения гипса в день:")
        for row in rows_4:
            if row.id in staff_ids:
                print(f"Сотрудник: {row.surname}, Адрес: {row.address}")


def task_10a(session):
    # 10a найти фамилии медперсонала из Навашино, проводивших инъекции в Выксе
    print("\n10a. Медперсонал из Навашино, проводивший инъекции в Выксе:")
    operation_ids = set()
    rows_5 = session.execute("""
            select id from operation_types
            where strong_point = 'Выкса' and name in ('Инъекция поливитаминов', 'Инъекция алоэ')
            allow filtering;
         """)
    for row in rows_5:
        operation_ids.add(row.id)
    staff_ids = set()
    for operation_id in operation_ids:
        rows = session.execute("""
                select staff_id from work_activity
                where operation_id = %s allow filtering;
            """, (operation_id,))
        for row in rows:
            staff_ids.add(row.staff_id)
    if staff_ids:
        rows_6 = session.execute("""
                select surname from medical_staff
                where id in %s and address = 'Навашино' allow filtering
            """, (tuple(staff_ids),))
        for row in rows_6:
            print(row.surname)
    else:
        print("Нет подходящего медперсонала")

def task_11b(session):
    # 11b найти медперсонал, проводивший операции с самой малой суммой оплаты
    min_payment = session.execute("""
            select min(payment) from work_activity;
        """).one()[0]

    med_ids = session.execute("""
            select staff_id from work_activity where payment = %s allow filtering
        """, (min_payment,))
    staff_ids = [row.staff_id for row in med_ids]

    surnames = session.execute("""
            select surname from medical_staff
            where id in (%s)
        """ % ','.join([str(id) for id in staff_ids]))
    print("\n11b. Медперсонал с минимальной оплатой:")
    for surname in surnames:
        print(surname.surname)

def task_13a(session):
    # 13a медперсонал, который не работал в субботу
    med_ids_2 = session.execute("""
        select staff_id from work_activity
        where date = 'Суббота' allow filtering;
    """)
    staff_ids_saturday = {row.staff_id for row in med_ids_2}
    surnames_2 = session.execute("""
        select surname, id from medical_staff;
    """)
    print("\n13a. Медперсонал, который не работал в субботу:")
    for surname in surnames_2:
        if surname.id not in staff_ids_saturday:
            print(surname.surname)

def task_14a(session):
    # 14a найти число различных мест работы для медперсонала,
    # работавшего в Выксы
    addresses = session.execute("""
            select id from workplaces
            where location = 'Выкса' allow filtering;
        """)
    workplace_ids = {row.id for row in addresses}
    workplace_ids_2 = session.execute("""
            select workplace_id from work_activity
            where workplace_id in (%s) allow filtering;
        """ % ','.join([str(id) for id in workplace_ids]))

    unique_workplaces = {row.workplace_id for row in workplace_ids_2}
    print("\n14а. Число различных мест работы медперсонала, работавших в Выксы:")
    print({len(unique_workplaces)})


def task_15a(session):
    # 15a определить для каждого дня недели и каждой операции
    # сколько раз ее проводили
    print("\n15a. Количество проведенных операций для каждого дня недели")
    operation_counts = session.execute("""
            select date, operation_id, quantity from work_activity;
        """)
    operation_count_by_day = {}
    for row in operation_counts:
        date = row.date
        operation_id = row.operation_id
        count = row.quantity
        if date not in operation_count_by_day:
            operation_count_by_day[date] = {}
        if operation_id not in operation_count_by_day[date]:
            operation_count_by_day[date][operation_id] = 0
        operation_count_by_day[date][operation_id] += count

    operation_names = session.execute("""
            select id, name from operation_types;
        """)
    operation_name_map = {row.id: row.name for row in operation_names}

    for date, operations in operation_count_by_day.items():
        for operation_id, count in operations.items():
            operation_name = operation_name_map.get(operation_id, "Unknown operation")
            print(f"День недели: {date}, Операция: {operation_name}, Количество: {count}")

