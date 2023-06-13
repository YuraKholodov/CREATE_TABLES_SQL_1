import psycopg2


def create_db(cur):
    """Добавление таблиц в БД"""
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(50) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            phone VARCHAR(15),
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
        );
        """
    )


def add_client(cur, first_name=None, last_name=None, email=None, phones=None):
    """Добавление клиента в БД"""
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


def add_phone(cur, client_id, phone):
    """Добавление телефона"""
    cur.execute(
        """
        INSERT INTO phones (phone, user_id) VALUES (%s, %s) RETURNING id, phone, user_id
        """,
        (phone, client_id),
    )
    print(f"В PHONES добавлен телефон: {cur.fetchone()}")


def change_client(
    cur, client_id, first_name=None, last_name=None, email=None, phones=None
):
    """Изменение данных клиента"""
    if first_name:
        cur.execute(
            """
        UPDATE users SET first_name=%s WHERE id=%s;
        """,
            (first_name, client_id),
        )

    if last_name:
        cur.execute(
            """
        UPDATE users SET last_name=%s WHERE id=%s;
        """,
            (last_name, client_id),
        )

    if email:
        cur.execute(
            """
        UPDATE users SET email=%s WHERE id=%s;
        """,
            (email, client_id),
        )

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

    cur.execute(
        """
        SELECT u.id, u.first_name, u.last_name, u.email, p.phone
        FROM users as u JOIN phones as p ON u.id = p.user_id
        WHERE u.id=%s;
        """,
        (client_id),
    )
    print(f"Изменены данные в USERS: {cur.fetchone()}")


def delete_phone(cur, client_id, phone):
    """Удаление телефона"""
    cur.execute(
        """
        DELETE FROM phones
        WHERE user_id=%s AND phone=%s RETURNING id, phone, user_id
        """,
        (client_id, phone),
    )
    print(f"Удален номер: {cur.fetchone()}")


def delete_client(cur, client_id):
    """Удаление клиента по ID"""
    cur.execute(
        """
        DELETE FROM users
        WHERE id=%s RETURNING id, first_name, last_name, email
        """,
        (client_id),
    )
    print(f"Удален клиент: {cur.fetchone()}")


def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
    """Поиск клиента"""
    if first_name is None:
        first_name = "%"
    else:
        first_name = "%" + first_name + "%"

    if last_name is None:
        last_name = "%"
    else:
        last_name = "%" + last_name + "%"

    if email == None:
        email = "%"
    else:
        email = "%" + email + "%"

    if phone is None:
        phone = "%"
    else:
        phone = "%" + phone + "%"

    cur.execute(
        """
        SELECT us.id, us.first_name, us.last_name, us.email, STRING_AGG(p.phone, ' OR ')
        FROM users AS us JOIN phones AS p ON us.id = p.user_id
        WHERE us.first_name LIKE %s AND us.last_name LIKE %s AND us.email LIKE %s AND p.phone LIKE %s
        GROUP BY us.id
        """,
        (first_name, last_name, email, phone),
    )

    res = cur.fetchall()
    for client in res:
        print(
            f"ID: {client[0]} | Name: {client[1]} | Surname: {client[2]} | Email: {client[3]} | Phone: {client[4]}"
        )


def drop_all_tables(cur):
    """Удаление всех таблиц из БД"""
    cur.execute(
        """
        DROP TABLE phones;
        DROP TABLE users;
        """
    )


if __name__ == "__main__":
    with psycopg2.connect(
        database="clients_db", user="postgres", password="baraguz"
    ) as conn:
        with conn.cursor() as cur:
            drop_all_tables(cur)

            create_db(cur)

            add_client(
                cur,
                first_name="Yura",
                last_name="Kholodov",
                email="yuyuyuyuy@mail.ru",
                phones="3243432545",
            )
            add_client(
                cur,
                first_name="Misha",
                last_name="Kholodov",
                email="ddvsvsd@mail.ru",
                phones="2113124214",
            )
            add_client(
                cur,
                first_name="Фудзи",
                last_name="Yama",
                email="dsdsv@mail.ru",
                phones="+7-5958-5858",
            )

            change_client(
                cur,
                client_id="2",
                first_name="Николай",
                last_name="Зайцев",
                phones="777-777",
            )

            add_phone(cur, client_id="3", phone="12345-12345")

            delete_phone(cur, client_id="2", phone="777-777")

            delete_client(cur, client_id="1")

            find_client(cur, first_name="Фудзи")
