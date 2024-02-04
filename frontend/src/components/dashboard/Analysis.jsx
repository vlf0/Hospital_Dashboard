import React, { useContext, useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useSpring, animated } from 'react-spring';
import isEqual from 'lodash/isEqual';
import ArrivedChart from '../charts/ArrivedChart';
import SignOutChart from '../charts/SignOutChart';
import DeadsChart from '../charts/DeadsChart';
import TopBlock from '../menu/TopBlock';
import BlockInfo from '../boards/BlockInfo';
import "../parent.css" 
import './dashboard_content.css'



function GetAnalysis() {


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
          <BlockInfo headerText='Поступившие' data={[110, 135, '18,5%']}/>
          <BlockInfo headerText='Госпитализировано' data={[90, 78, '12%']}/>
          <BlockInfo headerText='Отказано' data={[20, 60, '66,7%']}/>
          <BlockInfo headerText='Выписанные' data={[50, 30, '40%']}/>
          <BlockInfo headerText='Умершие' data={[10, 7, '33,3%']}/>
          <BlockInfo headerText='ОАР' data={[15, 22, '48%']}/>
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
