import React, { useState } from "react";
import { useSpring, animated } from "react-spring";
import DeadsChartDetail from "./DeadsChartDetail";
import SignOutDetailTable from "./SignOutDetailTable";
import '../signIn_detail_board/detail_blocks.css';

const signOutCount = 63;
const deadCount = 9;
const moveCount = 18;

const SignOutDetailBoard = ({ combinedData, profiles }) => {

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
      <span className='detail_block_header'> Исходы </span>
      <div className='blocks_container'>
        <div className='separated_detail_block_X' onClick={toggleDeadTableVisibility}>
          Смерть <br /><br /> {deadCount}
        </div>
        <div className='separated_detail_block'> Перевод в другую МО <br /><br /> {moveCount} </div>
        <div className='separated_detail_block'> Выписка <br /><br /> {signOutCount} </div>
      </div>
      <span className='detail_block_header'> Выписка по отделениям </span>
      <DeadsChartDetail profiles={profiles}/>
      <animated.div style={springProps}>
          {isDeadTableVisible && <SignOutDetailTable />}
      </animated.div>
    </div>
  );
};

export default SignOutDetailBoard;
