import React, { useState, useEffect } from "react";
import { useSpring, animated } from 'react-spring';
import noConnection from './noConnection.css'

const NoConnection = () => {
  const [loading, setLoading] = useState(true);

  // Simulate loading by hiding the loading spinner after 2 seconds
  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  const [spinnerVisible, setSpinnerVisible] = useState(true);

  const spinnerSpring = useSpring({
    from: { transform: 'rotate(0deg)' },
    to: { transform: 'rotate(360deg)' },
    loop: true,
    config: { duration: 1500 },
  });

  const errorSpring = useSpring({
    from: { opacity: 0, transform: 'translateY(100%)' },
    to: { opacity: loading ? 0 : 1, transform: loading ? 'translateY(100%)' : 'translateY(0%)' },
  });

  useEffect(() => {
    // When loading is complete, hide the spinner immediately
    if (!loading) {
      setSpinnerVisible(false);
    }
  }, [loading]);

  return (
    <>
      <div className="top_block">
        <h1 className="conn_header">
          Dashboard <br/> ГКБ Демихова 
        </h1>
      </div>
      <div className="center-content">
        {spinnerVisible && (
          <animated.div style={{ ...spinnerSpring, display: 'inline-block' }}>
            <div
              style={{
                width: '50px',
                height: '50px',
                borderRadius: '50%',
                border: '12px solid #bdc8db',
                borderTop: '12px solid #3498db',
                animation: 'spin 1s linear infinite',
              }}
            />
          </animated.div>
        )}
        <animated.div style={errorSpring}>
          <div className="error_text">
            Отсутствует подключение к серверу. Обратитесь к администратору.
          </div>  
        </animated.div>
      </div>
    </>
  );
}

export default NoConnection;
