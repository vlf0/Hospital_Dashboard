import React from "react";
import SignInDetailTable from "./SignInDetailTable";
import ScaleX from "../ScaleX";
import './detail_blocks.css';
import './signin_table.css';


const SignInDetailBoard = ({ signInCount, refuseCount, combinedData }) => {
    return (
        <div className='detail_block'>
          <span className='detail_block_header'> Обратившиеся </span>
          <div className='blocks_container'>
            <div className='separated_detail_block'> Отказано <br></br><br></br> {refuseCount} </div>
            <div className='separated_detail_block'> Госпитализировано <br></br><br></br> {signInCount} </div>
          </div>
          <span className='detail_block_header'> Госпитализировано по каналам </span>
          <div className='blocks_container'>
            <div className='separated_detail_block'> 103 <br></br><br></br> {1} </div>
            <div className='separated_detail_block'> Поликлиника <br></br><br></br> {1} </div>
            <div className='separated_detail_block'> 103 (Поликлиника) <br></br><br></br> {1} </div>
            <div className='separated_detail_block'> Самотёк <br></br><br></br> {1} </div>
          </div>
          <span className='detail_block_header'> Госпитализировано в статусе </span>
          <div className='blocks_container'>
            <div className='separated_detail_block'> ЗЛ <br></br><br></br> {1} </div>
            <div className='separated_detail_block'> Иногородние <br></br><br></br> {1} </div>
            <div className='separated_detail_block'> Москвичи <br></br><br></br> {1} </div>
            <div className='separated_detail_block'> Не указано <br></br><br></br> {1} </div>
          </div>
          <SignInDetailTable data={combinedData}/>
        </div>

    );
}

export default SignInDetailBoard;