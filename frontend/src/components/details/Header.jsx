import React from 'react';
import '../menu/top_block.css';


const Header = ({textHeader, date}) => {

  return (
    <>
    <p className='main_header'> {textHeader}</p>
    <span className='now_date'> по состоянию на {date}</span>
    </>
  );
};

export default Header;
