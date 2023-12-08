  // Import the functions you need from the SDKs you need
  import { initializeApp} from "https://www.gstatic.com/firebasejs/10.6.0/firebase-app.js"; 
  //import { firebase} from "https://www.gstatic.com/firebasejs/10.6.0/firebase.js";

  import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-analytics.js";
  import { getAuth, onAuthStateChanged, signInWithPopup, GoogleAuthProvider, signInWithEmailAndPassword, connectAuthEmulator} from "https://www.gstatic.com/firebasejs/10.6.0/firebase-auth.js";
  import { getFirestore, collection, getDoc, getDocs,addDoc, query, orderBy, GeoPoint} from "https://www.gstatic.com/firebasejs/10.6.0/firebase-firestore.js"

 //import { getFirestore, collection, getDoc, getDocs} from "https://www.gstatic.com/firebasejs/9.22.0/firebase-getFirestore.js";
//import { user } from "firebase-functions/v1/auth";
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional

  const btnLoginGoogle = document.getElementById("login-google-button")
  const LogInForm = document.getElementById("login-form")

  const dbAppraisal = "Avaluos"
  const dbClients = "Cliente"
  const dbInspectors = "Visitadores"

  const firebaseConfig = {
    apiKey: "AIzaSyDRwj6hrGphOvt4hiJIfNaBAO-FoDz366U",
    authDomain: "visitatecnica-a1b3f.firebaseapp.com",
    databaseURL: "https://visitatecnica-a1b3f.firebaseio.com",
    projectId: "visitatecnica-a1b3f",
    storageBucket: "visitatecnica-a1b3f.appspot.com",
    messagingSenderId: "651647208957",
    appId: "1:651647208957:web:80bc561c32078a53d89d94",
    measurementId: "G-XRPKF6BG18"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const analytics = getAnalytics(app);
  const provider = new GoogleAuthProvider();

  // funciones de coneccion y modificacion de la base de datos

  const db = getFirestore(app)

  export const saveTask = (email, password) =>{
    console.log(email, password);
    addDoc(collection(db, 'Pruebas'), {email, password})
  }

  

  // ------------------------------ Autenticacion ---------------------------------------------

  

  export const loginEmailPassword = async (email, password) => {
    const auth = getAuth(app)

    try {

      const userCredential = await signInWithEmailAndPassword(auth, email, password)
      window.location = "/Radicacion.html"
      
    } catch (error) {
      console.log(error);
      if (Notification.permission === 'granted') {
        new Notification("Usuario o contraseña incorrecta")
      }
    }
  }  

// -------------------------------Creacion y modificacion de avaluos -------------------------

  export const saveClient = async (

    nombreSolicitante,
    apellidoSolicitante,
    numeroSolicitante,
    tipoDocumentoSolicitante,
    idSolicitante, 

  ) => {
    addDoc(collection(db, dbClients),{
      nombreSolicitante,
    apellidoSolicitante,
    numeroSolicitante,
    tipoDocumentoSolicitante,
    idSolicitante, 
    })
  }

  export const saveAppraisal = async (nombreSolicitante,
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
    latitud, // Geopoint
    idVisitador,
    fecha,
    nombreVisitador,
    numeroVisitador,
    fechaRadicacion) => {

    let localizacion = new GeoPoint(latitud, longitud)
    const Estado = "Pendiente"

    addDoc(collection(db, dbAppraisal), {
    nombreSolicitante, //-
    apellidoSolicitante, //-
    numeroSolicitante, //-
    tipoDocumentoSolicitante, //-
    idSolicitante, //-
    nombreContacto, //-
    numeroContacto, //-
    ubicacionInmueble, //-
    tipoInmueble, //-
    departamento, //-
    municipio, //-
    direccion, //-
    matricula, //-
    chip, //-
    uidUsuario, //- Consulta Auth
    localizacion, // Geopoint
    idVisitador, //- Consulta auth
    fecha, // Automatico hora fecha del sistema
    nombreVisitador, //-
    numeroVisitador, // Consulta Firestore
    fechaRadicacion,
    Estado})
  }

  //----------------------- Consulta de datos ------------------------

  export const getAppraisals = () => {

    const appraisaldocs = getDocs(collection(db,dbAppraisal))
 
    return appraisaldocs
 
    //db.collection('Pruebas').getDocs();
   }

   export const getClients = () =>{

    const consulta = query(collection(db, dbClients), orderBy("nombreSolicitante"))
    //const clientsDocs = getDocs(collection(db, dbClients))
    const clientsDocs = getDocs(consulta)
    
    return clientsDocs

   }
   export const getInspectors = () =>{

    const consulta = query(collection(db, dbInspectors))
    const Docs = getDocs(consulta)
    
    return Docs

   }

/*
  const googleAuthProvider = new GoogleAuthProvider();

  onAuthStateChanged(auth, user => {
    if(user =! null){
      console.log('Logged in!');
      console.log(auth);
    } else {
      console.log('No User');
    }
  })*/
//****** Acceso con Google */

/*btnLoginGoogle.onclick = signInWithPopup(auth, provider)
  .then((result) => {
    // This gives you a Google Access Token. You can use it to access the Google API.
    const credential = GoogleAuthProvider.credentialFromResult(result);
    const token = credential.accessToken;
    // The signed-in user info.
    const user = result.user;

    console.log(result);
    // IdP data available using getAdditionalUserInfo(result)
    // ...
  }).catch((error) => {
    // Handle Errors here.
    const errorCode = error.code;
    const errorMessage = error.message;
    // The email of the user's account used.
    const email = error.customData.email;
    // The AuthCredential type that was used.
    const credential = GoogleAuthProvider.credentialFromError(error);
    // ...
  });*/
/*
  onAuthStateChanged(auth, async (user)=> {
    console.log();
  })



  LogInForm.addEventListener('submit', async e => {
    e.preventDefault()
    
    const email = LogInForm['email-login'].value
    const password = LogInForm['password-login'].value
   

    try {      
  
      const credentials = signInWithEmailAndPassword(auth, email, password)

      console.log(auth.user);
      open.window("/Radicacion.html")
      if(auth.user != null){
        open.window("/Radicacion.html")
      }
    
    } catch (error) {
      window.alert("Password o correo Errado")
      console.log(error.code);
      if(error.code === "auth/wrong-password" ){
        window.alert("Password o correo Errado")

      }
    }

  })*/