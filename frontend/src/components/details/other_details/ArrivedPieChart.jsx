import React from 'react';
import { Pie } from 'react-chartjs-2';
import NoData from '../../no_data/NoData';
import Header from '../Header';
import './details.css';
import '../../parent.css';



const mapChannels = {
  ch103: '103',
  clinic_only: 'Поликлиника',
  ch103_clinic: '103 Поликлиника',
  singly: 'Самотек',
};

const mapTypes = {
  ZL: 'ЗЛ',
  foreign: 'Иногородние',
  moscow: 'Москвичи',
  undefined: 'не указано'
};

const ArrivedDetailPie = ( {labels, data} ) => {


  const ruChannels = labels.map(name => mapChannels[name])
                     .filter(channel => channel !== undefined);
  const ruTypes = labels.map(name => mapTypes[name])
                  .filter(channel => channel !== undefined);


  const channels = data.slice(0, ruChannels.length)
  const types = data.slice(ruTypes.length)




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
        text: 'Детализация по каналам поступления',
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
        text: 'Детализация по типу пациентов',
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
    <div className='details'>
      <Header textHeader={'Детализация госпитализированных'} date={dateParam}/>  
        <div className='arrived_pie'>
          {pie1 ? (
          <Pie data={channelsData} options={channelsOptions} />
          ) : (
            <NoData name={'Детализация по каналам поступления'}/>
          )}
          {pie2 ? (
          <Pie data={typesData} options={typesOptions} />
          ) : (
            <NoData name={'Детализация по типу пациентов'}/>
          )}
        </div>
    </div>
  );
};

export default ArrivedDetailPie;