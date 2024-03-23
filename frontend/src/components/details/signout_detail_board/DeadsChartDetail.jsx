import React from 'react';
import { Bar } from 'react-chartjs-2';
import Chart from 'chart.js/auto';
import AnnotationPlugin from 'chartjs-plugin-annotation';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import '../../charts/arrived_chart.css';

Chart.register(AnnotationPlugin);
Chart.register(ChartDataLabels);


Chart.defaults.font.size = 12;
Chart.defaults.color = '#090b1f';  

// Depts map
const chartMap = {
    'surgery_d': 'Хирургическое отделение',
    'oar1_d': 'ОРИТ №1',
    'cardio_d': 'Кардиологическое отделение',
    'therapy_d': 'Терапевтическое отделение',
    'oar2_d': 'ОРИТ №2',
    'oar3_d': 'ОРИТ №3'
}

const deptsOrder = ['therapy_d', 'surgery_d', 'cardio_d', 'oar1_d'];

const DeadsChartDetail = ({ data }) => {


    const deptsOut = Object.fromEntries(
        Object.entries(data)
          .filter(([key, value]) => key.endsWith('_d'))
      );

    // Sorting depts order 
    const orderedData = Object.fromEntries(deptsOrder.map(key => [key, deptsOut[key]]));

    const endDepts = Object.keys(orderedData)

    const ruDepts = endDepts.map(index => chartMap[index])
    const nums = Object.values(orderedData) 


    const arrived_data = {
        labels: ruDepts,
        datasets: [
            {
              label: 'total',
              data: nums,
              backgroundColor: ['#2d8587'],
              borderColor: '#090b1f',
              borderWidth: 1,
            },
        ],
    };

    const chartOptions = {
        barThickness: 'flex',
        barPercentage: 0.9, 
        categoryPercentage: 0.8,
        scales: {
            x: {

                grid: { 
                  drawOnChartArea: false,
                  drawTicks: false
                },
                ticks: {
                    beginAtZero: true,
                    color: '#090b1f',   
                    font: {
                        weight: 'bold' 
                },},
            },
            y: {
                grid: {
                  drawOnChartArea: true,
                  drawTicks: false
                  },
             
                ticks: {
                    font: {
                      weight: 'bold'
                    },
                },
            },
        },

        plugins: { 
            datalabels: {
                display: true,
                labels: {
                    title: {
                        color: 'black',
                        font: {
                          size: 13,
                          },
                        anchor: 'end',
                        align: 'end',
                    },
                },
            },
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: 'Выписанные по отделениям',
                color: '#090b1f',
                font: {
                    size: 13,
            },                
            padding: {
              bottom: 30,
            }
            },
    
        },
    };

    return (
        <div className='arrived_chart'>
          <Bar data={arrived_data} options={chartOptions} />
        </div>
    );
};

export default DeadsChartDetail;