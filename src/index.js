import {loginEmailPassword} from '../js/Config/ConfigFirebase.js'


/*window.addEventListener('DOMContentLoaded', async () =>{
    const querySnapshot = await getTask();
    
    querySnapshot.forEach(element => {
        console.log(element.data());
    });

})*/



const taskForm = document.getElementById("login-form")

taskForm.addEventListener('submit', (e)=>{
    e.preventDefault()
    Notification.requestPermission().then(e)

    const email = taskForm['email-login']
    const password = taskForm['password-login']

    console.log(email.value, password.value);
    loginEmailPassword(email.value, password.value)

    //saveTask(email.value, password.value)
})


/*

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-analytics.js";

import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-auth.js"
import { getFirestore, collection, getDoc, getDocs} from "https://www.gstatic.com/firebasejs/10.6.0/firebase-firestore.js"
//import{getFirestore, collection, getDocs, getDoc} from "firebase/firestore"
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
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

const auth = getAuth(app);
const db = getFirestore(app)
const todosCol = collection(db, "Visitadores")
const snapshot = await getDocs(todosCol)

console.log(snapshot)



//const db = getFirestore(firebaseConfig)

//db.collection('todos').getDocs()

//const todosCol = collection(db, 'todos')

//const snapshot = await getDocs(todosCol)

onAuthStateChanged(auth, user => {
    if(user =! null){
        console.log('Logged in!')
    }else{
        console.log('No User')
    }
});

*/