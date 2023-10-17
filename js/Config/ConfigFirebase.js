  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.0/firebase-app.js";
  import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.22.0/firebase-analytics.js";
  import { getAuth, onAuthStateChanged, signInWithPopup, GoogleAuthProvider, signInWithEmailAndPassword} from "https://www.gstatic.com/firebasejs/9.22.0/firebase-auth.js";
  //import { getFirestore, collection, getDoc, getDocs} from "https://www.gstatic.com/firebasejs/9.22.0/firebase-getFirestore.js";
//import { user } from "firebase-functions/v1/auth";
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional

  const btnLoginGoogle = document.getElementById("login-google-button")
  const LogInForm = document.getElementById("login-form")

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

  const auth = getAuth(app)

  
  onAuthStateChanged(auth, user => {
    if(user =! null){
      console.log('Logged in!');
      console.log(auth);
    } else {
      console.log('No User');
    }
  })

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

  })