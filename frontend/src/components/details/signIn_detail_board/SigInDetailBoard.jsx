import React, { useContext, useEffect, useState  } from "react";
import SignInDetailTable from "./SignInDetailTable";
import DataContext from "../../DataContext";
import { mainSocket } from "../../..";
import { getMainDMK } from "../../Feauters";
import './detail_blocks.css';
import './signin_table.css';



const SignInDetailBoard = () => {

  const today = new Date();


  const data = useContext(DataContext);
  const kis = data.kis[0].arrived[0];
  const dmkData = data.dmk.main_dmk;

  let main_dmk;
  main_dmk = getMainDMK(dmkData, today, 1);
  

  const [reload, setReload] = useState(false);

  const fetchDataFromApi = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/main_data/');
      const newData = await response.json();

      // Update sessionStorage with the new data
      sessionStorage.setItem('data', JSON.stringify(newData));

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
    <div className='detail_block'>
      <span className='detail_block_header'> Обратившиеся </span>
      <div className='blocks_container'>
        <div className='separated_detail_block'> 
          <p> Отказано </p> {main_dmk.refused} 
        </div>
        <div className='separated_detail_block'>
        <p> Госпитализировано </p> {main_dmk.hosp}
        </div>
      </div>
      <span className='detail_block_header'> Госпитализировано по каналам </span>
      <div className='blocks_container'>
        <div className='separated_detail_block'> 
          <p> 103 </p> {kis.ch103} </div>
        <div className='separated_detail_block'>
           <p> Поликлиника </p> {kis.clinic_only} </div>
        <div className='separated_detail_block'>
           <p> 103 Поликлиника </p> {kis.ch103_clinic} </div>
        <div className='separated_detail_block'>
           <p> Самотёк </p> {kis.singly} </div>
        <div className='separated_detail_block'>
           <p> План </p> {kis.plan} </div>
      </div>
      <span className='detail_block_header'> Госпитализировано в статусе </span>
      <div className='blocks_container'>
        <div className='separated_detail_block'>
          <p> ЗЛ </p> {kis.ZL} </div>
        <div className='separated_detail_block'>
          <p> Иногородние </p> {kis.foreign} </div>
        <div className='separated_detail_block'> 
          <p> НР </p> {kis.nr} </div>
        <div className='separated_detail_block'>  
          <p> НИЛ </p> {kis.nil} </div>
        <div className='separated_detail_block'>  
          <p> ДМС </p> {kis.dms} </div>
        <div className='separated_detail_block'>  
          <p> Не указано </p> {kis.undefined} </div>
      </div>
      <SignInDetailTable key={reload}/>
      {/* <button className="reload_button" onClick={fetchDataFromApi}>Обновить планы</button> */}



    </div>
  );
};

export default SignInDetailBoard;
