import {saveTask} from './Config/ConfigFirebase.js'

// Envia la informacion basica de la solicitud al servidor

const saveTaskInmuebleForm = document.getElementById("form-activo-radicacion")
const saveTaskCLientForm = document.getElementById("form-cliente-radicacion")

saveTaskInmuebleForm.addEventListener('submit', (e) =>{
    e.preventDefault()
    const hoy = new Date.now()
    console.log(saveTaskInmuebleForm["form-activo-radicacion-zona"].value);
    new Notification(hoy.toDateString())

    // Calculo de fecha actual

   


    // informacion del cliente
    var nombreSolicitante = saveTaskCLientForm["form-cliente-name"]
    var apellidoSolicitante  = saveTaskCLientForm["form-cliente-lastname"]
    var numeroSolicitante = saveTaskCLientForm["form-cliente-phone"]
    var tipoDocumentoSolicitante = saveTaskCLientForm["form-cliente-ID"]
    var idSolicitante = saveTaskCLientForm["form-cliente-cliente-ID"]
    var nombreContacto = saveTaskCLientForm["form-cliente-contact-name"]
    var numeroContacto = saveTaskCLientForm["form-cliente-contacto-cell"]

    // Informacion del inmueble
    var ubicacionInmueble = saveTaskInmuebleForm["form-activo-radicacion-zona"]
    var tipoInmueble = saveTaskInmuebleForm["form-activo-radicacion-tipo-activo"]
    var departamento = saveTaskInmuebleForm["form-activo-radicacion-departamento"]
    var municipio = saveTaskInmuebleForm["form-activo-radicacion-municipio"]
    var direccion = saveTaskInmuebleForm["form-activo-radicacion-direccion"]
    var matricula = saveTaskInmuebleForm["form-activo-radicacion-matricula"]
    var chip = saveTaskInmuebleForm["form-activo-radicacion-chip"]
    var uidUsuario = "xxxxx"// Completar con aunth
    var localizacion = Geopoint( saveTaskInmuebleForm["form-activo-radicacion-latitud"].value, saveTaskInmuebleForm["form-activo-radicacion-longitud"].value )
    var idVisitador = "" // Completar con consulta db
    var fecha = new Date.now()
    var nombreVisitador = saveTaskInmuebleForm["form-activo-radicacion-"]
    var numeroVisitador = saveTaskInmuebleForm["form-activo-radicacion-"]
    var fechaRadicacion = saveTaskInmuebleForm["form-activo-radicacion-"]
    
})