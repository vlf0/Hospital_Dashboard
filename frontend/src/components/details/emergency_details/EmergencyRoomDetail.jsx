import React, { useState } from 'react';
import { useSpring, animated } from 'react-spring';
import WaitingDetailTable from './tables/WaitingTable';
import RefuseDetailTable from './tables/RefuseTable';
import './emergency_detail_block.css';

const EmergencyRoomDetail = () => {
  const [activeTable, setActiveTable] = useState(null);

  const toggleTableVisibility = (table) => {
    setActiveTable(activeTable === table ? null : table);
  };

  const isRefuseTableVisible = activeTable === 'refuse';
  const isWaitingTableVisible = activeTable === 'waiting';

  const springProps = useSpring({
    height: (isRefuseTableVisible || isWaitingTableVisible) ? "auto" : 0,
    opacity: (isRefuseTableVisible || isWaitingTableVisible) ? 1 : 0,
    config: { tension: 200, friction: 25 }
  });

  return (
    <div className='emergency_detail_block'>
      <div className='refuse_detail_block'>
        <span className='detail_block_header'> Отказы </span>
        <div className='blocks_container'>
          <div className='separated_detail_block_X' onClick={() => toggleTableVisibility('refuse')}> 
            <div className='card_header'> Отказано </div>
            <div className='card_header'> 0 </div>
          </div>
        </div>

        <animated.div style={springProps}>
          {isRefuseTableVisible && <RefuseDetailTable />}
        </animated.div>
      </div>

      <div className='theLine'></div>

      <div className='wait_detail_block'>
        <span className='detail_block_header'> Ожидание более 120 минут </span>
        <div className='blocks_container'>
          <div className='separated_detail_block_X' onClick={() => toggleTableVisibility('waiting')}> 
            <div className='card_header'> Ожидание </div>
            <div className='card_header'> 0 </div>
          </div>
        </div>

        <animated.div style={springProps}>
          {isWaitingTableVisible && <WaitingDetailTable />}
        </animated.div>
      </div>

    </div> 
  );
};

export default EmergencyRoomDetail;
