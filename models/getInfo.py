from models.database import Database  
from sqlalchemy import text

class GetInfos:
    def llenar_combo_users_zona():
        try:
            db = Database()  
            conn = db.engine.connect()
            
            query = text("""
                SELECT id_usr, nombre, apellidoP, apellidoM, alias
                FROM usuarios
                WHERE id_tuser = 2
                ORDER BY id_usr
            """)

            result = conn.execute(query)
            users_info = result.fetchall()

            conn.close()

            return users_info

        except Exception as e:
            print(f"Error al obtener información de usuarios: {e}")
            return []   
    
    def get_usuario_info(id_usuario):
            try:
                db = Database()
                conn = db.engine.connect()

                query = text("""
                    SELECT id_usr, nombre, apellidoP, apellidoM, alias, email, psw, id_tuser
                    FROM usuarios
                    WHERE id_usr = :id_usuario
                """)

                result = conn.execute(query, {'id_usuario': id_usuario})

                usuario = result.fetchone()

                conn.close()

                if usuario:
                    # Convertir la tupla en una lista
                    datos_usuario = list(usuario)
                else:
                    datos_usuario = ["Usuario no encontrado"]

                return datos_usuario

            except Exception as e:
                return [f"Error al obtener usuario por ID: {e}"]
            
    def obtener_info_zona(id_zona):
        try:
            db = Database()
            conn = db.engine.connect()

            query = text("""
                SELECT id_zn, nombre_zn, ubicacion_zn, activo_zn, id_usr, uptade_zn
                FROM zonas
                WHERE id_zn = :id_zona
            """)

            result = conn.execute(query, {'id_zona': id_zona})
            zona = result.fetchone()

            conn.close()

            if zona:
                datos_zona = list(zona)
            else:
                datos_zona = ["Zona no encontrada"]

            return datos_zona

        except Exception as e:
            return [f"Error al obtener información de la zona por ID: {e}"]
    
    def obtener_info_cabana(id_cabana):
        try:
            db = Database()
            conn = db.engine.connect()

            query = text("""
                SELECT id_cbn, no_cbn, ubicacion_cbn, capacidad_cbn, id_zn
                FROM cabanas
                WHERE id_cbn = :id_cabana
            """)

            result = conn.execute(query, {'id_cabana': id_cabana})
            zona = result.fetchone()

            conn.close()

            if zona:
                datos_zona = list(zona)
            else:
                datos_zona = ["Zona no encontrada"]

            return datos_zona

        except Exception as e:
            return [f"Error al obtener información de la zona por ID: {e}"]
        
    def obtener_info_fecha(id_fecha):
        try:
            db = Database()
            conn = db.engine.connect()

            query = text("""
                SELECT fechas.id_fh, cabanas.id_cbn
                FROM fechas
                JOIN cabanas ON fechas.id_cbn = cabanas.id_cbn
                WHERE id_fh = :id_fecha
            """)

            result = conn.execute(query, {'id_fecha': id_fecha})
            zona = result.fetchone()

            conn.close()

            if zona:
                datos_zona = list(zona)
            else:
                datos_zona = ["Fecha no encontrada"]

            return datos_zona

        except Exception as e:
            return [f"Error al obtener información de la zona por ID: {e}"]   

    def obtener_info_reservacion(id_reservacion):
        try:
            db = Database()
            conn = db.engine.connect()

            query = text("""
                SELECT id_rsvcn, id_cbn
                FROM reservaciones 
                WHERE id_rsvcn = :id_reservacion               
            """)

            result = conn.execute(query, {'id_reservacion': id_reservacion})
            zona = result.fetchone()

            conn.close()

            if zona:
                datos_zona = list(zona)
            else:
                datos_zona = ["Fecha no encontrada"]

            return datos_zona

        except Exception as e:
            return [f"Error al obtener información de la zona por ID: {e}"]