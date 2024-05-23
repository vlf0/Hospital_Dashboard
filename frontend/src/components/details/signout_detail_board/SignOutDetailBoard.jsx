import React, { useState, useContext } from 'react';
import { useSpring, animated } from 'react-spring';
import DeadsChartDetail from './DeadsChartDetail';
import SignOutDetailTable from './SignOutDetailTable';
import DataContext from '../../DataContext';
import { getMainDMK } from '../../Feauters';
import '../signIn_detail_board/detail_blocks.css';



const SignOutDetailBoard = () => {

  const today = new Date();
  
  const data = useContext(DataContext);
  const dmkData = data.dmk.main_dmk;
  let dmk;
  dmk = getMainDMK(dmkData, today, 1);

  let kis = data.kis;
  kis = kis.signout[0];

  const [isDeadTableVisible, setIsDeadTableVisible] = useState(false);
  const toggleDeadTableVisibility = () => {
    setIsDeadTableVisible(!isDeadTableVisible);
  };

  // Spring effect ofappearance
  const springProps = useSpring({
    transform: `scale(${isDeadTableVisible ? 1 : 0})`,
    height: isDeadTableVisible ? "auto" : 0,
    opacity: isDeadTableVisible ? 1 : 0,
    config: { tension: 200, friction: 25 },
    delay: isDeadTableVisible ? 30 : 0,
    width: '-webkit-fill-available',
  });

  return (
    <div className='detail_block'>
      <span className='detail_block_header'> Общее количество </span>
      <div className='blocks_container'>
        <div className='separated_detail_block'> 
          <div className='card_header'> Выписано </div> 
          <div className='card_data'> { dmk.signout } </div>
        </div>
      </div>

      <span className='detail_block_header'> Исходы </span>
      <div className='blocks_container'>
        <div className='separated_detail_block_X' onClick={toggleDeadTableVisibility}> 
          <div className='card_header'> Смерть </div> 
          <div className='card_data'> { kis.deads } </div>
        </div>
        <div className='separated_detail_block'> 
          <div className='card_header'> Перевод в другую МО </div>
          <div className='card_data'> { kis.moved } </div>
        </div>
        <div className='separated_detail_block'>
           <div className='card_header'> Выписка </div>
           <div className='card_data'> { kis.signout }  </div>
        </div>
      </div>
      <animated.div style={springProps}>
          {isDeadTableVisible && <SignOutDetailTable />}
      </animated.div>
      <span className='detail_block_header'> Выписка по отделениям </span>
        <DeadsChartDetail data={kis}/>
    </div>
  );
};

export default SignOutDetailBoard;
