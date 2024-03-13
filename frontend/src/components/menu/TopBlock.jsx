import React, { useState } from 'react';
import { useSpring, animated } from 'react-spring';
import MenuUnit from './MenuUnit';
import Header from '../details/Header';
import './top_block.css';


const arrivedpoint = 'Поступившие';
const outpoint = 'Выписанные';
const oarpoint = 'ОАР и ОРИТ';
const point_list = ['in', 'out', 'oar']


const TopBlock = ({ textContent, menu_point }) => {
  const [isHovered, setHovered] = useState(false);

  const handleToggleHover = () => {
    setHovered(!isHovered);
  };

  const props = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    config: { duration: 700 },
  });

  const dropdownProps = useSpring({
    transform: `scale(${isHovered ? 1 : 0})`,
    height: isHovered ? 90 : 0,
    opacity: isHovered ? 1 : 0,
    config: { tension: 200, friction: 25 },
    delay: isHovered ? 30 : 0,
  });


  return (
    <animated.div
      className='top_block'
      style={props}
      onMouseEnter={handleToggleHover}
      onMouseLeave={handleToggleHover}
    >
      {/* <p className='main_header'>{textContent}</p>
      <span className='now_date'>по состоянию на {currentDatetime}</span> */}
      <Header textHeader={textContent}/>

      {/* Dropdown */}
      <animated.div className='dropdown' style={dropdownProps}>
        {point_list.includes(menu_point)  && (
          <MenuUnit point={'Главная'} to='/' />
        )}
        <MenuUnit point={arrivedpoint} to='/arrived_detail' />
        <MenuUnit point={outpoint} to='/signout_detail' />
        <MenuUnit point={oarpoint} to='/OAR_detail' />




      </animated.div>
    </animated.div>
  );
};

export default TopBlock;
