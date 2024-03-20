from flask import Flask, url_for, render_template, request, redirect, jsonify, request, send_file, make_response
from models.hilos import ActualizarCabanaThread, ActualizarUsuarioThread, ActualizarZonaThread, AgregarCabanaThread, AgregarFechaThread, AgregarUsuarioThread, AgregarZonaThread, CrearReservacionThread, ModificarFechaThread, ModificarReservacionThread
from models.login import Login
from models.adm import Admin
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import Flask, session
from models.getInfo import GetInfos
from models.llenarReport import LlenarReporte
from models.dashboard import Dash
import shutil
import threading

lock = threading.Lock()

app = Flask(__name__, static_folder='static')


app.secret_key = 'saranbabiche'

@app.route("/")
def hello_world():
    return render_template('temp.html')

from flask_jwt_extended import create_access_token

@app.route('/inicio', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        auth_success, tipo_usuario = Login.check_login(email, password)
        print("Autenticación exitosa:", auth_success, "Tipo de Usuario:", tipo_usuario)

        if not auth_success:
            error = 'Error: Email o contraseña incorrectos'
        else:
            session['usuario_logueado'] = email
            session['tipo_usuario'] = tipo_usuario  # Guardar tipo de usuario en la sesión
            if tipo_usuario == 'Administrador':
                return redirect(url_for('admin'))
            elif tipo_usuario == 'Supervisor':
                return redirect(url_for('generar_reporte')) #No va

    return render_template('login2.html', error=error)


@app.route("/admin")
def admin():
    # Verifica si el usuario está logueado y si es Administrador
    if 'usuario_logueado' not in session or session.get('tipo_usuario') != 'Administrador':
        return redirect(url_for('login'))

    users_info = GetInfos.llenar_combo_users_zona()
    usuarios = Admin.obtener_usuarios()
    zonas = Admin.obtener_zonas()
    cabanas = Admin.obtener_cabanas()
    numcabanas = Admin.num_cabanas()
    fechas = Admin.obtener_calendarios()
    reservaciones = Admin.obtener_reservaciones()
    num_usuarios = Dash.contar_usuarios()
    total_cabanas = Dash.obtener_total_cabanas()
    porcentaje = Dash.calcular_porcentaje(total_cabanas, 40)

    
    return render_template('admin.html', usuarios=usuarios, zonas=zonas, users_info=users_info, cabanas=cabanas, 
                           numcabanas=numcabanas, fechas=fechas, num_usuarios = num_usuarios, 
                           total_cabanas=total_cabanas, porcentaje=porcentaje, reservaciones=reservaciones)

@app.route("/agregar_usuario", methods=["POST"])
def agregar_usuario():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        apellidoP = request.form.get("apellidoP")
        apellidoM = request.form.get("apellidoM")
        alias = request.form.get("alias")
        email = request.form.get("email")
        psw = request.form.get("psw")
        tipoUsuario = request.form.get("tipoUsuario")
       
        with lock:            
            hilo = AgregarUsuarioThread(nombre, apellidoP, apellidoM, alias, email, psw, tipoUsuario)
            hilo.start()
            hilo.join()
            
            #resultado = Admin.insertar_usuario(nombre, apellidoP, apellidoM, alias, email, psw, tipoUsuario)
            
            if not hilo.is_alive():
                return redirect(url_for("admin"))
            else:
                return "Hubo un error al agregar el usuario."
            
    else:
        return redirect(url_for("admin"))
    
@app.route('/eliminar_usuario/<int:id_usuario>', methods=['GET'])
def eliminar_usuario(id_usuario):
    
    if Admin.eliminar_usuario(id_usuario):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})
    
@app.route('/get_usuario_info/<int:id_usuario>', methods=['GET'])
def obtener_usuario_info(id_usuario):
    datos_usuario = GetInfos.get_usuario_info(id_usuario)
    print(datos_usuario)
    return jsonify({'success': True, 'usuario': datos_usuario})

