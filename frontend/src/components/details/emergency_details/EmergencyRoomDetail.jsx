import React, { useState, useMemo } from "react";
import { useSpring, animated } from "react-spring";
import WaitingDetailTable from "./tables/WaitingTable";
import RefuseDetailTable from "./tables/RefuseTable";
import NewTable from "./tables/RefuseDetailTable";
import './emergency_detail_block.css';

const EmergencyRoomDetail = () => {
  const [isRefuseTableVisible, setIsRefuseTableVisible] = useState(false);
  const [isWaitingTableVisible, setIsWaitingTableVisible] = useState(false);
  const [selectedDoctor, setSelectedDoctor] = useState(null);

  const toggleRefuseTableVisibility = () => {
    setIsRefuseTableVisible(!isRefuseTableVisible);
  };

  const toggleWaitingTableVisibility = () => {
    setIsWaitingTableVisible(!isWaitingTableVisible);
  };

  const handleRowClick = (doctorName) => {
    setSelectedDoctor(doctorName);
  };

  const springPropsRefuse = useSpring({
    transform: `scale(${isRefuseTableVisible ? 1 : 0})`,
    height: isRefuseTableVisible ? "auto" : 0,
    opacity: isRefuseTableVisible ? 1 : 0,
    config: { tension: 200, friction: 25 },
    delay: isRefuseTableVisible ? 30 : 0,
    width: '-webkit-fill-available',
  });

  const springPropsWaiting = useSpring({
    transform: `scale(${isWaitingTableVisible ? 1 : 0})`,
    height: isWaitingTableVisible ? "auto" : 0,
    opacity: isWaitingTableVisible ? 1 : 0,
    config: { tension: 200, friction: 25 },
    delay: isWaitingTableVisible ? 30 : 0,
    width: '-webkit-fill-available',
  });

  const memoizedRefuseTable = useMemo(() => {
    return isRefuseTableVisible && <RefuseDetailTable onRowClick={handleRowClick} />;
  }, [isRefuseTableVisible]);

  const memoizedWaitingTable = useMemo(() => {
    return isWaitingTableVisible && <WaitingDetailTable />;
  }, [isWaitingTableVisible]);

  return (
    <>
      <div className='emergency_detail_block'>
        <div className='refuse_detail_block'>
          <span className='detail_block_header'> Отказы </span>
          <div className='blocks_container'>
            <div className='separated_detail_block_X' onClick={toggleRefuseTableVisibility}> 
              <div className='card_header'> Отказано </div>
              <div className='card_header'> 0 </div>
            </div>
          </div>
          <animated.div style={springPropsRefuse}>
            {memoizedRefuseTable}
          </animated.div>
          {selectedDoctor && <NewTable doctorName={selectedDoctor} />}
        </div>

        <div className='theLine'></div>

        <div className='wait_detail_block'>
          <span className='detail_block_header'> Ожидание более 120 минут </span>
          <div className='blocks_container'>
            <div className='separated_detail_block_X' onClick={toggleWaitingTableVisibility}> 
              <div className='card_header'> Ожидание </div>
              <div className='card_header'> 0 </div>
            </div>
          </div>
          <animated.div style={springPropsWaiting}>
            {memoizedWaitingTable}
          </animated.div>
        </div>
      </div>

    </>
  );
};

export default EmergencyRoomDetail;
