import threading
from models.adm import Admin

class AgregarUsuarioThread(threading.Thread):
    def __init__(self, nombre, apellidoP, apellidoM, alias, email, psw, tipoUsuario):
        super(AgregarUsuarioThread, self).__init__()
        self.nombre = nombre
        self.apellidoP = apellidoP
        self.apellidoM = apellidoM
        self.alias = alias
        self.email = email
        self.psw = psw
        self.tipoUsuario = tipoUsuario
        
    def run(self):
        resultado = Admin.insertar_usuario(self.nombre, self.apellidoP, self.apellidoM, self.alias, self.email, self.psw, self.tipoUsuario)
        
class ActualizarUsuarioThread(threading.Thread):
    def __init__(self, id_usr, nombre, apellidoP, apellidoM, alias):
        super(ActualizarUsuarioThread, self).__init__()
        self.id_usr = id_usr
        self.nombre = nombre
        self.apellidoP = apellidoP
        self.apellidoM = apellidoM
        self.alias = alias
        
    def run(self):
        resultado = Admin.actualizar_usuario(self.id_usr, self.nombre, self.apellidoP, self.apellidoM, self.alias)
        
class AgregarZonaThread(threading.Thread):
    def __init__(self, nombre_zona, ubicacion_zona, activo_zona, id_usr_supervisor):
        super(AgregarZonaThread, self).__init__()
        self.nombre_zona = nombre_zona
        self.ubicacion_zona = ubicacion_zona
        self.activo_zona = activo_zona
        self.id_usr_supervisor = id_usr_supervisor
        
    def run(self):
        resultado = Admin.insertar_zona(self.nombre_zona, self.ubicacion_zona, self.activo_zona, self.id_usr_supervisor)
        
class ActualizarZonaThread(threading.Thread):
    def __init__(self, id_zn, nombre_zn, ubicacion_zn, activo_zn, id_usr):
        super(ActualizarZonaThread, self).__init__()
        self.id_zn = id_zn
        self.nombre_zn = nombre_zn
        self.ubicacion_zn = ubicacion_zn
        self.id_usr = id_usr
        
    def run(self):
        resultado = Admin.actualizar_zona(self.id_zn, self.nombre_zn, self.ubicacion_zn, self.activo_zn, self.id_usr)

class AgregarCabanaThread(threading.Thread):
    def __init__(self, nombre_cabana, ubicacion_cabana, capacidad_cabana, id_zn_cabana):
        super(AgregarCabanaThread, self).__init__()
        self.nombre_cabana = nombre_cabana
        self.ubicacion_cabana = ubicacion_cabana
        self.capacidad_cabana = capacidad_cabana
        self.id_zn_cabana = id_zn_cabana
        
    def run(self):
        resultado = Admin.insertar_cabana(self.nombre_cabana, self.ubicacion_cabana, self.capacidad_cabana, self.id_zn_cabana)        

class ActualizarCabanaThread(threading.Thread):
    def __init__(self, id_cbn, nombre_cabana, ubicacion_cabana, capacidad_cabana, id_zn_cabana):
        super(ActualizarCabanaThread, self).__init__()
        self.id_cbn = id_cbn
        self.nombre_cabana = nombre_cabana
        self.ubicacion_cabana = ubicacion_cabana
        self.capacidad_cabana = capacidad_cabana
        self.id_zn_cabana = id_zn_cabana
        
    def run(self):
        resultado = Admin.actualizar_cabana(self.id_cbn, self.nombre_cabana, self.ubicacion_cabana, self.capacidad_cabana, self.id_zn_cabana)
        
class AgregarFechaThread(threading.Thread):
    def __init__(self, dia, hora, id_fc_cabana, disponible):
        super(AgregarFechaThread, self).__init__()
        self.dia = dia
        self.hora = hora
        self.id_fc_cabana = id_fc_cabana
        self.disponible = disponible
        
    def run(self):
        resultado = Admin.insertar_fecha(self.dia, self.hora, self.id_fc_cabana, self.disponible)
        
class ModificarFechaThread(threading.Thread):
    def __init__(self, id, dia, hora, id_fc_cabana, disponible):
        super(ModificarFechaThread, self).__init__()
        self.id = id
        self.dia = dia
        self.hora = hora
        self.id_fc_cabana = id_fc_cabana
        self.disponible = disponible
        
    def run(self):
        resultado = Admin.actualizar_fecha(self.id, self.dia, self.hora, self.id_fc_cabana, self.disponible) 
        
class CrearReservacionThread(threading.Thread):
    def __init__(self, inicio, fin, cabana):
        super(CrearReservacionThread, self).__init__()
        self.inicio = inicio
        self.fin = fin
        self.cabana = cabana
        
    def run(self):
        resultado = Admin.insertar_reservacion(self.inicio, self.fin, self.cabana)
        
class ModificarReservacionThread(threading.Thread):
    def __init__(self, id, inicio, fin, cabana):
        super(ModificarReservacionThread, self).__init__()
        self.id = id
        self.inicio = inicio
        self.fin = fin
        self.cabana = cabana
        
    def run(self):
        resultado = Admin.actualizar_reservacion(self.id, self.inicio, self.fin, self.cabana) 