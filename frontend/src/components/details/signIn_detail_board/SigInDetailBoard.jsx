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
  const kis = data.kis.arrived[0];
  const dmkData = data.dmk.main_dmk;

  let main_dmk;
  main_dmk = getMainDMK(dmkData, today, 1);
  

  const [reload, setReload] = useState(false);

  const fetchDataFromApi = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/main_data/');
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
    <div className='detail_block'>
      <span className='detail_block_header'> Обратившиеся </span>
      <div className='blocks_container'>
        <div className='separated_detail_block'> 
          <div className='card_header'> Отказано </div>
          <div className='card_header'> {main_dmk.refused} </div>
        </div>

        <div className='separated_detail_block'> 
          <div className='card_header'> Госпитализировано </div>
          <div className='card_header'> {main_dmk.hosp} </div>
        </div>
      </div>

      <span className='detail_block_header'> Госпитализировано по каналам </span>
      <div className='blocks_container'>
        <div className='separated_detail_block'> 
          <div className='card_header'> 103 </div>
          <div className='card_header'> {kis.ch103} </div>
        </div>
        <div className='separated_detail_block'> 
          <div className='card_header'> Поликлиника </div>
          <div className='card_header'> {kis.clinic_only} </div>
        </div>
        <div className='separated_detail_block'> 
          <div className='card_header'> 103 Поликлиника </div>
          <div className='card_header'> {kis.ch103_clinic} </div>
        </div>
        <div className='separated_detail_block'> 
          <div className='card_header'> Самотек </div>
          <div className='card_header'> {kis.singly} </div>
        </div>
        <div className='separated_detail_block'> 
          <div className='card_header'> План </div>
          <div className='card_header'> {kis.plan} </div>
        </div>
      </div>

      <span className='detail_block_header'> Госпитализировано в статусе </span>
      <div className='blocks_container'>
        <div className='separated_detail_block'> 
          <div className='card_header'> ЗЛ </div>
          <div className='card_header'> {kis.ZL} </div>
        </div>
        <div className='separated_detail_block'> 
          <div className='card_header'> Иногородние </div>
          <div className='card_header'> {kis.foreign} </div>
        </div>
        <div className='separated_detail_block'> 
          <div className='card_header'> НР </div>
          <div className='card_header'> {kis.nr} </div>
        </div>
        <div className='separated_detail_block'> 
          <div className='card_header'> НИЛ </div>
          <div className='card_header'> {kis.nil} </div>
        </div>
        <div className='separated_detail_block'> 
          <div className='card_header'> ДМС </div>
          <div className='card_header'> {kis.dms} </div>
        </div>
        <div className='separated_detail_block'> 
          <div className='card_header'> Не указано </div>
          <div className='card_header'> {kis.undefined} </div>
        </div>
      </div>
      <SignInDetailTable key={reload}/>
      {/* <button className="reload_button" onClick={fetchDataFromApi}>Обновить планы</button> */}



    </div>
  );
};

export default SignInDetailBoard;