@app.route('/actualizar_usuario', methods=['POST'])
def actualizar_usuario():
    if request.method == "POST":
        id_usr = request.form.get("id_usr")
        nombre = request.form.get("nombre")
        apellidoP = request.form.get("apellidoP")
        apellidoM = request.form.get("apellidoM")
        alias = request.form.get("alias")
        print("ID a actualizar: ", id_usr)
        
        with lock:
            hilo = ActualizarUsuarioThread(id_usr, nombre, apellidoP, apellidoM, alias)
            hilo.start()
            hilo.join()
            #resultado = Admin.actualizar_usuario(id_usr,nombre, apellidoP, apellidoM, alias)

            if not hilo.is_alive():
                return redirect(url_for("admin"))
            else:
                return "Hubo un error al agregar el usuario."
    else:
        return redirect(url_for("admin"))
    
@app.route('/logout')
def logout():
    session.pop('usuario_logueado', None)  # Elimina el usuario de la sesión
    return redirect(url_for('login'))      # Redirige a la página de inicio de sesión


@app.route("/agregar_zona", methods=["POST"])
def agregar_zona():
    if request.method == "POST":
        nombre_zona = request.form.get("nombreZona")
        ubicacion_zona = request.form.get("ubicacionZona")
        activo_zona = request.form.get("activoZona") == "true"
        id_usr_supervisor = request.form.get("selectUsuario")

        with lock:
            hilo = AgregarZonaThread(nombre_zona, ubicacion_zona, activo_zona, id_usr_supervisor)
            hilo.start()
            hilo.join()
            #resultado = Admin.insertar_zona(nombre_zona, ubicacion_zona, activo_zona, id_usr_supervisor)

            if not hilo.is_alive():
                return redirect(url_for("admin"))
            else:
                return "Hubo un error al agregar la zona."
    else:
        return redirect(url_for("admin"))

@app.route('/eliminar_zona/<int:id_zona>', methods=['GET'])
def eliminar_zona(id_zona):
    if Admin.eliminar_zona(id_zona):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})
    
@app.route('/get_zona_info/<int:id_zona>', methods=['GET'])
def get_zona_info(id_zona):
    zona_info = GetInfos.obtener_info_zona(id_zona)
    return jsonify({'success': True, 'zona': zona_info})

@app.route('/actualizar_zona', methods=['POST'])
def actualizar_zona():
    if request.method == "POST":
        id_zn = request.form.get("id_zn_act")
        nombre_zn = request.form.get("nombreZona_act")
        ubicacion_zn = request.form.get("ubicacionZona_act")
        activo_zn = request.form.get("activoZona_act")
        id_usr = request.form.get("selectUsuario_act")         

        with lock:
            hilo = ActualizarZonaThread(id_zn, nombre_zn, ubicacion_zn, activo_zn, id_usr)
            hilo.start()
            hilo.join()
            #resultado = Admin.actualizar_zona(id_zn, nombre_zn, ubicacion_zn, activo_zn, id_usr)
            if not hilo.is_alive():
                print(id_zn)
                return redirect(url_for("admin"))
            else:
                return "Hubo un error al actualizar la zona."
    else:
        return redirect(url_for("admin"))


