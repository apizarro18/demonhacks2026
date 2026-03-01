// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getMessaging } from "firebase/messaging";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAra_eULhbKVA1E2sfssdn8FxbJXmMybNg",
  authDomain: "hackathon-notifications-1bb85.firebaseapp.com",
  projectId: "hackathon-notifications-1bb85",
  storageBucket: "hackathon-notifications-1bb85.firebasestorage.app",
  messagingSenderId: "581491889428",
  appId: "1:581491889428:web:d3b695e244b9ad3ebf9e01"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

export const messaging = getMessaging(app);