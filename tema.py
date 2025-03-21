from collections import defaultdict


def task_5a(session):
    # 5a. Найти даты и номера договоров, когда производились операции на сумму не менее 14000 руб.
    rows = session.execute("""
        SELECT contract, date FROM work_activity
        WHERE payment >= 14000 ALLOW FILTERING;
    """)

    print("\n5a. Даты и номера договоров с суммой операции не менее 14000 руб.:")
    for row in rows:
        print(f"Дата: {row.date}, Номер договора: {row.contract}")



def task_6b(session):
    # 6b. Вывести номер договора, название места работы, количество операций, оплату. Отсортировать по возрастанию оплаты.
    rows = session.execute("""
        SELECT contract, workplace_id, quantity, payment
        FROM work_activity;
    """)
    workplaces = {}
    workplace_rows = session.execute("SELECT id, institution FROM workplaces;")
    for row in workplace_rows:
        workplaces[row.id] = row.institution

    sorted_rows = sorted(rows, key=lambda x: x.payment)

    print("\n6b. Номер договора, название места работы, количество операций, оплата (отсортировано по возрастанию оплаты):")
    for row in sorted_rows:
        workplace_name = workplaces.get(row.workplace_id, "Неизвестное место работы")
        print(f"Договор: {row.contract}, Место работы: {workplace_name}, Количество операций: {row.quantity}, Оплата: {row.payment}")


def task_7d(session):
    # 7d. Определить даты, идентификаторы операций и фамилии тех, кто проводил операции стоимостью не менее 7000 руб больше одного раза.

    work_activity_rows = session.execute("""
        SELECT date, operation_id, staff_id, quantity
        FROM work_activity;
    """)

    operation_types_rows = session.execute("""
        SELECT id, price
        FROM operation_types;
    """)

    medical_staff_rows = session.execute("""
        SELECT id, surname
        FROM medical_staff;
    """)

    operation_prices = {row.id: row.price for row in operation_types_rows}
    staff_surnames = {row.id: row.surname for row in medical_staff_rows}

    filtered_results = []
    for row in work_activity_rows:
        operation_price = operation_prices.get(row.operation_id, 0)
        if operation_price >= 7000 and row.quantity > 1:
            staff_surname = staff_surnames.get(row.staff_id, "Неизвестный сотрудник")
            filtered_results.append((row.date, row.operation_id, staff_surname))

    print("\n7d. Даты, идентификаторы операций и фамилии тех, кто проводил операции стоимостью не менее 7000 руб больше одного раза:")
    for date, operation_id, surname in filtered_results:
        print(f"Дата: {date}, ID операции: {operation_id}, Фамилия: {surname}")


def task_11a(session):
    # 11a. Найти учреждение с наименьшим процентом отчислений.

    min_tax_row = session.execute("""
        SELECT MIN(local_tax_percent) AS min_tax
        FROM workplaces;
    """).one()

    if not min_tax_row:
        print("\n11a. Учреждения не найдены.")
        return

    min_tax_percent = min_tax_row.min_tax

    min_tax_institutions = session.execute(f"""
        SELECT institution
        FROM workplaces
        WHERE local_tax_percent = {min_tax_percent}
        ALLOW FILTERING;
    """)

    unique_institutions = set(row.institution for row in min_tax_institutions)

    if unique_institutions:
        print("\n11a. Учреждения с наименьшим процентом отчислений:")
        for institution in unique_institutions:
            print(f"Учреждение: {institution}")
    else:
        print("\n11a. Учреждения не найдены.")


def task_12(session):
    # 12. Используя операцию UNION, получить места проживания медперсонала и операционные пункты для операций.

    staff_locations = session.execute("SELECT address FROM medical_staff;")
    operation_locations = session.execute("SELECT strong_point FROM operation_types;")

    unique_locations = set(row.address for row in staff_locations).union(
        set(row.strong_point for row in operation_locations)
    )

    print("\n12. Места проживания медперсонала и операционные пункты для операций:")
    for location in unique_locations:
        print(location)


def task_13d(session):
    # 13d. Определить места работы, где работали все врачи из чужих населенных пунктов.
    staff_rows = session.execute("SELECT id, address FROM medical_staff;")
    staff_data = {row.id: row.address for row in staff_rows}

    workplace_rows = session.execute("SELECT id, institution, location FROM workplaces;")
    workplace_data = {row.id: (row.institution, row.location) for row in workplace_rows}

    activity_rows = session.execute("SELECT staff_id, workplace_id FROM work_activity;")

    workplace_info = {}
    for row in activity_rows:
        staff_id = row.staff_id
        workplace_id = row.workplace_id

        staff_address = staff_data.get(staff_id, "")
        workplace_location = workplace_data.get(workplace_id, ("", ""))[1]

        is_foreign = staff_address != workplace_location

        if workplace_id not in workplace_info:
            workplace_info[workplace_id] = {"institution": workplace_data.get(workplace_id, ("", ""))[0],
                                            "all_foreign": True}

        if not is_foreign:
            workplace_info[workplace_id]["all_foreign"] = False

    foreign_workplaces = [info for info in workplace_info.values() if info["all_foreign"]]

    if foreign_workplaces:
        print("\n13d. Места работы, где работали все врачи из чужих населенных пунктов:")
        for workplace in foreign_workplaces:
            print(f"Учреждение: {workplace['institution']}")
    else:
        print("\n13d. Нет мест работы, где работали все врачи из чужих населенных пунктов.")
        print("Для выполнения запроса добавьте данные о врачах, которые работают только в чужих населенных пунктах.")


def task_14d(session):
    # 14d. Определить количество операций стоимостью не более 15000, проведенных в понедельник Губановым.

    gubanov_row = session.execute("""
        SELECT id FROM medical_staff WHERE surname = 'Губанов' ALLOW FILTERING;
    """).one()

    if not gubanov_row:
        print("\n14d. Сотрудник с фамилией 'Губанов' не найден.")
        return

    gubanov_id = gubanov_row.id
    operations = session.execute(f"""
        SELECT operation_id, quantity FROM work_activity
        WHERE staff_id = {gubanov_id} AND date = 'Понедельник'
        ALLOW FILTERING;
    """)

    operation_prices = {}
    operation_rows = session.execute("SELECT id, price FROM operation_types;")
    for row in operation_rows:
        operation_prices[row.id] = row.price

    total_quantity = 0
    for row in operations:
        operation_id = row.operation_id
        quantity = row.quantity
        operation_price = operation_prices.get(operation_id, 0)

        if operation_price <= 15000:
            total_quantity += quantity

    print(
        f"\n14d. Общее количество операций стоимостью не более 15000, проведенных в понедельник Губановым: {total_quantity}")


def task_15d(session):
    # 15d. Для каждого дня недели найти общее количество проведенных операций.

    rows = session.execute("""
        SELECT date, quantity FROM work_activity;
    """)

    operations_by_day = {}

    for row in rows:
        day = row.date
        quantity = row.quantity

        if day in operations_by_day:
            operations_by_day[day] += quantity
        else:
            operations_by_day[day] = quantity

    print("\n15d. Общее количество операций по дням недели:")
    for day, total_quantity in operations_by_day.items():
        print(f"День: {day}, Общее количество операций: {total_quantity}")