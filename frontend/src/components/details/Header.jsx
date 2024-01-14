import React from 'react';
import current_date from '../dates/DatesFormat';
import '../menu/top_block.css';


const Header = ({textHeader}) => {

  const currentDatetime = new Date().toLocaleDateString('ru-RU');

  return (
    <>
    <p className='main_header'> {textHeader}</p>
    <span className='now_date'> по состоянию на {currentDatetime}</span>
    </>
  );
};

export default Header;
