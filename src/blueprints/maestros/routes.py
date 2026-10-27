from flask import Blueprint, jsonify, request
from database import mysql

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros'
)

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))


def leer_maestro_bd(idmaestro):
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM maestros WHERE idmaestro = %s"
        cursor.execute(sql, (idmaestro,))
        datos = cursor.fetchone()

        if datos != None:
            maestro = {
                "idmaestro": datos[0],
                "nombre": datos[1],
                "apaterno": datos[2],
                "amaterno": datos[3],
                "correo": datos[4]
            }
            return maestro
        else:
            return None

    except Exception as ex:
        raise ex


@maestros_bp.route('', methods=['POST'])
def registrar_maestro():
    try:
        maestro = leer_maestro_bd(request.json['idmaestro'])

        if maestro != None:
            return jsonify({
                'mensaje': 'Maestro ya existe, no se puede duplicar',
                'exito': False
            })
        else:
            cursor = mysql.connection.cursor()
            sql = """INSERT INTO maestros
            (idmaestro, nombre, apaterno, amaterno, correo)
            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')""".format(
                request.json['idmaestro'],
                request.json['nombre'],
                request.json['apaterno'],
                request.json['amaterno'],
                request.json['correo']
            )

            cursor.execute(sql)
            mysql.connection.commit()

            return jsonify({
                'mensaje': "Maestro registrado",
                'exito': True
            })

    except Exception as ex:
        return jsonify({
            "message": "error {}".format(ex),
            'exito': False
        })


@maestros_bp.route('', methods=['GET'])
def lista_maestros():
    cursor = None

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
                       SELECT idmaestro, nombre, apaterno, amaterno, correo
                       FROM maestros
                       """)

        datos = cursor.fetchall()
        maestros = [
            fila_a_diccionario(cursor, fila)
            for fila in datos
        ]

        return jsonify({
            'maestros': maestros,
            'mensaje': 'Lista de maestros',
            'exito': True
        }), 200

    except Exception:
        return jsonify({
            'mensaje': 'Error al consultar los maestros',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@maestros_bp.route('/<idmaestro>', methods=['PUT'])
def actualizar_maestro(idmaestro):
    try:
        maestro = leer_maestro_bd(idmaestro)

        if maestro != None:
            cursor = mysql.connection.cursor()
            sql = """UPDATE maestros SET nombre = '{0}',
            apaterno = '{1}',
            amaterno = '{2}',
            correo = '{3}'
            WHERE idmaestro = {4}""".format(
                request.json['nombre'],
                request.json['apaterno'],
                request.json['amaterno'],
                request.json['correo'],
                idmaestro
            )

            cursor.execute(sql)
            mysql.connection.commit()

            return jsonify({
                'mensaje': "Maestro actualizado",
                'exito': True
            })
        else:
            return jsonify({
                'mensaje': "Maestro no encontrado",
                'exito': False
            })

    except Exception as ex:
        return jsonify({
            'mensaje': "Error {0}".format(ex),
            'exito': False
        })


@maestros_bp.route('/<idmaestro>', methods=['DELETE'])
def eliminar_maestro(idmaestro):
    try:
        maestro = leer_maestro_bd(idmaestro)

        if maestro != None:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM maestros WHERE idmaestro={0}".format(idmaestro)
            cursor.execute(sql)
            mysql.connection.commit()

            return jsonify({
                'mensaje': "Maestro eliminado",
                'exito': True
            })
        else:
            return jsonify({
                'mensaje': "Maestro NO eliminado",
                'exito': False
            })

    except Exception as ex:
        return jsonify({
            'mensaje': "Error: {}".format(ex),
            'exito': False
        })