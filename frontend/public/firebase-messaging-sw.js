importScripts("https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/10.7.0/firebase-messaging-compat.js");

firebase.initializeApp({
  apiKey: "AIzaSyAra_eULhbKVA1E2sfssdn8FxbJXmMybNg",
  authDomain: "hackathon-notifications-1bb85.firebaseapp.com",
  projectId: "hackathon-notifications-1bb85",
  storageBucket: "hackathon-notifications-1bb85.firebasestorage.app",
  messagingSenderId: "581491889428",
  appId: "1:581491889428:web:d3b695e244b9ad3ebf9e01"
}); 

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function(payload) {
  self.registration.showNotification(payload.notification.title, {
    body: payload.notification.body,
  });
});