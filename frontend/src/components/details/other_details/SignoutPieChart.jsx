import React from 'react';
import { Pie } from 'react-chartjs-2';
import NoData from '../../no_data/NoData';
import TopBlock from '../../menu/TopBlock';
import './details.css';
import '../../parent.css';


const mapResult = {
  deads: 'Умершие',
  moved: 'Переведенные в другую МО',
  signout: 'Выписанные',

};


const SignoutDetailPie = ( {labels, data} ) => {


  const ruColumns = labels.map(name => mapResult[name])
                    .filter(channel => channel !== undefined);
  const signoutData = data.slice(0, ruColumns.length)



  const resultsData = {
    labels: ruColumns,
    datasets: [
      {
        label: 'кол-во',
        data: signoutData,
        backgroundColor: [
          'rgba(255, 99, 132, 0.4)',
          'rgba(54, 162, 235, 0.4)',
          'rgba(255, 206, 86, 0.4)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const resultsOptions = {
    plugins: {    
      datalabels: {
        anchor: 'center',
        align: 'start',
        font: {
          size: 15,
          // weight: 'bold',
        }
      },
      legend: {
        labels: {
          padding: 15,
          font: {
            family: 'Arial',
            size: 15,
            weight: 'bold',
          },
        },
      },
      title: {
        display: true,
        text: 'По исходу',
        color: '#090b1f',
        font: {
          size: 18,
        },
        padding: {
          bottom: 15,
        },
      },
    },
  };
  

  const pie = signoutData.some(data => data !== 0);
  const dateParam = new URLSearchParams(window.location.href).get('date').split('-').reverse().join('.');

  return (
    <>
    <TopBlock textContent={'Детализация выписки'} menu_point={'details'} date={dateParam} />
    <div className='details'>
        <div className='signout_pie'>
          {pie ? (
          <Pie data={resultsData} options={resultsOptions} />
          ) : (
            <NoData name={'Детализация выписанных'}/>
          )}
        </div>
    </div>
    </>
  );
};

export default SignoutDetailPie;