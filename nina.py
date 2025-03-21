from cassandra.cluster import Cluster
from decimal import Decimal

# 4.c) Различные дни, для которых хранится информация о трудовой деятельности.
def task_4c(session):
    rows = session.execute("SELECT date FROM work_activity;")
    unique_dates = set(row.date for row in rows)

    print("Ответ на задание 4с.\n Различные дни, для которых хранится информация о трудовой деятельности:")
    for date in unique_dates:
        print(date)


# 6.a) Дата, фамилия медперсонала, название места работы, название операции.
def task_6a(session):
    print(" Ответ на задание 6а.\n Детали трудовой деятельности:")
    work_rows = session.execute("SELECT * FROM work_activity;")

    for work in work_rows:
        staff_row = session.execute(
            "SELECT surname FROM medical_staff WHERE id = %s;", (work.staff_id,)
        ).one()
        surname = staff_row.surname if staff_row else "Неизвестно"
        workplace_row = session.execute(
            "SELECT institution FROM workplaces WHERE id = %s;", (work.workplace_id,)
        ).one()
        institution = workplace_row.institution if workplace_row else "Неизвестно"
        operation_row = session.execute(
            "SELECT name FROM operation_types WHERE id = %s;", (work.operation_id,)
        ).one()
        operation_name = operation_row.name if operation_row else "Неизвестно"

        print(f"{work.date}, {surname}, {institution}, {operation_name}")


# 7.c) Учреждения и отчисления, где налог 7-16%, фамилии, сортировка по отчислениям и налогу.
def task_7c(session):
    print("Ответ на задание 7с.\n Учреждения и отчисления, где налог 7-16%:")

    staff_rows = session.execute("""
        SELECT id, surname, tax_percent FROM medical_staff 
        WHERE tax_percent >= 7 AND tax_percent <= 16 ALLOW FILTERING;
    """)

    staff_dict = {row.id: (row.surname, float(row.tax_percent)) for row in staff_rows}
    if not staff_dict:
        print("Нет сотрудников с налогом в диапазоне 7-16%.")
        return
    wp_rows = session.execute("SELECT id, institution FROM workplaces;")
    wp_dict = {row.id: row.institution for row in wp_rows}
    work_rows = session.execute("SELECT staff_id, workplace_id FROM work_activity;")
    tax_data = set()
    for work in work_rows:
        if work.staff_id in staff_dict and work.workplace_id in wp_dict:
            surname, tax_percent = staff_dict[work.staff_id]
            institution = wp_dict[work.workplace_id]
            tax_data.add((institution, tax_percent, surname))

    if not tax_data:
        print("Нет данных для отображения.")
        return

    sorted_data = sorted(tax_data, key=lambda x: (x[1], x[2]))

    for institution, deduction_percent, surname in sorted_data:
        print(f"{institution}, отчисление_percent: {deduction_percent:.2f}, {surname}")

#10с
def task_10c(session):
    print("Ответ на задание 10с. \n Операции стоимостью >=7000 руб, выполненные более одного раза в день:")

    high_cost_ops = session.execute("""
        SELECT id FROM operation_types WHERE price >= 7000 ALLOW FILTERING;
    """)
    high_cost_ids = {row.id for row in high_cost_ops}

    if not high_cost_ids:
        print("Нет операций со стоимостью >=7000 руб.")
        return

    work_rows = session.execute("""
        SELECT date, staff_id, operation_id, quantity FROM work_activity;
    """)

    result_rows = []
    for row in work_rows:
        if row.operation_id in high_cost_ids and row.quantity > 1:
            result_rows.append((row.date, row.staff_id, row.operation_id))

    staff_map = {}
    staff_rows = session.execute("SELECT id, surname FROM medical_staff;")
    for row in staff_rows:
        staff_map[row.id] = row.surname

    for date, staff_id, operation_id in result_rows:
        surname = staff_map.get(staff_id, "Неизвестно")
        print(f"{date}, Операция ID {operation_id}, {surname}")



