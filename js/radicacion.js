import {getClients, saveAppraisal, saveClient, getInspectors} from './Config/ConfigFirebase.js'

// Envia la informacion basica de la solicitud al servidor

const saveTaskInmuebleForm = document.getElementById("form-activo-radicacion")
const saveClientForm = document.getElementById("form-cliente-radicacion")
const saveTaskCLientForm = document.getElementById("form-cliente-radicacion")

// informacion del cliente
let nombreSolicitante = saveTaskCLientForm["form-cliente-name"]
let apellidoSolicitante  = saveTaskCLientForm["form-cliente-lastname"]
let numeroSolicitante = saveTaskCLientForm["form-cliente-phone"]
let tipoDocumentoSolicitante = saveTaskCLientForm["form-cliente-ID"]
let idSolicitante = saveTaskCLientForm["form-cliente-cliente-ID"]
let numeroContacto = saveTaskCLientForm["form-cliente-contacto-cell"]
let nombreContacto = saveTaskCLientForm["form-cliente-contact-name"]

let listClients
let listInspectors

// Constantes informacion cliente e inspector tecnico

let idCliente
let idInspector

window.addEventListener('DOMContentLoaded', consultaClientes)
window.addEventListener('DOMContentLoaded', consultaInspectores)

// Ingresa la informacion del cliente consultada

saveClientForm["form-cliente-search"].onchange = function(){

    listClients.forEach(element => {

        if (saveClientForm["form-cliente-search"].value == element.data().idSolicitante) {
            nombreSolicitante.value =element.data().nombreSolicitante
            apellidoSolicitante.value = element.data().apellidoSolicitante
            numeroSolicitante.value = element.data().numeroSolicitante
            tipoDocumentoSolicitante.value = element.data().tipoDocumentoSolicitante
            idSolicitante.value = element.data().idSolicitante
            numeroContacto.value = element.data().numeroContacto
            nombreContacto.value = element.data().nombreContacto
            idCliente = element
        }

    })
}
saveTaskInmuebleForm["form-activo-inspectors"].onchange = function(){

    listInspectors.forEach(element => {
        console.log(saveTaskInmuebleForm["form-activo-inspectors"].value == element.data().ID)
        if (saveTaskInmuebleForm["form-activo-inspectors"].value == element.data().ID) {
            idInspector = element
        }
    })
}

saveClientForm.addEventListener('submit', (e)=>{

    e.preventDefault( )
        
        // E-mail

        try {

            let clienteNoExiste = true
            listClients.forEach(element => {
                console.log(saveClientForm["form-cliente-cliente-ID"].value == element.value);
        
                if (saveClientForm["form-cliente-cliente-ID"].value == element.data().idSolicitante) {
                    alert("El cliente ya existe, por favor agregar desde consulta")
                    clienteNoExiste = falsesaveClientForm
                }      
            })

            if(clienteNoExiste){
                saveClient(
                    nombreSolicitante.value,
                    apellidoSolicitante.value,
                    numeroSolicitante.value,
                    tipoDocumentoSolicitante.value,
                    idSolicitante.value)
                    
                alert("El cliente se ha creado con exito.")
                consultaClientes()
            }
            
            
        } catch (error) {
            console.log(error);   
        }
    

})


saveTaskInmuebleForm.addEventListener('submit', (e) =>{
    e.preventDefault()
    let hoy = new Date();
    new Notification(hoy.toDateString())


    // informacion del cliente
    nombreSolicitante = saveTaskCLientForm["form-cliente-name"].value
    apellidoSolicitante  = saveTaskCLientForm["form-cliente-lastname"].value
    numeroSolicitante = saveTaskCLientForm["form-cliente-phone"].value
    tipoDocumentoSolicitante = saveTaskCLientForm["form-cliente-ID"].value
    idSolicitante = saveTaskCLientForm["form-cliente-cliente-ID"].value
    nombreContacto = saveTaskCLientForm["form-cliente-contact-name"].value
    numeroContacto = saveTaskCLientForm["form-cliente-contacto-cell"].value

    var ubicacionInmueble = saveTaskInmuebleForm["form-activo-radicacion-zona"].value
    var tipoInmueble = saveTaskInmuebleForm["form-activo-radicacion-tipo-activo"].value
    var departamento = saveTaskInmuebleForm["form-activo-radicacion-departamento"].value
    var municipio = saveTaskInmuebleForm["form-activo-radicacion-municipio"].value
    var direccion = saveTaskInmuebleForm["form-activo-radicacion-direccion"].value
    var matricula = saveTaskInmuebleForm["form-activo-radicacion-matricula"].value
    var chip = saveTaskInmuebleForm["form-activo-radicacion-chip"].value
    var uidUsuario = idCliente.id // Completar con aunth.value
    var latitud = saveTaskInmuebleForm["form-activo-radicacion-latitud"].value
    var longitud = saveTaskInmuebleForm["form-activo-radicacion-longitud"].value
    var idVisitador = idInspector.data().ID // Completar con consulta db.value
    var fecha = saveTaskInmuebleForm["form-activo-radicacion-Fecha-Visita"].value
    var nombreVisitador = idInspector.id
    console.log(idInspector.data().Numero);
    var numeroVisitador = idInspector.data().Numero
    var fechaRadicacion = new Date()

    console.log(fecha);
    saveAppraisal(
        nombreSolicitante,
        apellidoSolicitante,
        numeroSolicitante,
        tipoDocumentoSolicitante,
        idSolicitante,
        nombreContacto,
        numeroContacto,
        ubicacionInmueble,
        tipoInmueble,
        departamento,
        municipio,
        direccion,
        matricula,
        chip,
        uidUsuario,
        longitud,
        latitud,
        idVisitador,
        fecha,
        nombreVisitador,
        numeroVisitador,
        fechaRadicacion)
})


// ------------------------------ Funciones de la clase ---------------------------

// Consulta informacion de clientes

async function consultaClientes(){
    listClients = await getClients()
    //saveClientForm["form-cliente-search"].empty()

    limpiar()

    let dataSearch = document.createElement("option")
        dataSearch.text = "Buscar"
        saveClientForm["form-cliente-search"].appendChild(dataSearch)
    
    listClients.forEach(element => {
        dataSearch = document.createElement("option")
        dataSearch.text = element.data().nombreSolicitante+"-"+element.data().idSolicitante
        dataSearch.value = element.data().idSolicitante
        saveClientForm["form-cliente-search"].appendChild(dataSearch)
    });
    
}

// Consulta informacion ispectores y diligencia opciones

async function consultaInspectores(){
    listInspectors = await getInspectors()
    
    listInspectors.forEach(element => {
        let dataSearch = document.createElement("option")
        dataSearch.text = element.id
        dataSearch.value = element.data().ID
        saveTaskInmuebleForm["form-activo-inspectors"].appendChild(dataSearch)
    });
    
}

const limpiar = () => {
    for (let i = saveClientForm["form-cliente-search"].options.length; i >= 0; i--) {
       
        saveClientForm["form-cliente-search"].remove(i);
    }
  };