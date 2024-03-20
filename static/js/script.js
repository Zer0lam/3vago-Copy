
$(document).ready(function() {
    
    console.log("Hora de chambear :p");

    $(".home").click(function(){
        mostrarDash();
    });

    $(".users").click(function(){
        mostrarUsers();
    });

    $(".zone").click(function(){
        mostrarZona();
    });

    $(".gerente").click(function(){
        mostrarGerente();
    })

    $(".actionEdit").click(function() {
        var id = $(this).data("id");
        get_data_user(id)
    });
     
    $(".actionDelete").click(function() {
        var id = $(this).data("id");
        console.log("Obtuve el id:", id);
        Swal.fire({
            title: '¿Estás seguro?',
            text: 'Esta acción no se puede deshacer',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Sí, eliminar'
        }).then((result) => {
            if (result.isConfirmed) {
                eliminarUsuario(id);
            }
        });
    });
    
    $(".del-zone").click(function(){
        var id = $(this).data("id");
        console.log("Obtuve el id:", id);
        Swal.fire({
            title: '¿Estás seguro?',
            text: 'Esta acción no se puede deshacer',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Sí, eliminar'
        }).then((result) => {
            if (result.isConfirmed) {
                eliminar_zona(id);
            }
        });
    });

    $(".edit-zone").click(function() {
        var id = $(this).data("id");
        get_data_zona(id);
    });

    $(".edit-cabana").click(function() {
        var id = $(this).data("id");
        get_data_cabana(id);
    });

    $(".del-cabanas").click(function(){
        var id = $(this).data("id");
        console.log("Obtuve el id:", id);
        Swal.fire({
            title: '¿Estás seguro?',
            text: 'Esta acción no se puede deshacer',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Sí, eliminar'
        }).then((result) => {
            if (result.isConfirmed) {
                eliminar_cabanas(id);
            }
        });
    });

    $(".edit-calendario").click(function() {
        var id = $(this).data("id");
        get_data_calendario(id);
    });

    $(".del-calendario").click(function(){
        var id = $(this).data("id");
        console.log("Obtuve el id:", id);
        Swal.fire({
            title: '¿Estás seguro?',
            text: 'Esta acción no se puede deshacer',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Sí, eliminar'
        }).then((result) => {
            if (result.isConfirmed) {
                eliminar_calendario(id);
            }
        });
    });
   
    $(".edit-reservacion").click(function() {
        var id = $(this).data("id");
        get_data_reservacion(id);
    });

    $(".del-reservacion").click(function() {
        var id = $(this).data("id");
        console.log("Obtuve el id:", id);
        Swal.fire({
            title: '¿Estás seguro?',
            text: 'Esta acción no se puede deshacer',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Sí, eliminar'
        }).then((result) => {
            if (result.isConfirmed) {
                eliminar_reservacion(id);
            }
        });
    });
});


function mostrarDash(){
    var divInico = document.getElementById("divInicio");
    var divUsers = document.getElementById("divUsuarios");
    var divZonas = document.getElementById("divZona");
    var divGerente = document.getElementById("divGerente");
    divInico.style.display = 'block';
    divUsers.style.display = 'none';
    divZonas.style.display = 'none';
    divGerente.style.display = 'none';
}

function mostrarUsers(){
    var divInico = document.getElementById("divInicio");
    var divUsers = document.getElementById("divUsuarios");
    var divZonas = document.getElementById("divZona");
    var divGerente = document.getElementById("divGerente");
    divInico.style.display = 'none';
    divUsers.style.display = 'block';
    divZonas.style.display = 'none';
    divGerente.style.display = 'none';
}

function mostrarZona(){
    var divInico = document.getElementById("divInicio");
    var divUsers = document.getElementById("divUsuarios");
    var divZonas = document.getElementById("divZona");
    var divGerente = document.getElementById("divGerente");
    divInico.style.display = 'none';
    divUsers.style.display = 'none';
    divZonas.style.display = 'block';
    divGerente.style.display = 'none';
}

function mostrarGerente(){
    var divInico = document.getElementById("divInicio");
    var divUsers = document.getElementById("divUsuarios");
    var divZonas = document.getElementById("divZona");
    var divGerente = document.getElementById("divGerente");
    divInico.style.display = 'none';
    divUsers.style.display = 'none';
    divZonas.style.display = 'none';
    divGerente.style.display = 'block';
}

function eliminarUsuario(id) {
    $.ajax({
        url: "/eliminar_usuario/" + id,
        type: "GET",
        success: function(response) {
            if (response.success) {
                
                console.log("Usuario eliminado exitosamente.");
            } else {
                console.error("Error al eliminar usuario.");
            }
        },
        error: function(error) {
            console.error("Error de solicitud:", error);
        }
    });
}

