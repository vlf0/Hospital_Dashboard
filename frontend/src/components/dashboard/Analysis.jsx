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

  const data = GetData();
  console.log(data);

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
          <BlockInfo headerText='Поступившие' data={[data.arrived, 10]}/>
          <BlockInfo headerText='Госпитализировано' data={[data.hosp, 88]}/>
          <BlockInfo headerText='Отказано' data={[data.refused, 18]}/>
          <BlockInfo headerText='Выписанные' data={[data.signout, 62]}/>
          <BlockInfo headerText='Умершие' data={[data.deads, 7]}/>
          <BlockInfo headerText='ОАР' data={[data.reanimation, 19]}/>
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
