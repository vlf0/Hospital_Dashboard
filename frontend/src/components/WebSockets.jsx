import { useEffect } from 'react';

const useWebSocket = (onMessageCallback) => {
  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8001/ws/notifications/');

    socket.onopen = () => {
        console.log('connected')
    };

    socket.onmessage = () => {
      onMessageCallback(); // Call the provided callback without passing data
    };

    socket.onerror = (event) => {
      console.error('error');

    };

    return () => {
      socket.close();
    };
  }, [onMessageCallback]);
};

export default useWebSocket;







// useEffect(() => {
//     const socket = new WebSocket('ws://localhost:8001/ws/notifications/');

//     socket.onmessage = (event) => {
//       console.log(event);
//       const data = JSON.parse(event.data);
//       console.log('WebSocket message received:', data);
//       // Call your function when a message is received
//       handleWebSocketMessage(data);
//     };

//     socket.onerror = (event) => {
//       console.error('WebSocket error:', event);
//     };

//     // Cleanup the WebSocket connection when the component unmounts
//     return () => {
//       socket.close();
//     };
//   }, []);