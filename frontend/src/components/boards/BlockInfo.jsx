import React from 'react';
import { useSpring, animated } from 'react-spring';
import './boards.css';



const BlockInfo = ({data, headerText}) => {

  // const data = [112, 136]

  const props = useSpring({
    from: { transform: 'scale(0)', opacity: 0 },
    to: { transform: data ? 'scale(1)' : 'scale(0)', opacity: data ? 1 : 0 },
    config: { duration: 500 },
  });

  const imagePath = data && data[0] > data[1] ? '/images/dynamic_high.png' : '/images/dynamic_low.png';

  return (
    <animated.div className='boards' style={props}>
      {data ? (
        <>
          <span className='headers'>{headerText}</span>
          <p className='text_data'>{data[0]}</p>
          <img src={imagePath} className='logo' alt=''/>
          <p className='text_data'>{data[1]}</p>
          
          {/* Add more properties as needed */}
        </>
      ) : (
        <p>Loading...</p>
      )}
    </animated.div>
  );

};

export default BlockInfo;
