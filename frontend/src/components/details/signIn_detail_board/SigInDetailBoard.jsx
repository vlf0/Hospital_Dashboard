import React, { useContext } from "react";
import SignInDetailTable from "./SignInDetailTable";
import DataContext from "../../DataContext";
import './detail_blocks.css';
import './signin_table.css';


const SignInDetailBoard = () => {

  const data = useContext(DataContext);

  const dept_hosp = data.kis[0].dept_hosp[0]
  let dmk = data.dmk
  dmk = dmk[dmk.length-1]

  let kis = data.kis
  kis = kis[0].arrived[0]


    return (
        <div className='detail_block'>
          <span className='detail_block_header'> Обратившиеся </span>
          <div className='blocks_container'>
            <div className='separated_detail_block'> 
              <p> Отказано </p> {dmk.refused} 
            </div>
            <div className='separated_detail_block'>
            <p> Госпитализировано </p> {dmk.hosp}
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
          <SignInDetailTable data={dept_hosp}/>
        </div>

    );
}

export default SignInDetailBoard;