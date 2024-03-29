import React, { useState } from "react";
import { useSpring, animated } from "react-spring";
import InOARDetailTable from "./InOARDetailTable";
import MoveOARDetailTable from "./MoveOARDetailTable";
import OnTreatmentOARDetailTable from "./OnTreatmentOARDetailTable";
import DeadsOARDetailTable from "./DeadsOARDetailTable";


const OARDetailBoard = ({ dept, values, deads }) => {

  const [isOARTableVisible, setIsOARTableVisible] = useState(false);
  const [tableType, setTableType] = useState(null);
  const [selectedValue, setSelectedValue] = useState(null);

  const toggleDeadTableVisibility = (type, event) => {
    const department = event.currentTarget.getAttribute('orit-name');
    setIsOARTableVisible(!isOARTableVisible);
    setTableType(type);
    setSelectedValue(department);
  };

  // Spring effect of appearance
  const springProps = useSpring({
    transform: `scale(${isOARTableVisible ? 1 : 0})`,
    height: isOARTableVisible ? "auto" : 0,
    opacity: isOARTableVisible ? 1 : 0,
    config: { tension: 200, friction: 25 },
    delay: isOARTableVisible ? 30 : 0,
    width: "-webkit-fill-available",
  });

  return (
    <>
      <span className="detail_block_header"> {dept} </span>
      <div 
      className="blocks_container"
      orit-name={dept}
      >
        <div
          className="separated_detail_block_X"
          onClick={(event) => toggleDeadTableVisibility("in", event)}
          orit-name={dept}
        >
          <p> Поступило новых пациентов </p> {values[0]}
        </div>

        <div
          className="separated_detail_block_X"
          onClick={(event) => toggleDeadTableVisibility("move", event)}
          orit-name={dept}
        >
          <p> Переводы из отделений </p> {values[1]}
        </div>

        <div
          className="separated_detail_block_X"
          onClick={(event) => toggleDeadTableVisibility("onTreatment", event)}
          orit-name={dept}
        >
          <p> Находятся на лечении </p> {values[2]}
        </div>

        <div
          className="separated_detail_block_X"
          onClick={(event) => toggleDeadTableVisibility("deads", event)}
          orit-name={dept}
        >
          <p> Умерли в отделении </p> {deads}
        </div>
      </div>
      <animated.div style={springProps}>
        {isOARTableVisible && tableType === "in" && <InOARDetailTable departament={selectedValue} />}
        {isOARTableVisible && tableType === "move" && <MoveOARDetailTable departament={selectedValue} />}
        {isOARTableVisible && tableType === "onTreatment" && <OnTreatmentOARDetailTable departament={selectedValue} />}
        {isOARTableVisible && tableType === "deads" && <DeadsOARDetailTable departament={selectedValue} />}
      </animated.div> 
    </>
  ); 
}; 

export default OARDetailBoard;
