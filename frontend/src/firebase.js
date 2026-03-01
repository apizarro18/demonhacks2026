import { initializeApp } from "firebase/app";
import { getMessaging } from "firebase/messaging";

const firebaseConfig = {
  apiKey: "AIzaSyAra_eULhbKVA1E2sfssdn8FxbJXmMybNg",
  authDomain: "hackathon-notifications-1bb85.firebaseapp.com",
  projectId: "hackathon-notifications-1bb85",
  storageBucket: "hackathon-notifications-1bb85.firebasestorage.app",
  messagingSenderId: "581491889428",
  appId: "1:581491889428:web:d3b695e244b9ad3ebf9e01"
};

const app = initializeApp(firebaseConfig);

// Register Service Worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/firebase-messaging-sw.js')
    .catch(err => console.error('SW registration failed:', err));
}

export const messaging = getMessaging(app);