import psycopg2

try:
    connetion=psycopg2.connect(
        host='localhost',
        user='postgres',
        password='guts_2015',
        database='asapeace',
        port='5432'
    )

    print("conexion exitosa")

    cursor=connetion.cursor()
    cursor.execute("SELECT* FROM main_homenaje")
    rows= cursor.fetchall()
    for row in rows:
        print(row)
except Exception as ex:
    print(ex)
finally: 
    connetion.close()
    print("conexion finalizada")
    
    




try:
    # Establecer conexión con la base de datos
    connection = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='guts_2015',
        database='asapeace',
        port='5432'
    )
    print("Conexión exitosa")

    cursor = connection.cursor()

    # Crear las tablas necesarias
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tipos_servicio (
        id SERIAL PRIMARY KEY,
        tipo VARCHAR(50) NOT NULL,
        precio_base INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servicios_adicionales (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        precio INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ubicaciones (
        id SERIAL PRIMARY KEY,
        region VARCHAR(100) NOT NULL,
        factor_precio REAL NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS beneficios (
        id SERIAL PRIMARY KEY,
        tipo VARCHAR(100) NOT NULL,
        monto INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos_adicionales (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        precio INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS impuestos_descuentos (
        id SERIAL PRIMARY KEY,
        descripcion VARCHAR(100) NOT NULL,
        tipo VARCHAR(50) NOT NULL,
        valor REAL NOT NULL
    );
    """)

    # Insertar datos de ejemplo
    cursor.executemany("""
    INSERT INTO tipos_servicio (tipo, precio_base) VALUES (%s, %s)
    """, [
        ('Sepultura', 2345745),
        ('Cremación', 2146425)
    ])

    cursor.executemany("""
    INSERT INTO servicios_adicionales (nombre, precio) VALUES (%s, %s)
    """, [
        ('Velatorio', 500000),
        ('Transporte', 250000),
        ('Ceremonia', 300000)
    ])

    cursor.executemany("""
    INSERT INTO ubicaciones (region, factor_precio) VALUES (%s, %s)
    """, [
        ('Región Metropolitana', 1.0),
        ('Valparaíso', 1.1),
        ('Araucanía', 0.9)
    ])

    cursor.executemany("""
    INSERT INTO beneficios (tipo, monto) VALUES (%s, %s)
    """, [
        ('Asignación por Muerte', 550000),
        ('Cobertura Isapre', 750000),
        ('Convenio FONASA', 500000)
    ])

    cursor.executemany("""
    INSERT INTO productos_adicionales (nombre, precio) VALUES (%s, %s)
    """, [
        ('Urna Básica', 100000),
        ('Ataúd de Madera', 300000),
        ('Corona de Flores', 120000)
    ])

    cursor.executemany("""
    INSERT INTO impuestos_descuentos (descripcion, tipo, valor) VALUES (%s, %s, %s)
    """, [
        ('IVA', 'IVA', 0.19),
        ('Descuento por Convenio', 'descuento', 100000)
    ])

    # Confirmar los cambios
    connection.commit()
    print("Tablas creadas e información insertada con éxito.")

except Exception as ex:
    print(f"Error: {ex}")

finally:
    if connection:
        cursor.close()
        connection.close()
        print("Conexión finalizada.")
