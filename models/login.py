from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError  
from models.database import Database

class Login:
    def check_login(email, password):
        try:
            db = Database()
            conn = db.engine.connect()

           
            cmd = text("""
                SELECT u.id_usr, u.email, t.tipo_usr
                FROM usuarios u
                JOIN tipo_usuario t ON u.id_tuser = t.id_tpurs
                WHERE u.email = :email AND u.psw = :password
            """)

            result = conn.execute(cmd, {'email': email, 'password': password})
            user = result.fetchone()
            
            
            conn.close()

            if user:
                # Devuelve True y el tipo de usuario
                return True, user.tipo_usr  
            else:
                return False, None

        except OperationalError as e:
            print(f"Error de base de datos: {e}")
            return False, None