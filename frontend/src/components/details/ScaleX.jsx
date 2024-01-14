import React from 'react';

const plan = 100

const ColoredLine = ({ percentage, arrivedFact }) => {
  const gradient = `linear-gradient(to right, #828cff ${percentage}%, #e785fc ${percentage}%)`;

  const lineStyle = {
    width: '-webkit-fill-available',
    height: '18px', // Set the height of the line
    background: gradient,
    display: 'flex',
    flexDirection: 'row',
    flexWrap: 'wrap',
    alignItems: 'center',
    justifyContent: 'space-between',
    alignContent: 'center',
  };

  const spanStyle = {
    fontSize: '12px',
    fontWeight: 'bold',
    marginLeft: '22px',
    marginRight: '22px',
    marginBottom: '1px',
  };

  return <div style={lineStyle}>
    <span style={spanStyle}> факт { arrivedFact } </span>
    <span style={spanStyle}> план { plan } </span>
  </div>;
};

const ScaleX = ({ arrivedFact }) => {

  const percentage = arrivedFact / plan * 100;
  
  return (
    <div>
      <ColoredLine arrivedFact={arrivedFact} percentage={percentage}/>
      {/* Add other components or content as needed */}
    </div>
  );
};

export default ScaleX;