# 11.d) Медперсонал с более чем 1 наложением гипса в день.
def task_11d(session):
    try:
        session.execute("CREATE INDEX IF NOT EXISTS idx_work_activity_operation_id ON work_activity (operation_id);")
        session.execute("CREATE INDEX IF NOT EXISTS idx_work_activity_quantity ON work_activity (quantity);")
        operation_id = None
        operations = session.execute("""
            SELECT id FROM operation_types WHERE name = 'Наложение гипса' ALLOW FILTERING;
        """)

        print("Ответ на задание 11d. \nФамилии и места проживания медперсонала, проведших более одного наложения гипса в день:")
        for operation in operations:
            operation_id = operation.id
            break

        if operation_id is not None:
            rows_3 = session.execute("""
                SELECT staff_id FROM work_activity
                WHERE operation_id = %s AND quantity > 1 ALLOW FILTERING;
            """, (operation_id,))

            staff_ids = {row.staff_id for row in rows_3}
            rows_4 = session.execute("""
                SELECT id, surname, address FROM medical_staff;
            """)
            found = False
            for row in rows_4:
                if row.id in staff_ids:
                    print(f"Сотрудник: {row.surname}, Адрес: {row.address}")
                    found = True
            if not found:
                print("Нет данных.")
        else:
            print("Операция 'Наложение гипса' не найдена в таблице.")
    finally:
        session.execute("DROP INDEX IF EXISTS idx_work_activity_operation_id;")
        session.execute("DROP INDEX IF EXISTS idx_work_activity_quantity;")


# 13.c) Места работы, где не делали УЗИ более 1 раза.
def task_13c(session):
    rows = session.execute("""
        SELECT workplace_id FROM work_activity
        WHERE operation_id = 6 ALLOW FILTERING;
    """)
    print("Ответ на задание 13с.\n Места работы, где УЗИ делали <=1 раза:")
    from collections import Counter
    wp_ids = [row.workplace_id for row in rows]
    counter = Counter(wp_ids)
    limited_wp_ids = [wp_id for wp_id, count in counter.items() if count <= 1]
    if not limited_wp_ids:
        print("Нет таких мест работы. Нужно добавить данные.")
        return
    wp_rows = session.execute(f"""
        SELECT institution FROM workplaces
        WHERE id IN ({', '.join(map(str, limited_wp_ids))});
    """)
    for row in wp_rows:
        print(row.institution)

# 14.c) Медперсонал, сделавший операцию с минимальной стоимостью.
def task_14c(session):
    print("Ответ на задание 14с.\n Медперсонал, сделавший операцию с минимальной стоимостью:")

    operation_rows = session.execute("SELECT id, name, price FROM operation_types;")
    operations = list(operation_rows)

    if not operations:
        print("Нет данных об операциях.")
        return

    min_price = min(op.price for op in operations)
    min_price_operations = [op.id for op in operations if op.price == min_price]

    placeholders = ', '.join(str(op_id) for op_id in min_price_operations)
    query = f"""
        SELECT staff_id FROM work_activity 
        WHERE operation_id IN ({placeholders}) ALLOW FILTERING;
    """
    rows = session.execute(query)
    staff_ids = set(row.staff_id for row in rows)

    if not staff_ids:
        print("Нет сотрудников, выполнивших операцию с минимальной стоимостью.")
        return

    for staff_id in staff_ids:
        staff_row = session.execute("SELECT surname FROM medical_staff WHERE id=%s;", (staff_id,))
        surname_row = staff_row.one()
        if surname_row:
            print(f"Сотрудник: {surname_row.surname} выполнил операцию стоимостью {min_price} руб.")

# 15.c) Медучреждения с суммой операций >30000.
def task_15c(session):
    print("Ответ на задание 15с.\n Медучреждения с суммой операций >30000 руб.")

    work_rows = session.execute("SELECT workplace_id, payment FROM work_activity;")

    payments_by_workplace = {}
    for row in work_rows:
        payments_by_workplace.setdefault(row.workplace_id, Decimal(0))
        payments_by_workplace[row.workplace_id] += row.payment

    high_payment_workplaces = [wid for wid, total in payments_by_workplace.items() if total > 30000]

    if not high_payment_workplaces:
        print("Нет мест работы с общей суммой выплат более 30000 руб.")
        return

    for workplace_id in high_payment_workplaces:
        workplace_row = session.execute("SELECT institution, location FROM workplaces WHERE id=%s;", (workplace_id,))
        result = workplace_row.one()
        if result:
            total_payment = payments_by_workplace[workplace_id]
            print(f"{result.institution}, {result.location}, общая сумма выплат: {total_payment} руб.")
