from models.database import Database  
from sqlalchemy import text
from datetime import datetime
import threading


class Admin:
    def obtener_usuarios():
            db = Database()
            conn = db.engine.connect()
            query = text("""
                SELECT u.id_usr, 
                    u.nombre || ' ' || u.apellidoP || ' ' || u.apellidoM AS nombre,
                    u.alias,
                    u.email,
                    t.tipo_usr
                FROM usuarios u
                JOIN tipo_usuario t ON u.id_tuser = t.id_tpurs
                """)

            result = conn.execute(query)
            usuarios = result.fetchall()
            conn.close()
            return usuarios

    def insertar_usuario(nombre, apellidoP, apellidoM, alias, email, psw, tipoUsuario):
        try:
            # Conectar a la base de datos
            db = Database()
            conn = db.engine.connect()

            # Insertar el nuevo usuario en la base de datos
            query = text("""
                INSERT INTO usuarios (nombre, apellidoP, apellidoM, alias, email, psw, id_tuser)
                VALUES (:nombre, :apellidoP, :apellidoM, :alias, :email, :psw, :tipoUsuario)
            """)
            
            conn.execute(query, {
                'nombre': nombre,
                'apellidoP': apellidoP,
                'apellidoM': apellidoM,
                'alias': alias,
                'email': email,
                'psw': psw,
                'tipoUsuario': tipoUsuario
            })
            
            conn.commit()  

            conn.close()
            
            return True
        except Exception as e:
            # Si ocurre un error, se captura y se devuelve False
            print(f"Error al insertar usuario: {e}")
            return False
        
    def eliminar_usuario(id_usuario):
            try:
                # Conectar a la base de datos
                db = Database()
                conn = db.engine.connect()

                # Eliminar el usuario de la base de datos
                query = text("DELETE FROM usuarios WHERE id_usr = :id_usuario")
                conn.execute(query, {'id_usuario': id_usuario})

                conn.commit()
                conn.close()

                return True
            except Exception as e:
                # Si ocurre un error, se captura y se devuelve False
                print(f"Error al eliminar usuario: {e}")
                return False
            
    def actualizar_usuario(id_usuario, nombre, apellidoP, apellidoM, alias):
        try:
            # Conectar a la base de datos
            db = Database()
            conn = db.engine.connect()

            # Actualizar el usuario en la base de datos
            query = text("""
                UPDATE usuarios
                SET nombre = :nombre, apellidoP = :apellidoP, apellidoM = :apellidoM, alias = :alias
                WHERE id_usr = :id_usuario
            """)

            conn.execute(query, {
                'id_usuario': id_usuario,
                'nombre': nombre,
                'apellidoP': apellidoP,
                'apellidoM': apellidoM,
                'alias': alias
            })

            conn.commit()

            conn.close()

            return True
        except Exception as e:
            # Si ocurre un error, se captura y se devuelve False
            print(f"Error al actualizar usuario: {e}")
            return False
    
    def obtener_zonas():
            db = Database()
            conn = db.engine.connect()
            query = text("""
                SELECT z.*, u.nombre
                FROM zonas z
                INNER JOIN usuarios u ON z.id_usr = u.id_usr
                """)

            result = conn.execute(query)
            zonas = result.fetchall()
            conn.close()
            return zonas
    
    def eliminar_zona(id_zona):
        try:
            db = Database()
            conn = db.engine.connect()

            # Eliminar la zona con el ID proporcionado
            query = text("DELETE FROM zonas WHERE id_zn = :id_zona")
            conn.execute(query, {"id_zona": id_zona})
            
            conn.commit()
            conn.close()

            return True
        except Exception as e:
            print(f"Error al eliminar zona: {e}")
            return False
    
    def insertar_zona(nombre_zn, ubicacion_zn, activo_zn, id_usr):
        try:
            # Conectar a la base de datos
            db = Database()
            conn = db.engine.connect()

            # Insertar la nueva zona en la base de datos
            query = text("""
                INSERT INTO zonas (nombre_zn, ubicacion_zn, activo_zn, id_usr, uptade_zn)
                VALUES (:nombre_zn, :ubicacion_zn, :activo_zn, :id_usr, :update_time)
            """)

            conn.execute(query, {
                'nombre_zn': nombre_zn,
                'ubicacion_zn': ubicacion_zn,
                'activo_zn': activo_zn,
                'id_usr': id_usr,
                'update_time': datetime.now()
            })

            conn.commit()
            conn.close()

            return True
        except Exception as e:
            # Si ocurre un error, se captura y se devuelve False
            print(f"Error al insertar zona: {e}")
            return False
        
    def actualizar_zona(id_zn, nombre_zn, ubicacion_zn, activo_zn, id_usr):
        try:
            # Conectar a la base de datos
            db = Database()
            conn = db.engine.connect()

            # Actualizar la zona en la base de datos
            query = text("""
                UPDATE zonas
                SET nombre_zn = :nombre_zn,
                    ubicacion_zn = :ubicacion_zn,
                    activo_zn = :activo_zn,
                    id_usr = :id_usr,
                    uptade_zn = :update_time
                WHERE id_zn = :id_zn
            """)

            conn.execute(query, {
                'nombre_zn': nombre_zn,
                'ubicacion_zn': ubicacion_zn,
                'activo_zn': activo_zn,
                'id_usr': id_usr,
                'update_time': datetime.now(),
                'id_zn': id_zn
            })

            conn.commit()
            conn.close()

            return True
        except Exception as e:
            # Si ocurre un error, se captura y se devuelve False
            print(f"Error al actualizar zona: {e}")
            return False

    #--------Cabañas----------#
    def obtener_cabanas():
            db = Database()
            conn = db.engine.connect()
            query = text("""
                SELECT id_cbn, no_cbn, ubicacion_cbn, capacidad_cbn
                FROM cabanas 
                """)

            result = conn.execute(query)
            cabanas = result.fetchall()
            conn.close()
            return cabanas
    
    def num_cabanas():
        db = Database()
        conn = db.engine.connect()
        query = text("""
            SELECT COUNT(*) FROM cabanas 
            """)
        result = conn.execute(query)
        numcabanas = result.fetchone()[0]
        conn.close()
        return numcabanas
    
    def insertar_cabana(no_cbn, ubicacion_cbn, capacidad_cbn, id_zn):
        try:
            # Conectar a la base de datos
            db = Database()
            conn = db.engine.connect()

            # Insertar el nuevo usuario en la base de datos
            query = text("""
                INSERT INTO cabanas (no_cbn, ubicacion_cbn, capacidad_cbn, id_zn)
                VALUES (:no_cbn, :ubicacion_cbn, :capacidad_cbn, :id_zn)
            """)
            
            conn.execute(query, {
                'no_cbn': no_cbn,
                'ubicacion_cbn': ubicacion_cbn,
                'capacidad_cbn': capacidad_cbn,
                'id_zn': id_zn
            })
            
            conn.commit()  

            conn.close()
            
            return True
        except Exception as e:
            # Si ocurre un error, se captura y se devuelve False
            print(f"Error al insertar cabaña: {e}")
            return False

    def actualizar_cabana(id_cbn, no_cbn, ubicacion_cbn, capacidad_cbn, id_zn):
        try:
            # Conectar a la base de datos
            db = Database()
            conn = db.engine.connect()

            # Actualizar el usuario en la base de datos
            query = text("""
                UPDATE cabanas
                SET no_cbn = :no_cbn, ubicacion_cbn = :ubicacion_cbn, capacidad_cbn = :capacidad_cbn, id_zn = :id_zn
                WHERE id_cbn = :id_cbn
            """)

            conn.execute(query, {
                'id_cbn': id_cbn,
                'no_cbn': no_cbn,
                'ubicacion_cbn': ubicacion_cbn,
                'capacidad_cbn': capacidad_cbn,
                'id_zn': id_zn
            })

            conn.commit()

            conn.close()

            return True
        except Exception as e:
            # Si ocurre un error, se captura y se devuelve False
            print(f"Error al actualizar cabaña: {e}")
            return False

    def eliminar_cabana(id_cbn):
        try:
            db = Database()
            conn = db.engine.connect()  
            
            query = text("DELETE FROM cabanas WHERE id_cbn = :id_cbn")
            conn.execute(query, {"id_cbn": id_cbn})

            conn.commit()
            conn.close()
            
            return True

        except Exception as e:
            print(f"Error al eliminar zona: {e}")
            return False

    #--------Calenadarios----------#
    def obtener_calendarios():
            db = Database()
            conn = db.engine.connect()
            query = text("""
                SELECT fechas.id_fh, fechas.dia_disp, cabanas.no_cbn, fechas.disponible
                FROM fechas
                JOIN cabanas ON fechas.id_cbn = cabanas.id_cbn
                ORDER BY fechas.id_fh ASC
                """)

            result = conn.execute(query)
            fechas = result.fetchall()
            conn.close()
            return fechas
    
    def insertar_fecha(dia_disp, hora_disp, id_cbn, disponible):
        try:
            # Conectar a la base de datos
            db = Database()
            conn = db.engine.connect()

            # Insertar el nuevo usuario en la base de datos
            query = text("""
                INSERT INTO fechas (dia_disp, hora_disp, id_cbn, disponible)
                VALUES (:dia_disp, :hora_disp, :id_cbn, CAST(:disponible AS BIT))
            """)

            
            conn.execute(query, {
                'dia_disp': dia_disp,
                'hora_disp': hora_disp,
                'id_cbn': id_cbn,
                'disponible': disponible
            })
            
            conn.commit()  

            conn.close()
            
            return True
        except Exception as e:
            # Si ocurre un error, se captura y se devuelve False
            print(f"Error al insertar cabaña: {e}")
            return False
        
    def actualizar_fecha(id_fh, dia_disp, hora_disp, id_cbn, disponible):
        try:
            # Conectar a la base de datos
            db = Database()
            conn = db.engine.connect()

            # Actualizar el usuario en la base de datos
            query = text("""
                UPDATE fechas
                SET id_fh = :id_fh, dia_disp = :dia_disp, hora_disp = :hora_disp, id_cbn = :id_cbn, disponible = CAST(:disponible AS BIT)
                WHERE id_fh = :id_fh
            """)

            conn.execute(query, {
                'id_fh': id_fh,
                'dia_disp': dia_disp,
                'hora_disp': hora_disp,
                'id_cbn': id_cbn,
                'disponible': disponible
            })

            conn.commit()

            conn.close()

            return True
        except Exception as e:
            # Si ocurre un error, se captura y se devuelve False
            print(f"Error al actualizar cabaña: {e}")
            return False
    
    def eliminar_fecha(id_fh):
        try:
            db = Database()
            conn = db.engine.connect()  
            
            query = text("DELETE FROM fechas WHERE id_fh = :id_fh")
            conn.execute(query, {"id_fh": id_fh})

            conn.commit()
            conn.close()
            
            return True

        except Exception as e:
            print(f"Error al eliminar zona: {e}")
            return False

    #--------Reservaciones----------#

    def obtener_reservaciones():
        db = Database()
        conn = db.engine.connect()
        query = text("""
            SELECT reservaciones.id_rsvcn, reservaciones.fecha_inicio, reservaciones.fecha_fin, cabanas.no_cbn
            FROM reservaciones
            JOIN cabanas ON reservaciones.id_cbn = cabanas.id_cbn;
            """)
        result = conn.execute(query)
        fechas = result.fetchall()
        conn.close()
        return fechas
     
    def insertar_reservacion(fecha_inicio, fecha_fin, id_cbn):
        try:
            # Conectar a la base de datos
            db = Database()
            conn = db.engine.connect()

            # Insertar el nuevo usuario en la base de datos
            query = text("""
                INSERT INTO reservaciones (fecha_inicio, fecha_fin, id_cbn)
                VALUES (:fecha_inicio, :fecha_fin, :id_cbn)
            """)
            
            # Marcar las fechas como no disponibles en la tabla fechas
            conn.execute(query, {
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'id_cbn': id_cbn
            })

            query_update_fechas = text("""
                UPDATE fechas
                SET disponible = CAST(0 AS BIT)
                WHERE id_cbn = :id_cbn AND dia_disp BETWEEN :fecha_inicio AND :fecha_fin
            """)

            # Ejecutar la consulta de actualización de fechas
            conn.execute(query_update_fechas, {
                'id_cbn': id_cbn,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin
            })
            
            conn.commit()  

            conn.close()
            
            return True
        except Exception as e:
            # Si ocurre un error, se captura y se devuelve False
            print(f"Error al insertar cabaña: {e}")
            return False        

    def actualizar_reservacion(id_rsvcn, fecha_inicio, fecha_fin, id_cbn):
        try:
            # Conectar a la base de datos
            db = Database()
            conn = db.engine.connect()

            # Actualizar el usuario en la base de datos
            query = text("""
                UPDATE reservaciones
                SET id_rsvcn = :id_rsvcn, fecha_inicio = :fecha_inicio, fecha_fin = :fecha_fin, id_cbn = :id_cbn
                WHERE id_rsvcn = :id_rsvcn
            """)

            conn.execute(query, {
                'id_rsvcn': id_rsvcn,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'id_cbn': id_cbn
            })

            query_update_fechas = text("""
                UPDATE fechas
                SET disponible = CAST(0 AS BIT)
                WHERE id_cbn = :id_cbn AND dia_disp BETWEEN :fecha_inicio AND :fecha_fin
            """)

            # Ejecutar la consulta de actualización de fechas
            conn.execute(query_update_fechas, {
                'id_cbn': id_cbn,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin
            })

            conn.commit()

            conn.close()

            return True
        except Exception as e:
            # Si ocurre un error, se captura y se devuelve False
            print(f"Error al actualizar cabaña: {e}")
            return False

    def eliminar_reservacion(id_rsvcn):
        try:
            db = Database()
            conn = db.engine.connect()  
            
            query = text("DELETE FROM reservaciones WHERE id_rsvcn = :id_rsvcn")
            conn.execute(query, {"id_rsvcn": id_rsvcn})

            conn.commit()
            conn.close()
            
            return True

        except Exception as e:
            print(f"Error al eliminar zona: {e}")
            return False
