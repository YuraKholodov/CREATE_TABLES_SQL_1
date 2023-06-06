import psycopg2


def create_db(conn):
    """Добавление таблиц в БД"""
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(50)
        );

        CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            phone VARCHAR(15),
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
        );
        """
    )
    conn.commit()


def add_client(conn, first_name=None, last_name=None, email=None, phones=None):
    """Добавление клиента в БД"""
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO users
        (first_name, last_name, email)
        VALUES (%s, %s, %s) RETURNING id, first_name, last_name, email
        """,
        (first_name, last_name, email),
    )
    users_res = cur.fetchone()
    print(f"В USERS добавлен {users_res}")

    if phones:
        cur.execute(
            """
            INSERT INTO phones
            (phone, user_id) VALUES (%s, %s) RETURNING id, phone, user_id

            """,
            (phones, users_res[0]),
        )

        print(f"В PHONES добавлен телефон: {cur.fetchone()}")


def add_phone(conn, client_id, phone):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO phones (phone, user_id) VALUES (%s, %s) RETURNING id, phone, user_id
        """,
        (phone, client_id),
    )
    print(f"В PHONES добавлен телефон: {cur.fetchone()}")


def change_client(
    conn, client_id, first_name=None, last_name=None, email=None, phones=None
):
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE users SET first_name=%s, last_name=%s, email=%s WHERE id=%s;
        """,
        (first_name, last_name, email, client_id),
    )

    cur.execute(
        """
        SELECT *
        FROM users
        WHERE id=%s;
        """,
        (client_id),
    )
    print(f"Изменены данные в USERS: {cur.fetchone()}")

    if phones:
        cur.execute(
            """
            DELETE FROM phones
            WHERE user_id=%s
            """,
            (client_id),
        )

        cur.execute(
            """
            INSERT INTO phones (phone, user_id)
            VALUES (%s, %s) RETURNING user_id, phone
            """,
            (phones, client_id),
        )
        print(f"Изменен телефон: {cur.fetchone()}")


def delete_phone(conn, client_id, phone):
    cur = conn.cursor()
    cur.execute(
        """
        DELETE FROM phones
        WHERE user_id=%s AND phone=%s RETURNING id, phone, user_id
        """,
        (client_id, phone),
    )
    print(f"Удален номер: {cur.fetchone()}")


def delete_client(conn, client_id):
    cur = conn.cursor()
    cur.execute(
        """
        DELETE FROM users
        WHERE id=%s RETURNING id, first_name, last_name, email
        """,
        (client_id),
    )
    print(f"Удален клиент: {cur.fetchone()}")


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    """Поиск клиента"""
    cur = conn.cursor()
    cur.execute(
        """
        SELECT us.id, us.first_name, us.last_name, us.email, STRING_AGG(p.phone, ' OR ')
        FROM users AS us JOIN phones AS p ON us.id = p.user_id
        WHERE us.first_name=%s OR us.last_name=%s OR us.email=%s OR p.phone=%s
        GROUP BY us.id
        """,
        (first_name, last_name, email, phone),
    )

    res = cur.fetchall()
    for client in res:
        print(
            f"ID: {client[0]} | Name: {client[1]} | Surname: {client[2]} | Email: {client[3]} | Phone: {client[4]}"
        )


def drop_all_tables(conn):
    """Удаление всех таблиц из БД"""
    cur = conn.cursor()
    cur.execute(
        """
        DROP TABLE phones;
        DROP TABLE users;
        """
    )
    conn.commit()


with psycopg2.connect(
    database="clients_db", user="postgres", password="baraguz"
) as conn:
    drop_all_tables(conn)

    create_db(conn)

    add_client(
        conn,
        first_name="Yura",
        last_name="Kholodov",
        email="yuyuyuyuy",
        phones="3243432545",
    )
    add_client(conn, first_name="Misha", last_name="Kholodov", phones="2113124214")
    add_client(conn, first_name="Фудзи", phones="000000000")

    change_client(
        conn=conn,
        client_id="2",
        first_name="Николай",
        last_name="Зайцев",
        phones="777-777",
    )

    add_phone(conn=conn, client_id="3", phone="12345-12345")

    delete_phone(conn=conn, client_id="2", phone="777-777")

    delete_client(conn=conn, client_id="1")

    find_client(conn=conn, first_name="Фудзи")

conn.close()
