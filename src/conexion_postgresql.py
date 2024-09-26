import psycopg2

try:
    connetion=psycopg2.connect(
        host='localhost',
        user='postgres',
        password='guts_2015',
        database='ASApeace',
        port='5433'
    )

    print("conexion exitosa")

    cursor=connetion.cursor()
    cursor.execute("SELECT* FROM funeraria")
    rows= cursor.fetchall()
    for row in rows:
        print(row)
except Exception as ex:
    print(ex)
finally: 
    connetion.close()
    print("conexion finalizada")