@app.route('/generar_reporte', methods=['GET'])
def generar_reporte():
    try:
        ruta_reporte_original = "./static/reportes/Plantilla_reporte.xlsx"
        
        datos_usuarios = LlenarReporte.tabla_usuarios()
        datos_zonas = LlenarReporte.tabla_zonas()
        datos_cabanas_zonas = LlenarReporte.obtener_cabanas_por_zonas()
        datos_usurs_total = LlenarReporte.contar_registros_usuarios()
        datos_zonas_total = LlenarReporte.contar_registros_zonas()
        datos_cabanas_total = LlenarReporte.contar_registros_cabanas()
        datos_fechasdis_total = LlenarReporte.contar_fechas_disponibles()
        datos_fechasnodis_total = LlenarReporte.contar_fechas_no_disponibles()

        llenar_reporte = LlenarReporte(ruta_reporte_original)
        llenar_reporte.llenar_hoja_usuarios(datos_usuarios)
        llenar_reporte.llenar_hoja_zonas(datos_zonas)
        llenar_reporte.llenar_hoja_cabanas_por_zonas(datos_cabanas_zonas)
        llenar_reporte.llenar_hoja_resumen(datos_usurs_total, datos_zonas_total, datos_cabanas_total, datos_fechasdis_total, datos_fechasnodis_total)

        # Guardar el reporte
        llenar_reporte.guardar_reporte()

        # Crear una respuesta para el archivo
        response = make_response(send_file(ruta_reporte_original, as_attachment=True, download_name="reporte_lleno.xlsx"))
        
        # Configurar la respuesta para descargar automáticamente
        response.headers["Content-Disposition"] = "attachment; filename=reporte_lleno.xlsx"

        return response

    except Exception as e:
        return f"Error al generar el reporte: {e}"

#Cabañas
@app.route("/agregar_cabana", methods=["POST"])
def agregar_cabana():
    if request.method == "POST":
        nombre_cabana = request.form.get("NoCabana")
        ubicacion_cabana = request.form.get("bcnCabana")
        capacidad_cabana = request.form.get("CpdCabana")
        id_zn_cabana = request.form.get("selectZonaCbn")

        with lock:
            hilo = AgregarCabanaThread(nombre_cabana, ubicacion_cabana, capacidad_cabana, id_zn_cabana)
            hilo.start()
            hilo.join()
            #resultado = Admin.insertar_cabana(nombre_cabana, ubicacion_cabana, capacidad_cabana, id_zn_cabana)

            if not hilo.is_alive():
                return redirect(url_for("admin"))
            else:
                return "Hubo un error al agregar la zona."
    else:
        return redirect(url_for("admin"))

@app.route('/get_cabana_info/<int:id_cabana>', methods=['GET'])
def obtener_cabana_info(id_cabana):
    datos_cabana = GetInfos.obtener_info_cabana(id_cabana)
    print(datos_cabana)
    return jsonify({'success': True, 'cabana': datos_cabana})

@app.route("/modificar_cabana", methods=["POST"])
def modificar_cabana():
    if request.method == "POST":
        id_cbn = request.form.get("id_cbn_act")
        nombre_cabana = request.form.get("ActNoCabana")
        ubicacion_cabana = request.form.get("ActbcnCabana")
        capacidad_cabana = request.form.get("ActCpdCabana")
        id_zn_cabana = request.form.get("ActselectZonaCbn")

        with lock:
            hilo = ActualizarCabanaThread(id_cbn, nombre_cabana, ubicacion_cabana, capacidad_cabana, id_zn_cabana)
            hilo.start()
            hilo.join()
            #resultado = Admin.actualizar_cabana(id_cbn, nombre_cabana, ubicacion_cabana, capacidad_cabana, id_zn_cabana)

            if not hilo.is_alive():
                return redirect(url_for("admin"))
            else:
                return "Hubo un error al agregar la zona."
    else:
        return redirect(url_for("admin"))

@app.route('/eliminar_cabanas/<int:id_cabana>')
def eliminar_cabanas(id_cabana):
    if Admin.eliminar_cabana(id_cabana):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

#Fechas
@app.route("/agregar_fecha", methods=["POST"])
def agregar_fecha():
    if request.method == "POST":
        dia = request.form.get("lblfecha")
        hora = request.form.get("lblHora")
        id_fc_cabana = request.form.get("selectfcCbn")                
        disponible = request.form.get("selectEstCbn")

        if disponible == "reservado":
            disponible_str = '0' 
        else:
            disponible_str = '1' 
        
        with lock:
            hilo = AgregarFechaThread(dia, hora, id_fc_cabana, disponible_str)
            hilo.start()
            hilo.join()
            #resultado = Admin.insertar_fecha(dia, hora, id_fc_cabana)

            if not hilo.is_alive():
                return redirect(url_for("admin"))
            else:
                return "Hubo un error al agregar la zona."
    else:
        return redirect(url_for("admin"))

