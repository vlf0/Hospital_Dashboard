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


// export function GetLocalData() {

//   const storedData = sessionStorage.getItem('data');
//   if (storedData) {
//   console.log(storedData);
//   storedData = (JSON.parse(storedData));
//   console.log(storedData);
//   } 
//   else {
//   const fetchedData = GetData();
//   console.log(fetchedData);
//   if (fetchedData) {
//     sessionStorage.setItem('data', JSON.stringify(fetchedData))
//     console.log(JSON.stringify(storedData));
//   };
// };

//   return {storedData};
// };





function GetAnalysis() {


  const readyData = useContext(DataContext);

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
          <BlockInfo headerText='Поступившие' data={(readyData ? readyData.arrived : null)}/>
          <BlockInfo headerText='Госпитализировано' data={(readyData ? readyData.hosp : null)}/>
          <BlockInfo headerText='Отказано' data={(readyData ? readyData.refused : null)}/>
          <BlockInfo headerText='Выписанные' data={(readyData ? readyData.signout : null)}/>
          <BlockInfo headerText='Умершие' data={(readyData ? readyData.deads : null)}/>
          <BlockInfo headerText='ОАР' data={(readyData ? readyData.reanimation : null)}/>
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
