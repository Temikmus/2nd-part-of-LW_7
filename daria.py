
def task_4b(session):
    print("Задание 4b: вывести список различных медучреждений:")
    rows = session.execute("""
        SELECT institution FROM workplaces;
    """)
    unique_institutions = set(row.institution for row in rows)
    for institution in unique_institutions:
        print(institution)


def task_5c(session):
    print(
        "Задание 5c: вывести название, стоимость и адрес опорного пункта для операций, в названии которых есть слово Инъекция, и стоящих более 10000р. Результат отсортировать по адресу и стоимости")
    rows = session.execute("""
        select name, price, strong_point
        from operation_types where price>10000
        allow filtering
    """)
    result = list()
    for row in rows:
        if "Инъекция" in row.name:
            result.append(row)
    result.sort(key=lambda row: (row.strong_point, row.price))
    for res in result:
        print(res.name, res.price, res.strong_point)


def task_7b(session):
    print("Задание 7b: вывести название операций, которые проводили врачи из Вознесенского или Выксы в больницах")
    operation_map = {}
    rows_operation = session.execute("SELECT * FROM operation_types")
    for row_operation in rows_operation:
        operation_map[row_operation.id] = (row_operation.name)
    place_map = {}
    rows_place = session.execute("select * from workplaces")
    for row_place in rows_place:
        place_map[row_place.id] = (row_place.institution, row_place.location)
    staff_map = {}
    rows_staff = session.execute("select * from medical_staff")
    for row_staff in rows_staff:
        staff_map[row_staff.id] = (row_staff.address)
    result = []
    rows = session.execute("SELECT staff_id, operation_id, workplace_id FROM work_activity")
    for row in rows:
        staff_info = staff_map.get(row.staff_id)
        operation_info = operation_map.get(row.operation_id)
        place_info = place_map.get(row.workplace_id)
        if ("Вознесенское" in staff_info or "Выкса" in staff_info) and ("больница" in place_info[0].lower()) and (
                operation_info not in result):
            result.append((operation_info))
    for r in result:
        print(r)


def task_10b(session):
    print("Задание 10b: найти операции, не проводившиеся до среды")
    """Пояснение: не используется not in тк такая операция очень сильно влияет на производительность"""
    rows = session.execute("""
        select operation_id from work_activity where date in ('Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')
        allow filtering;
    """)
    operations_after = {row_after.operation_id for row_after in rows}
    rows_before = session.execute("""
    select operation_id from work_activity 
    where date in ('Понедельник', 'Вторник')
    allow filtering;
    """)
    operations_before = {row.operation_id for row in rows_before}  # Множество operation_id

    new_operations = operations_after - operations_before
    operation_map = {}
    rows_operation = session.execute("select id, name from operation_types")
    for row_operation in rows_operation:
        operation_map[row_operation.id] = (row_operation.name)
    for row_result in new_operations:
        print(operation_map.get(row_result))


def task_11c(session):
    print("Задание 11c: найти цену самой дорогой операции, проведенной в четверг или пятницу")
    rows = session.execute("select * from work_activity where date in ('Четверг', 'Пятница') allow filtering")
    rows_operation = session.execute("select * from operation_types")
    operation_map = {}
    for row_operation in rows_operation:
        operation_map[row_operation.id] = (row_operation.price)
    max_operation = 0
    for row in rows:
        operation_info = operation_map.get(row.operation_id)
        if operation_info > max_operation:
            max_operation = operation_info
    print("Самая дорогая операция стоила:", max_operation)


def task_13b(session):
    print("Задание 13b: вывести операции, проводившиеся всеми врачами в Выксе")
    rows = session.execute("select id from medical_staff where address='Выкса' allow filtering")
    medical_staff = {row.id for row in rows}
    if not medical_staff:
        print("Нет врачей в Выксе.")
    else:
        staff_ids = ', '.join(map(str, medical_staff))
        query = f"select staff_id, operation_id from work_activity where staff_id in ({staff_ids}) allow filtering"
        rows_activity = session.execute(query)
        staff_operations = {staff_id: set() for staff_id in medical_staff}
        for row in rows_activity:
            staff_operations[row.staff_id].add(row.operation_id)
        non_empty_operations = [ops for ops in staff_operations.values() if ops]
        if non_empty_operations:
            common_operations = set.intersection(*non_empty_operations)
        else:
            common_operations = set()
        rows_operations = session.execute("select id, name from operation_types")
        operation_map = {row.id: row.name for row in rows_operations}
        if common_operations:
            for common in common_operations:
                print(operation_map.get(common, f"Неизвестная операция (ID: {common})"))
        else:
            print("Нет операций, которые выполняли все врачи в Выксе.")


def task_14b(session):
    print("Задание 14b: определить средний размер налога для медперсонала, производившего инъекции")
    operation_rows = session.execute("select id, name from operation_types")
    operation_map = {}
    for operation_row in operation_rows:
        operation_map[operation_row.id] = (operation_row.name)
    medical_staff_rows = session.execute("select id, tax_percent from medical_staff")
    medical_staff_map = {}
    for staff_row in medical_staff_rows:
        medical_staff_map[staff_row.id] = (staff_row.tax_percent)
    result = []
    rows = session.execute("select staff_id, operation_id from work_activity")
    for row in rows:
        staff_info = medical_staff_map.get(row.staff_id)
        operation_info = operation_map.get(row.operation_id)
        if 'инъекция' in operation_info.lower():
            result.append((staff_info))
    if result:
        print("Средний налог:", round(sum(result) / len(result), 2))
    else:
        print("Нет данных дляя вычисления среднего налога")


def task_15b(session):
    print("Задание 15b: найти для каждого медработника среднюю стоимость всех проведенных им операций")
    medical_staff_rows = session.execute("select id, surname from medical_staff")
    medical_staff_map = {}
    for staff_row in medical_staff_rows:
        medical_staff_map[staff_row.id] = (staff_row.surname)
    result = {}
    rows = session.execute("select staff_id, payment, quantity from work_activity")
    for row in rows:
        staff_info = medical_staff_map.get(row.staff_id)
        if staff_info in result:
            total_payment, count = result[staff_info]
            result[staff_info] = (total_payment + row.payment, row.quantity + count)
        else:
            result[staff_info] = (row.payment, row.quantity)
    for staff_name, (total_payment, count) in result.items():
        avg_payment = total_payment / count
        print(f"Медработник {staff_name}: Средняя стоимость операции = {avg_payment:.2f}")


