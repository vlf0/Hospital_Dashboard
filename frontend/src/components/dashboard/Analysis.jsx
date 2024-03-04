import React, { useContext } from 'react';
import { useLocation } from 'react-router-dom';
import { useSpring, animated } from 'react-spring';
import ArrivedChart from '../charts/ArrivedChart';
import SignOutChart from '../charts/SignOutChart';
import DeadsChart from '../charts/DeadsChart';
import TopBlock from '../menu/TopBlock';
import BlockInfo from '../boards/BlockInfo';
import DataContext from '../DataContext';
import { Persents, CustomMap } from '../Feauters';
import "../parent.css" 
import './dashboard_content.css'


function GetAnalysis() {

  const props = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    config: { duration: 1000 },
  });

  const location = useLocation();
  
  const main_dmk = useContext(DataContext).dmk.main_dmk;

  const currentDay = main_dmk[main_dmk.length - 1];
  const yesterday = main_dmk[main_dmk.length - 2];

  const arrived = CustomMap(currentDay.arrived, yesterday.arrived)
  const hosp = CustomMap(currentDay.hosp, yesterday.hosp)
  const refused = CustomMap(currentDay.refused, yesterday.refused)
  const signout = CustomMap(currentDay.signout, yesterday.signout)
  const deads = CustomMap(currentDay.deads, yesterday.deads)
  const reanimation = CustomMap(currentDay.reanimation, yesterday.reanimation)

  return (
    <> 

      {/* <h1>{data.arrived}</h1> */}
      <TopBlock textContent={'Оперативная сводка ГКБ Им. Демихова'}/>
      <animated.div className='dashboard' style={1}>
        <div className='board-cards'>
          <BlockInfo headerText='Поступившие' data={arrived}/>
          <BlockInfo headerText='Госпитализировано' data={hosp}/>
          <BlockInfo headerText='Отказано' data={refused}/>
          <BlockInfo headerText='Выписанные' data={signout}/>
          <BlockInfo headerText='Умершие' data={deads}/>
          <BlockInfo headerText='ОАР' data={reanimation}/>
        </div>
        <div className='board-charts'>
          <ArrivedChart />
          <SignOutChart /> 
          <DeadsChart />
        </div>
      </animated.div>
    </>
  );
}

export default GetAnalysis;
