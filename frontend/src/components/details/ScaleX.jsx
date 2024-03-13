import React from 'react';


const ColoredLine = ({ percentage, plan, arrivedFact }) => {
  const gradient = `linear-gradient(to right, #828cff ${percentage}%, #e785fc ${percentage}%)`;

  const lineStyle = {
    width: '-webkit-fill-available',
    height: '30px', // Set the height of the line
    background: gradient,
    display: 'flex',
    flexDirection: 'row',
    flexWrap: 'wrap',
    alignItems: 'center',
    justifyContent: 'space-between',
    alignContent: 'center',
    margin: -3,
  };

  const spanStyle = {
    fontSize: '14px',
    fontWeight: 'bold',
    marginLeft: '22px',
    marginRight: '22px',
  };

  return <div style={lineStyle}>
    <span style={spanStyle}> факт { arrivedFact } </span>
    <span style={spanStyle}> план { plan } </span>
  </div>;
};

const ScaleX = ({ hospFact, hospPlan }) => {

  const percentage = hospFact / hospPlan * 100;
  
  return (
    <div>
      <ColoredLine arrivedFact={hospFact} plan={hospPlan} percentage={percentage}/>
      {/* Add other components or content as needed */}
    </div>
  );
};

export default ScaleX;
