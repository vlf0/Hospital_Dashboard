import React from "react";
import { useSpring, animated } from 'react-spring';


const NoData = ({name}) => {

   return (
    <animated.div className={'nodata_animate'}>

      
      <span className='pie_chart_name'> {name}</span>
      <span className='null_data'>Нет доступных данных для отображения</span>

    </animated.div>
   );
};

export default NoData;