import React, { createContext, useContext, useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useSpring, animated } from 'react-spring';
import isEqual from 'lodash/isEqual';
import ArrivedChart from '../charts/ArrivedChart';
import SignOutChart from '../charts/SignOutChart';
import DeadsChart from '../charts/DeadsChart';
import TopBlock from '../menu/TopBlock';
import BlockInfo from '../boards/BlockInfo';
import GetData from '../GetData';
import { useData } from '../DataContext';
import "../parent.css" 
import './dashboard_content.css'
import { set } from 'lodash';



function GetAnalysis() {

  const { data, setNewData } = useData();


  const useEffect = (() => {
    // Check if data is already available in localStorage
    const storedData = localStorage.getItem('myAppData');

    if (storedData) {
      // If data is in localStorage, use it directly
      setNewData(JSON.parse(storedData));
    } else {
      // Otherwise, fetch data from API and store it in localStorage
      const fetchedData = GetData();
      setNewData(fetchedData);
      localStorage.setItem('myAppData', JSON.stringify(fetchedData));
    }
  }, [setNewData]);

  console.log(data);

  const ex = {t1: 'test1',t2: 'test2'}
  localStorage.setItem('test', JSON.stringify(ex));
  const data1 = localStorage.getItem('test');
  const r_data = JSON.parse(data1)

  console.log(r_data);





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
          <BlockInfo headerText='Поступившие' data={[2,5,7]}/>
          <BlockInfo headerText='Госпитализировано' data={[3,7,5]}/>
          {/* <BlockInfo headerText='Отказано' data={todayData.refused}/>
          <BlockInfo headerText='Выписанные' data={todayData.signout}/>
          <BlockInfo headerText='Умершие' data={todayData.deads}/>
          <BlockInfo headerText='ОАР' data={todayData.reanimation}/>
        </div>
        <div className='board-charts'>
          <ArrivedChart data={todayData.arrivedArray}/>
          <SignOutChart data={todayData.signOutArray} />
          <DeadsChart data={todayData.deadsArray} /> */}
        </div>
      </animated.div>
    </>
  );
}

export default GetAnalysis;