function get_data_user(id){
    $.ajax({
        url: "/get_usuario_info/" + id,
        type: "GET",
        success: function(response) {
            console.log("Respuesta completa del servidor:", response);

            if (response.success) {
                var datos_usuario = response.usuario;
                $("#id_usr").val(response.usuario.id_usr);
                $("#id_usr_act").val(datos_usuario[0]);
                $("#nombre_act").val(datos_usuario[1]);
                $("#apellidoP_act").val(datos_usuario[2]);
                $("#apellidoM_act").val(datos_usuario[3]);
                $("#alias_act").val(datos_usuario[4]);
                $("#email_act").val(datos_usuario[5]);
                $("#psw_act").val(datos_usuario[6]);
                $("#tipoUsuario_act").val(datos_usuario[7]);

                // Mostrar el modal de actualización
                $("#modalActualizarUsuario").modal("show");

            } else {
                console.error("Error al obtener información del usuario.");
            }
        },
        error: function(error) {
            console.error("Error de solicitud:", error);
        }
    });
}

function eliminar_zona(id){
    $.ajax({
        url: "/eliminar_zona/" + id,
        type: "GET",
        success: function(response) {
            if (response.success) {
                
                console.log("Zona eliminada exitosamente.");
            } else {
                console.error("Error al eliminar una zona.");
            }
        },
        error: function(error) {
            console.error("Error de solicitud:", error);
        }
    });
}

function get_data_zona(id) {
    $.ajax({
        url: "/get_zona_info/" + id,
        type: "GET",
        success: function(response) {
            console.log("Respuesta completa del servidor:", response);

            if (response.success) {
                var datos_zona = response.zona;
                $("#id_zn_act").val(datos_zona[0]);
                $("#nombreZona_act").val(datos_zona[1]);
                $("#ubicacionZona_act").val(datos_zona[2]);

                var selectAct = datos_zona[3].toString();
                $("#activoZona_act").val(selectAct);  // No es necesario convertir a minúsculas

                

                $("#selectUsuario_act").val(datos_zona[4]);

                $("#modalActualizarZona").modal("show");

            } else {
                console.error("Error al obtener información de la zona.");
            }
        },
        error: function(error) {
            console.error("Error de solicitud:", error);
        }
    });
}

//Cabañas
function get_data_cabana(id){
    $.ajax({
        url: "/get_cabana_info/" + id,
        type: "GET",
        success: function(response) {
            console.log("Respuesta completa del servidor:", response);

            if (response.success) {
                var datos_cabana = response.cabana;
                $("#id_cbn_act").val(datos_cabana[0]);
                $("#ActNoCabana").val(datos_cabana[1]);
                $("#ActbcnCabana").val(datos_cabana[2]);
                $("#ActCpdCabana").val(datos_cabana[3]);                

                // Mostrar el modal de actualización
                $("#modalModCabana").modal("show");

            } else {
                console.error("Error al obtener información de la cabaña.");
            }
        },
        error: function(error) {
            console.error("Error de solicitud:", error);
        }
    });
}

function eliminar_cabanas(id){
    $.ajax({
        url: "/eliminar_cabanas/" + id,
        type: "GET",
        success: function(response) {
            if (response.success) {
                
                console.log("Zona eliminada exitosamente.");
            } else {
                console.error("Error al eliminar una zona.");
            }
        },
        error: function(error) {
            console.error("Error de solicitud:", error);
        }
    });
}

//Calendario
function get_data_calendario(id){
    $.ajax({
        url: "/get_fecha_info/" + id,
        type: "GET",
        success: function(response) {
            console.log("Respuesta completa del servidor:", response);

            if (response.success) {
                var datos_cabana = response.fecha;
                $("#id_fc_act").val(datos_cabana[0]);
                $("#ActselectfcCbn").val(datos_cabana[1]);                

                // Mostrar el modal de actualización
                $("#modalActCalendario").modal("show");

            } else {
                console.error("Error al obtener información de la cabaña.");
            }
        },
        error: function(error) {
            console.error("Error de solicitud:", error);
        }
    });
}

function eliminar_calendario(id){
    $.ajax({
        url: "/eliminar_calendario/" + id,
        type: "GET",
        success: function(response) {
            if (response.success) {
                
                console.log("Fecha eliminada exitosamente.");
            } else {
                console.error("Error al eliminar una zona.");
            }
        },
        error: function(error) {
            console.error("Error de solicitud:", error);
        }
    });
}

//Reservacion
function get_data_reservacion(id){
    $.ajax({
        url: "/get_reservacion_info/" + id,
        type: "GET",
        success: function(response) {
            console.log("Respuesta completa del servidor:", response);

            if (response.success) {
                var datos_reservacion = response.reservacion;
                $("#id_re_act").val(datos_reservacion[0]);
                $("#selectResCbnModal").val(datos_reservacion[1]);

                // Mostrar el modal de actualización
                $("#modalActReservacion").modal("show");

            } else {
                console.error("Error al obtener información de la cabaña.");
            }
        },
        error: function(error) {
            console.error("Error de solicitud:", error);
        }
    });
}

function eliminar_reservacion(id){
    $.ajax({
        url: "/eliminar_reservacion/" + id,
        type: "GET",
        success: function(response) {
            if (response.success) {                
                console.log("reservacion eliminada exitosamente.");
            } else {
                console.error("reservacion al eliminar una zona.");
            }
        },
        error: function(error) {
            console.error("Error de solicitud:", error);
        }
    });
}