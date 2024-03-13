import React, { createContext, useContext, useMemo } from 'react';

export const WebSocketContext = createContext();

export const WebSocketProvider = ({ children, socket }) => {
  const memoizedSocket = useMemo(() => socket, [socket]);

  return (
    <WebSocketContext.Provider value={memoizedSocket}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocketContext = () => {
  return useContext(WebSocketContext);
};
