import React, { useState } from 'react';
import { useSpring, animated } from 'react-spring';
import { useLocation } from 'react-router-dom';
import MenuUnit from './MenuUnit';
import Header from '../details/Header';
import './top_block.css';


const menuUnitsMapping = {
    'arrived': 'Поступившие',
    'emergency': 'Приёмное отделение',
    'plan_hosp': 'Плановая госпитализация',
    'signout': 'Выписанные',
    'oar': 'Реанимация'
}


const TopBlock = ({ textContent, menu_point, date }) => {
  const [isHovered, setHovered] = useState(false);
  const location = useLocation();

  const handleToggleHover = () => {
    setHovered(!isHovered);
  };

  const isDefaultAddress = location.pathname !== '/';

  const props = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    config: { duration: 700 },
  });

  return (

    <animated.div
      className='parent_block sticky-top'
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
          {isDefaultAddress && <MenuUnit point={'Главная'} to='/' />}

          {Object.keys(menuUnitsMapping).map((key, index) => {
            const detailPageURL = `/${key}_detail`;
            if (location.pathname !== detailPageURL) {
              return (
                <MenuUnit key={index} point={menuUnitsMapping[key]} to={detailPageURL} />
              );
            }
            return null; // Return null to exclude this menu point from rendering
          })}

        </div>
      </div>
    </animated.div>
  );
};

export default TopBlock;
