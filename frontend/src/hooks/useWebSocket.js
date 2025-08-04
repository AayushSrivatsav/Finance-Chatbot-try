import { useState, useEffect, useRef } from 'react';

export const useWebSocket = (url = 'ws://localhost:8000/ws/chat') => {
  const [isConnected, setIsConnected] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const wsRef = useRef(null);

  useEffect(() => {
    const connect = () => {
      try {
        const ws = new WebSocket(url);
        wsRef.current = ws;

        ws.onopen = () => {
          setIsConnected(true);
          setConnectionStatus('connected');
        };

        ws.onclose = () => {
          setIsConnected(false);
          setConnectionStatus('disconnected');
        };

        ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          setConnectionStatus('error');
        };

        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            // Handle incoming messages
            console.log('Received message:', data);
          } catch (error) {
            console.error('Failed to parse WebSocket message:', error);
          }
        };
      } catch (error) {
        console.error('Failed to connect to WebSocket:', error);
        setConnectionStatus('error');
      }
    };

    connect();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [url]);

  const sendMessage = (message) => {
    if (wsRef.current && isConnected) {
      wsRef.current.send(JSON.stringify(message));
    }
  };

  return {
    isConnected,
    connectionStatus,
    sendMessage
  };
}; 