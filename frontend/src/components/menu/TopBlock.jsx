import React, { useState } from 'react';
import { useSpring, animated } from 'react-spring';
import MenuUnit from './MenuUnit';
import Header from '../details/Header';
import './top_block.css';


const arrivedpoint = 'Поступившие';
const outpoint = 'Выписанные';
const oarpoint = 'ОАР и ОРИТ';
const point_list = ['in', 'out', 'oar', 'details']


const TopBlock = ({ textContent, menu_point, date }) => {
  const [isHovered, setHovered] = useState(false);

  const handleToggleHover = () => {
    setHovered(!isHovered);
  };

  const props = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    config: { duration: 700 },
  });

  return (

    <animated.div
      className='parent_block'
      style={props}>

      <div className='logo_with_header'>
        <div className='empty_block'>
          <img className='dmklogo' src='/images/gkblogo.png' alt=''></img>
        </div>
        <Header textHeader={textContent} date={date}/>
        <div className='empty_block'> </div>
      </div>

      <div className='top_block'>
        <div className='dropdown' >
          {point_list.includes(menu_point)  && (
            <MenuUnit point={'Главная'} to='/' />
          )}
          <MenuUnit point={arrivedpoint} to='/arrived_detail' />
          <MenuUnit point={outpoint} to='/signout_detail' />
          <MenuUnit point={oarpoint} to='/OAR_detail' />
        </div>
      </div>
    </animated.div>
  );
};

export default TopBlock;
