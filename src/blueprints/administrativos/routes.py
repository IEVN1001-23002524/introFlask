from flask import Blueprint, jsonify, request
from database import mysql

administrativos_bp = Blueprint(
    'administrativos',
    __name__,
    url_prefix='/api/administrativos'
)

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))


def leer_administrativo_bd(numempleado):
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM administrativos WHERE numempleado = %s"
        cursor.execute(sql, (numempleado,))
        datos = cursor.fetchone()

        if datos != None:
            administrativo = {
                "numempleado": datos[0],
                "nombre": datos[1],
                "apellidos": datos[2],
                "telefono": datos[3],
                "correo": datos[4],
                "departamento": datos[5]
            }
            return administrativo
        else:
            return None

    except Exception as ex:
        raise ex


@administrativos_bp.route('', methods=['GET'])
def lista_administrativos():
    cursor = None

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
                       SELECT numempleado, nombre, apellidos, telefono, correo, departamento
                       FROM administrativos
                       """)

        datos = cursor.fetchall()
        administrativos = [
            fila_a_diccionario(cursor, fila)
            for fila in datos
        ]

        return jsonify({
            'administrativos': administrativos,
            'mensaje': 'Lista de administrativos',
            'exito': True
        }), 200

    except Exception:
        return jsonify({
            'mensaje': 'Error al consultar los administrativos',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@administrativos_bp.route('', methods=['POST'])
def registrar_administrativo():
    try:
        administrativo = leer_administrativo_bd(request.json['numempleado'])

        if administrativo != None:
            return jsonify({
                'mensaje': 'Administrativo ya existe, no se puede duplicar',
                'exito': False
            })
        else:
            cursor = mysql.connection.cursor()
            sql = """INSERT INTO administrativos
            (numempleado, nombre, apellidos, telefono, correo, departamento)
            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')""".format(
                request.json['numempleado'],
                request.json['nombre'],
                request.json['apellidos'],
                request.json['telefono'],
                request.json['correo'],
                request.json['departamento']
            )

            cursor.execute(sql)
            mysql.connection.commit()

            return jsonify({
                'mensaje': "Administrativo registrado",
                'exito': True
            })

    except Exception as ex:
        return jsonify({
            "message": "error {}".format(ex),
            'exito': False
        })


@administrativos_bp.route('/<numempleado>', methods=['PUT'])
def actualizar_administrativo(numempleado):
    try:
        administrativo = leer_administrativo_bd(numempleado)

        if administrativo != None:
            cursor = mysql.connection.cursor()
            sql = """UPDATE administrativos SET nombre = '{0}',
            apellidos = '{1}',
            telefono = '{2}',
            correo = '{3}',
            departamento = '{4}'
            WHERE numempleado = '{5}'""".format(
                request.json['nombre'],
                request.json['apellidos'],
                request.json['telefono'],
                request.json['correo'],
                request.json['departamento'],
                numempleado
            )

            cursor.execute(sql)
            mysql.connection.commit()

            return jsonify({
                'mensaje': "Administrativo actualizado",
                'exito': True
            })
        else:
            return jsonify({
                'mensaje': "Administrativo no encontrado",
                'exito': False
            })

    except Exception as ex:
        return jsonify({
            'mensaje': "Error {0}".format(ex),
            'exito': False
        })


@administrativos_bp.route('/<numempleado>', methods=['DELETE'])
def eliminar_administrativo(numempleado):
    try:
        administrativo = leer_administrativo_bd(numempleado)

        if administrativo != None:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM administrativos WHERE numempleado = '{0}'".format(numempleado)
            cursor.execute(sql)
            mysql.connection.commit()

            return jsonify({
                'mensaje': "Administrativo eliminado",
                'exito': True
            })
        else:
            return jsonify({
                'mensaje': "Administrativo NO eliminado",
                'exito': False
            })

    except Exception as ex:
        return jsonify({
            'mensaje': "Error: {}".format(ex),
            'exito': False
        })