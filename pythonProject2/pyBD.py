import psycopg2
#
def create_db(conn):
    cur.execute("""
                CREATE TABLE IF NOT EXISTS client(
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(40),
                    last_name VARCHAR(40), 
                    email VARCHAR(40) UNIQUE,
                    phones VARCHAR(40) UNIQUE
                );
                """)
    cur.execute("""
                    CREATE TABLE IF NOT EXISTS numbers(
                        id integer not null references client(id),
                        phones VARCHAR(40) UNIQUE
                    );
                    """)
    #️cur.execute("""ALTER TABLE client DROP COLUMN phones;""")
    pass

def add_client (conn, name, lastname, email, phones=None):
    cur.execute("""
    			INSERT INTO client(first_name, last_name, email)
    			VALUES (%s, %s,%s)
    			RETURNING id, first_name, last_name, email;
    			""",(name, lastname, email))

def add_phone(conn, client_id, phone):
    cur.execute("""
        		INSERT INTO numbers(id,phones)
        		VALUES (%s,%s);           		
        		""", (client_id, phone))
    pass


def change_client(conn, client_id, name, surname, e_mail):
    cur.execute("""UPDATE client SET first_name=%s, last_name=%s, email=%s WHERE id=%s;
           """, (name, surname, e_mail,client_id))



def delete_phone(conn, phone):
    cur.execute("""DELETE FROM numbers WHERE phones = %s;
    """, (phone,))
    pass

def delete_client(conn, client_id):
    cur.execute("""DELETE FROM numbers WHERE id = %s;
        """, (client_id,))
    cur.execute("""DELETE FROM client WHERE id = %s;
        """, (client_id,))
    pass

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    cur.execute("""
    			SELECT c.first_name, c.last_name, c.email, p.phones From client c
    			LEFT JOIN numbers p ON c.id = p.id
    			WHERE c.first_name=%s OR c.last_name=%s OR c.email=%s OR p.phones=%s;
    			""", (first_name, last_name, email, phone,))
    return cur.fetchone()



conn = psycopg2.connect(database="info",user="postgres",password="1234")
with conn.cursor() as cur:
    create_db(conn)
    #️add_client(conn, 'Алина', 'Верет', 'AliNik@')
    #️add_phone(conn, 1, '8444445455')
    #️change_client(conn, 1, 'Аля','Веретен', 'AliNik@')
    #️delete_phone(conn, '8444445455')
    #️delete_client(conn, 1)
    print(find_client(conn, first_name='Ali'))


    conn.commit()

conn.close()