import React, { useContext } from 'react';
import { useLocation } from 'react-router-dom';
import { useSpring, animated } from 'react-spring';
import ArrivedChart from '../charts/ArrivedChart';
import SignOutChart from '../charts/SignOutChart';
import DeadsChart from '../charts/DeadsChart';
import TopBlock from '../menu/TopBlock';
import BlockInfo from '../boards/BlockInfo';
import DataContext from '../DataContext';
import { CustomMap } from '../Feauters';
import { currentDatetime } from '../Feauters';
import { getMainDMK } from '../Feauters';
import { getYesterdayDate } from '../Feauters';
import "../parent.css" 
import './dashboard_content.css'


function GetAnalysis() {

  const today = new Date();
  const yesterDay = getYesterdayDate();


  const props = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    config: { duration: 700 },
  });

  const location = useLocation();
  
  const main_dmk = useContext(DataContext).dmk.main_dmk;

  const currentDay = getMainDMK(main_dmk, today, 1);
  const yesterday = getMainDMK(main_dmk, yesterDay, 2);

  const arrived = CustomMap(currentDay, yesterday, 'arrived')
  const hosp = CustomMap(currentDay, yesterday, 'hosp')
  const refused = CustomMap(currentDay, yesterday, 'refused')
  const signout = CustomMap(currentDay, yesterday, 'signout')
  const deads = CustomMap(currentDay, yesterday, 'deads')
  const reanimation = CustomMap(currentDay, yesterday, 'reanimation')

  return (
    <> 

      {/* <h1>{data.arrived}</h1> */}
      <TopBlock textContent={'Оперативная сводка ГКБ Им. Демихова'} date={currentDatetime}/>
      <animated.div className='main_dashboard' style={props}>
        <div className='board-cards'>
          <div className='cards_line'>
            <BlockInfo headerText='Поступившие' data={arrived}/>
            <BlockInfo headerText='Госпитализировано' data={hosp}/>
            <BlockInfo headerText='Отказано' data={refused}/>
          </div>
          <div className='cards_line'>
            <BlockInfo headerText='Выписанные' data={signout}/>
            <BlockInfo headerText='Умершие' data={deads}/>
            <BlockInfo headerText='ОАР' data={reanimation}/>
          </div>
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
