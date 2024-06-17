import React, { useContext, useEffect, useState  } from 'react';
import { mainSocket } from '../../';
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
import '../parent.css';
import './dashboard_content.css';


function GetAnalysis() {

  const props = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
    config: { duration: 700 },
  });
  
  const main_dmk = useContext(DataContext).dmk.main_dmk;

  const currentDay = getMainDMK(main_dmk, 'today');
  const yesterday = getMainDMK(main_dmk, 'yesterday');

  const arrived = CustomMap(currentDay, yesterday, 'arrived')
  const hosp = CustomMap(currentDay, yesterday, 'hosp')
  const refused = CustomMap(currentDay, yesterday, 'refused')
  const signout = CustomMap(currentDay, yesterday, 'signout')
  const deads = CustomMap(currentDay, yesterday, 'deads')
  const reanimation = CustomMap(currentDay, yesterday, 'reanimation')

  const [reload, setReload] = useState(false);

  const fetchDataFromApi = async () => {
    try {
      const response = await fetch('http://10.123.8.17:9000/api/v1/main_data/');
      const newData = await response.json();

      // Update sessionStorage with the new data
      sessionStorage.setItem('main_data', JSON.stringify(newData));

      // Trigger re-render by toggling the reload state
      setReload(prevReload => !prevReload);
    } catch (error) {
      console.error('Error fetching new data:', error);
    }
  };

  useEffect(() => {
    mainSocket.onmessage = () => {
      fetchDataFromApi();
    };
  }, [reload]);

  return (
    <> 

      {/* <h1>{data.arrived}</h1> */}
      <TopBlock textContent={'Оперативная сводка'} date={currentDatetime}/>
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
          <ArrivedChart key={reload}/>
          <SignOutChart /> 
          <DeadsChart />
        </div>
      </animated.div>
    </>
  );
}

export default GetAnalysis;
