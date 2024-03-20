from models.adm import Admin
from models.database import Database  
from sqlalchemy import text

class Dash:
    def contar_usuarios():
        usuarios = Admin.obtener_usuarios()

        
        num_usuarios = len(usuarios)

        return num_usuarios
    
    def obtener_total_cabanas():
        db = Database()
        conn = db.engine.connect()
        
        query = text("""
            SELECT COUNT(*) as total_cabanas
            FROM cabanas
        """)

        result = conn.execute(query)
        total_cabanas = result.fetchone()[0]  
        conn.close()
        
        return total_cabanas

    def calcular_porcentaje(valor_actual, valor_total):
        if valor_total == 0:
            return 0

        porcentaje = (valor_actual / valor_total) * 100
        return round(porcentaje, 2)

    def obtener_fechas(month):
        try:
            db = Database()
            conn = db.engine.connect()
            query = text("""
                SELECT id_fh, TO_CHAR(dia_disp, 'YYYY-MM-DD') as fecha, TO_CHAR(hora_disp, 'HH24:MI:SS') as hora, id_cbn
                FROM fechas
            """)

            result = conn.execute(query)
            fechas_info = result.fetchall()

            # Formatear fechas y horas
            fechas_formateadas = [{'id_fh': row.id_fh, 'fecha': str(row.fecha), 'hora': str(row.hora), 'id_cbn': row.id_cbn} for row in fechas_info]

            conn.close()

            return fechas_formateadas

        except Exception as e:
            print(f"Error al obtener información de fechas: {e}")
            return []
