import React, { useContext } from 'react';
import { useSpring, animated } from 'react-spring';
import SignInDetailBoard from './signIn_detail_board/SigInDetailBoard';
import SignOutDetailBoard from './signout_detail_board/SignOutDetailBoard';
import OARDetailBoard from './OAR_detail_board/OARDetailBoard';
import TopBlock from '../menu/TopBlock';
import DataContext from '../DataContext';
import '../menu/top_block.css';
import '../dashboard/dashboard_content.css';





const profiles = ['Кардио', 'Невро', 'Терапия']; //List of depts from KISDB
const arrivedFacts = [10, 15, 8]; //List of fact arrived patients
const combinedData = profiles.map((profile, index) => ({ профиль: profile, план: arrivedFacts[index] })); //Mapping two lists above

function DetailBoard({ sign }) {

  const readyData = useContext(DataContext);

  const props = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    config: { duration: 700 },
  }); 

  let topBlockHeader;
  let content;

  if (sign === 'in') {
    content = 
    <SignInDetailBoard combinedData={combinedData} />
    topBlockHeader = 'Детализация поступивших';
  } else if (sign === 'out') {
    content = <SignOutDetailBoard profiles={profiles} />;
    topBlockHeader = 'Детализация выписанных';
  } else if (sign === 'oar') {
    content = <div className='detail_block'>
              <OARDetailBoard dept={'ОРИТ №1'} values={[readyData.reanimation[0],15,20]} /> 
              <OARDetailBoard dept={'ОРИТ №2'} values={[33,19,24]} />
              <OARDetailBoard dept={'ОРИТ №3'} values={[33,19,24]} />              
              </div>;
    topBlockHeader = 'Детализация по реанимациям';
  };


  return (
    <>
    {/* <animated.div
    className='top_block'
    style={props}>
      <Header textHeader={textHeader} currentDatetime={currentDatetime}/>
    </animated.div> */}
    <TopBlock menu_point={sign} textContent={topBlockHeader} />
    
    <animated.div className='dashboard' style={props}>
      {content}
    </animated.div>
    </>
  );
}
  
export default DetailBoard;