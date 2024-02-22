import React, { useContext } from "react";
import SignInDetailTable from "./SignInDetailTable";
import DataContext from "../../DataContext";
import ScaleX from "../ScaleX";
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
              Отказано <br></br><br></br> {dmk.refused} 
            </div>
            <div className='separated_detail_block'>
               Госпитализировано <br></br><br></br> {dmk.hosp}
            </div>
          </div>
          <span className='detail_block_header'> Госпитализировано по каналам </span>
          <div className='blocks_container'>
            <div className='separated_detail_block'> 103 <br></br><br></br> {kis.ch103} </div>
            <div className='separated_detail_block'> Поликлиника <br></br><br></br> {kis.clinic_only} </div>
            <div className='separated_detail_block'> 103 Поликлиника <br></br><br></br> {kis.ch103_clinic} </div>
            <div className='separated_detail_block'> Самотёк <br></br><br></br> {kis.singly} </div>
          </div>
          <span className='detail_block_header'> Госпитализировано в статусе </span>
          <div className='blocks_container'>
            <div className='separated_detail_block'> ЗЛ <br></br><br></br> {kis.ZL} </div>
            <div className='separated_detail_block'> Иногородние <br></br><br></br> {kis.foreign} </div>
            <div className='separated_detail_block'> Москвичи <br></br><br></br> {kis.moscow} </div>
            <div className='separated_detail_block'> Не указано <br></br><br></br> {kis.undefined} </div>
          </div>
          <SignInDetailTable data={dept_hosp}/>
        </div>

    );
}

export default SignInDetailBoard;