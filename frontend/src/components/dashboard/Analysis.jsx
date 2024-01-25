import React, { useContext, useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useSpring, animated } from 'react-spring';
import isEqual from 'lodash/isEqual';
import ArrivedChart from '../charts/ArrivedChart';
import SignOutChart from '../charts/SignOutChart';
import DeadsChart from '../charts/DeadsChart';
import TopBlock from '../menu/TopBlock';
import BlockInfo from '../boards/BlockInfo';
import GetData from '../GetData';
import DataContext from '../DataContext';
import "../parent.css" 
import './dashboard_content.css'


export let storedData = localStorage.getItem('apiData');
if (storedData) {
  // If data is in localStorage, use it directly
  storedData = (JSON.parse(storedData));
} else {
  // Otherwise, fetch data from API and store it in localStorage
  const fetchedData = GetData();
  
  localStorage.setItem('apiData', JSON.stringify(fetchedData));
};


function GetAnalysis() {

  const readyData = useContext(DataContext);
  console.log(readyData);
  
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
          <BlockInfo headerText='Поступившие' data={readyData.arrived}/>
          <BlockInfo headerText='Госпитализировано' data={readyData.hosp}/>
          <BlockInfo headerText='Отказано' data={readyData.refused}/>
          <BlockInfo headerText='Выписанные' data={readyData.signout}/>
          <BlockInfo headerText='Умершие' data={readyData.deads}/>
          <BlockInfo headerText='ОАР' data={readyData.reanimation}/>
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
