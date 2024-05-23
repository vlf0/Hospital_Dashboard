import React from 'react';
import '../menu/top_block.css';


const Header = ({textHeader, date}) => {

  return (
    <>
    <div className='main_header'> 
      {textHeader} 
      <span className='now_date'> по состоянию на {date}</span>
    </div>
    </>
  );
};

export default Header;
