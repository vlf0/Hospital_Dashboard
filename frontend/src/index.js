import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { WebSocketProvider } from './components/websocket/WebSocketContext';

export const mainSocket = new WebSocket('ws://localhost:8000/ws/notifications/');


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <WebSocketProvider socket={mainSocket}>
    <App />
  </WebSocketProvider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals

