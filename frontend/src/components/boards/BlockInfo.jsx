import React from 'react';
import { useSpring, animated } from 'react-spring';
import './boards.css';



const BlockInfo = ({data, headerText}) => {


  const props = useSpring({
    from: { transform: 'scale(0)', opacity: 0 },
    to: { transform: data ? 'scale(1)' : 'scale(0)', opacity: data ? 1 : 0 },
    config: { duration: 500 },
  });

  const imagePath = data && data[0] > data[1] ? '/images/a_up2.svg' : '/images/a_down2.svg';
  const reverseImagePath = data && data[1] > data[0] ? '/images/a_up2.svg' : '/images/a_down2.svg';

  return (
    <animated.div className='boards' style={props}>
      <>
        <span className='headers'>{headerText}</span>
        <p className='text_data'>{data[0]}</p>
          {['Отказано', 'Умершие', 'ОАР'].includes(headerText) ? (
            <img src={reverseImagePath} className='logo' alt=''/>
            ) : (
            <img src={imagePath} className='logo' alt=''/>
          )}
        <span className='percent'>{data[2]}</span>
        <p className='text_data'>{data[1]}</p>

        {/* Add more properties as needed */}
      </>
    </animated.div>
  );

};

<<<<<<< HEAD
export default BlockInfo;
=======
export default BlockInfo;
>>>>>>> 07e3ae2a2bd5da94925016810338cd63f70ae8b8