@app.route("/modificar_fecha", methods=["POST"])
def modificar_fecha():
    if request.method == "POST":

        id = request.form.get("id_fc_act")
        dia = request.form.get("Actlblfecha")
        hora = request.form.get("ActlblHora")
        id_fc_cabana = request.form.get("ActselectfcCbn")
        disponible = request.form.get("selectEstCbn")

        if disponible == "reservado":
            disponible_str = '0' 
        else:
            disponible_str = '1' 


        with lock:
            hilo = ModificarFechaThread(id, dia, hora, id_fc_cabana, disponible_str)
            hilo.start()
            hilo.join()
            #resultado = Admin.actualizar_fecha(id, dia, hora, id_fc_cabana)

            if not hilo.is_alive():
                return redirect(url_for("admin"))
            else:
                return "Hubo un error al agregar la zona."
    else:
        return redirect(url_for("admin"))

@app.route('/get_fecha_info/<int:id_fecha>', methods=['GET'])
def obtener_fecha_info(id_fecha):
    datos_fecha = GetInfos.obtener_info_fecha(id_fecha)
    print(datos_fecha)
    return jsonify({'success': True, 'fecha': datos_fecha})

@app.route('/eliminar_calendario/<int:id_feha>')
def eliminar_calendario(id_feha):
    if Admin.eliminar_fecha(id_feha):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

#Reservaciones
@app.route("/agregar_reservacion", methods=["POST"])
def agregar_reservacion():
    if request.method == "POST":
        
        cabana = request.form.get("selectResCbn")
        inicio = request.form.get("fechaInicio")
        fin = request.form.get("fechaFin")

        with lock:
            hilo = CrearReservacionThread(inicio, fin, cabana)
            hilo.start()
            hilo.join()
            #resultado = Admin.insertar_reservacion(inicio, fin, cabana)

            if not hilo.is_alive():
                return redirect(url_for("admin"))
            else:
                return "Hubo un error al agregar la zona."
    else:
        return redirect(url_for("admin"))

@app.route('/get_reservacion_info/<int:id_reservacion>', methods=['GET'])
def obtener_reservacion_info(id_reservacion):
    datos_reservacion = GetInfos.obtener_info_reservacion(id_reservacion)
    print(datos_reservacion)
    return jsonify({'success': True, 'reservacion': datos_reservacion})

@app.route("/modificar_reservacion", methods=["POST"])
def modificar_reservacion():
    if request.method == "POST":

        id = request.form.get("id_re_act")
        cabana = request.form.get("selectResCbnModal")
        inicio = request.form.get("fechaInicioModal")
        fin = request.form.get("fechaFinModal")
        
        with lock:
            hilo = ModificarReservacionThread(id, inicio, fin, cabana)
            hilo.start()
            hilo.join()
            
            #resultado = Admin.actualizar_reservacion(id, inicio, fin, cabana)

            if not hilo.is_alive():
                return redirect(url_for("admin"))
            else:
                return "Hubo un error al agregar la zona."
    else:
        return redirect(url_for("admin"))

@app.route('/eliminar_reservacion/<int:id_reservacion>')
def eliminar_reservacion(id_reservacion):
    if Admin.eliminar_reservacion(id_reservacion):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})




@app.route('/reservations_chart/<int:month>')
def reservations_chart(month):
    # Supongamos que tienes una función para obtener las reservaciones para un mes específico
    reservations_data = Dash.obtener_fechas(month)

    # Devuelve los datos como un objeto JSON
    return jsonify(reservations_data)



def formatear_fecha_hora(dt):    
    formato = "%Y-%m-%d %H:%M:%S"
    return dt.strftime(formato) if dt else None



if __name__ == '__main__':
    app.run(debug=True)



