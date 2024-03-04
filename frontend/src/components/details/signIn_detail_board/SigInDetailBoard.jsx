import React, { useContext } from "react";
import SignInDetailTable from "./SignInDetailTable";
import DataContext from "../../DataContext";
import './detail_blocks.css';
import './signin_table.css';
import { constructFrom } from "date-fns";


const SignInDetailBoard = () => {

  const data = useContext(DataContext);

  const kis = data.kis[0].arrived[0]

  // Accumulated data for month's plan
  const accum_dmk = data.dmk.accum_dmk

  let main_dmk = data.dmk.main_dmk
  main_dmk = main_dmk[main_dmk.length-1]


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

          </div>
          <span className='detail_block_header'> Госпитализировано в статусе </span>
          <div className='blocks_container'>
            <div className='separated_detail_block'>
              <p> ЗЛ </p> {kis.ZL} </div>
            <div className='separated_detail_block'>
              <p> Иногородние </p> {kis.foreign} </div>
            <div className='separated_detail_block'> 
              <p> Москвичи </p> {kis.moscow} </div>
            <div className='separated_detail_block'>  
              <p> Не указано </p> {kis.undefined} </div>
          </div>
          <SignInDetailTable data={accum_dmk}/>
        </div>

    );
}

export default SignInDetailBoard;