import React, { useContext } from 'react';
import { useSpring, animated } from 'react-spring';
import SignInDetailBoard from './signIn_detail_board/SigInDetailBoard';
import SignOutDetailBoard from './signout_detail_board/SignOutDetailBoard';
import OARDetailBoard from './OAR_detail_board/OARDetailBoard';
import EmergencyRoomDetail from './emergency_details/EmergencyRoomDetail';
import PlanHospDetail from './plan_hosp_detailing/PlanHospDetail';
import TopBlock from '../menu/TopBlock';
import DataContext from '../DataContext';
import { currentDatetime } from '../Feauters';
import '../menu/top_block.css';
import '../dashboard/dashboard_content.css';


function DetailBoard({ sign }) {


  const data = useContext(DataContext).kis;

  const kis = data.oar_numbers;
  const deads = kis[3].deads_nums[0];
  // Zipping and mapping data to pass as a props
  const arrived = Object.values(kis[0].arrived_nums[0]);
  const moved = Object.values(kis[1].moved_nums[0]);
  const current = Object.values(kis[2].current_nums[0]);

  const oar1 = [arrived[0],moved[0], current[0]];
  const oar2 = [arrived[1],moved[1], current[1]];
  const oar4 = [arrived[3], moved[3], current[3]];
  const oar5 = [arrived[4],moved[4], current[4]];


  const props = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    config: { duration: 700 },
  });

  let topBlockHeader;
  let content;

  if (sign === 'in') {
    content = <SignInDetailBoard />
    topBlockHeader = 'Детализация поступивших';
  } else if (sign === 'planHosp') {
    content = <PlanHospDetail />;
    topBlockHeader = 'Детализация плановой госпитализации';
  } else if (sign === 'emergencyRoom') {
    content = <EmergencyRoomDetail />;
    topBlockHeader = 'Детализация приёмного отделения';
  } else if (sign === 'out') {
    content = <SignOutDetailBoard />;
    topBlockHeader = 'Детализация выписанных';
  } else if (sign === 'oar') {
      content = <div className='detail_block'>
                <OARDetailBoard dept={'Отделение реанимации и интенсивной терапии № 1'} values={oar2} deads={deads.oar1_d} />
                <OARDetailBoard dept={'Отделение реанимации и интенсивной терапии № 2'} values={oar5} deads={deads.oar2_d} />          
                <OARDetailBoard dept={'Отделение реанимации и интенсивной терапии для больных с ОНМК'} values={oar1} deads={deads.oaronmk_d} />
                <OARDetailBoard dept={'Отделение реанимации и интенсивной терапии для больных с острым инфарктом миокарда'} values={oar4} deads={deads.oaroim_d} />
              </div>
    topBlockHeader = 'Детализация по реанимациям';
  };


  return (
    <>
    <TopBlock menu_point={sign} textContent={topBlockHeader} date={currentDatetime} />

    <animated.div className='dashboard' style={props}>
      {content}
    </animated.div>
    </>
  );
};
  
export default DetailBoard;