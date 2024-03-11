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

