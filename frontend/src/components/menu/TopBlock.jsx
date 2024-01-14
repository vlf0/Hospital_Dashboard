import React, { useState } from 'react';
import { useSpring, animated } from 'react-spring';
import MenuUnit from './MenuUnit';
import './top_block.css';


const arrivedpoint = 'Поступившие';
const outpoint = 'Выписанные';
const oarpoint = 'ОАР и ОРИТ';


const TopBlock = () => {
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
    height: isHovered ? 100 : 0,
    opacity: isHovered ? 1 : 0,
    config: { tension: 200, friction: 25 },
    delay: isHovered ? 30 : 0,
  });

  const textContent = 'Оперативная сводка ГКБ им. Демихова';
  const currentDatetime = new Date().toLocaleDateString('ru-RU');

  return (
    <animated.div
      className='top_block'
      style={props}
      onMouseEnter={handleToggleHover}
      onMouseLeave={handleToggleHover}
    >
      <p className='main_header'>{textContent}</p>
      <span className='now_date'>по состоянию на {currentDatetime}</span>

      {/* Dropdown */}
      <animated.div className='dropdown' style={dropdownProps}>
        {/* Add your dropdown content here */}
        <MenuUnit point={arrivedpoint} to='/arrived_detail' />

        <MenuUnit point={outpoint} to='/signout_detail' />

        <MenuUnit point={oarpoint} to='/OAR_detail' />
        {/* <MenuUnit point={}/> */}
      </animated.div>
    </animated.div>
  );
};

export default TopBlock;
