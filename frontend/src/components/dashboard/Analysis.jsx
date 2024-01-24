import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useSpring, animated } from 'react-spring';
import ArrivedChart from '../charts/ArrivedChart';
import SignOutChart from '../charts/SignOutChart';
import DeadsChart from '../charts/DeadsChart';
import TopBlock from '../menu/TopBlock';
import BlockInfo from '../boards/BlockInfo';
import GetData from '../GetData';
import "../parent.css" 
import './dashboard_content.css'




function GetAnalysis() {

  const todayData = GetData();


  const location = useLocation();


  const props = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    config: { duration: 1000 },
  });

  return (
    <> 

      {/* <h1>{data.arrived}</h1> */}

      <TopBlock textContent={'Оперативная сводка ГКБ Им. Демихова'}/>
      <animated.div className='dashboard' style={props}>
        <div className='board-cards'>
          <BlockInfo headerText='Поступившие' data={todayData.arrived}/>
          <BlockInfo headerText='Госпитализировано' data={todayData.hosp}/>
          <BlockInfo headerText='Отказано' data={todayData.refused}/>
          <BlockInfo headerText='Выписанные' data={todayData.signout}/>
          <BlockInfo headerText='Умершие' data={todayData.deads}/>
          <BlockInfo headerText='ОАР' data={todayData.reanimation}/>
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
