import React from 'react';
import { Pie } from 'react-chartjs-2';
import NoData from '../../no_data/NoData';
import TopBlock from '../../menu/TopBlock';
import './details.css';
import '../../parent.css';



const mapChannels = {
  ch103: '103',
  clinic_only: 'Поликлиника',
  ch103_clinic: '103 Поликлиника',
  singly: 'Самотек',
  plan: 'План'
};

const mapTypes = {
  ZL: 'ЗЛ',
  foreign: 'Иногородние',
  nr: 'НИЛ',
  nil: 'НР',
  dms: 'ДМС',
  undefined: 'Не указано'
};

const ArrivedDetailPie = ( {labels, data} ) => {


  const ruChannels = labels.map(name => mapChannels[name])
                     .filter(channel => channel !== undefined);
  const ruTypes = labels.map(name => mapTypes[name])
                  .filter(channel => channel !== undefined);


  const channels = data.slice(0, ruChannels.length)
  const types = data.slice(ruChannels.length)



  const channelsData = {
    labels: ruChannels,
    datasets: [
      {
        label: 'кол-во',
        data: channels,
        backgroundColor: [
          'rgba(255, 99, 132, 0.4)',
          'rgba(54, 162, 235, 0.4)',
          'rgba(255, 206, 86, 0.4)',
          'rgba(75, 192, 192, 0.4)',
          'rgba(153, 102, 255, 0.4)',
          'rgba(255, 159, 64, 0.4)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const channelsOptions = {
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
        text: 'По каналам поступления',
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
  


  const typesData = {
    labels: ruTypes,
    datasets: [
      {
        label: 'кол-во',
        data: types,
        backgroundColor: [
          'rgba(117, 217, 160, 0.4)',
          'rgba(54, 162, 235, 0.4)',
          'rgba(255, 206, 86, 0.4)',
          'rgba(245, 147, 66, 0.4)',
          'rgba(153, 102, 255, 0.4)',
          'rgba(255, 159, 64, 0.4)',
        ],
        borderColor: [
          'rgba(117, 217, 160)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(154, 161, 157)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const typesOptions = {
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
        text: 'По типу пациентов',
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


  const pie1 = channels.some(data => data !== 0);
  const pie2 = types.some(data => data !== 0);




  const dateParam = new URLSearchParams(window.location.href).get('date').split('-').reverse().join('.');

  return (
    <>
    <TopBlock textContent={'Детализация госпитализированных'} menu_point={'details'} date={dateParam} />
    <div className='details'>

        <div className='arrived_pie'>
          {pie1 ? (
          <Pie data={channelsData} options={channelsOptions} />
          ) : (
            <NoData name={'По каналам поступления'}/>
          )}
          {pie2 ? (
          <Pie data={typesData} options={typesOptions} />
          ) : (
            <NoData name={'По типу пациентов'}/>
          )}
        </div>
    </div>
    </>
  );
};

export default ArrivedDetailPie;