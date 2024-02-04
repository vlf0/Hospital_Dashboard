import React, { useContext } from "react";
import SignInDetailTable from "./SignInDetailTable";
import DataContext from "../../DataContext";
import ScaleX from "../ScaleX";
import './detail_blocks.css';
import './signin_table.css';


const SignInDetailBoard = ({ combinedData }) => {

    let readyData = useContext(DataContext);

    return (
        <div className='detail_block'>
          <span className='detail_block_header'> Обратившиеся </span>
          <div className='blocks_container'>
            <div className='separated_detail_block'> 
              Отказано <br></br><br></br> { 20 } 
            </div>
            <div className='separated_detail_block'>
               Госпитализировано <br></br><br></br> { 90 }
            </div>
          </div>
          <span className='detail_block_header'> Госпитализировано по каналам </span>
          <div className='blocks_container'>
            <div className='separated_detail_block'> 103 канал <br></br><br></br> {43} </div>
            <div className='separated_detail_block'> Поликлиника <br></br><br></br> {17} </div>
            <div className='separated_detail_block'> 103 (Поликлиника) <br></br><br></br> {24} </div>
            <div className='separated_detail_block'> Самотёк <br></br><br></br> {6} </div>
          </div>
          <span className='detail_block_header'> Госпитализировано в статусе </span>
          <div className='blocks_container'>
            <div className='separated_detail_block'> ЗЛ <br></br><br></br> {56} </div>
            <div className='separated_detail_block'> Иногородние <br></br><br></br> {24} </div>
            <div className='separated_detail_block'> Москвичи <br></br><br></br> {18} </div>
            <div className='separated_detail_block'> Не указано <br></br><br></br> {2} </div>
          </div>
          <SignInDetailTable data={combinedData}/>
        </div>

    );
}

export default SignInDetailBoard;