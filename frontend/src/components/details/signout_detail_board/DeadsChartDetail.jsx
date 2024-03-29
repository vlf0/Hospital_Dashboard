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
    'oaronmk_d': 'ОРИТ ОНМК',
    'surgery_d': 'Хирургическое',
    'oar1_d': 'ОРИТ № 1',
    'dp_d': 'Приемное ДП',
    'oar_d': 'ОАР',
    'trauma_d': 'травматологии и ортопедии',
    'neurosurgery_d': 'Нейрохирургическое',
    'oaroim_d': 'ОРИТ ОИМ',
    'oar2_d': 'ОРИТ № 2',
    'cardio_d': 'Кардиологическое',
    'therapy_d': 'Терапевтическое',
    'endo_d': 'Эндокринологическое',
    'neuroonmk_d': 'Неврологическое ОНМК',
    'urology_d': 'Урологическое',
    'pursurgery_d': 'Гнойной хирургии',
    'cardio2_d': '2 кардиологическое (ОИМ)',
    'skp_d': 'СКП',
    'gynecology_d': 'Гинекологическое',
    'emer_d': 'Приемное отделение',
    'multi_pay_d': 'МПО',
    'apc_d': 'ДС АПЦ',
    'combine_d': 'Сочетанной травмы',
    'pulmonology_d': 'Пульмонологическое'
}

const deptsOrder = ['emer_d', 'dp_d', 'oar_d', 'oar1_d', 'oar2_d', 'oaronmk_d', 'oaroim_d',
                    'surgery_d', 'neurosurgery_d', 'trauma_d', 'cardio_d', 'cardio2_d', 'therapy_d',
                    'endo_d', 'neuroonmk_d', 'urology_d', 'pursurgery_d', 'pulmonology_d',
                    'combine_d', 'gynecology_d', 'skp_d', 'apc_d', 'multi_pay_d'];
                    

const DeadsChartDetail = ({ data }) => {

    const deptsOut = Object.fromEntries(
        Object.entries(data)
          .filter(([key, value]) => key.endsWith('_d'))
      );

    // Sorting depts order 
    const orderedData = Object.fromEntries(deptsOrder.map(key => [key, deptsOut[key]]));

    const endDepts = Object.keys(orderedData)

    const ruDepts = endDepts.map(index => chartMap[index])
    const nums = Object.values(orderedData).map(value => value === undefined ? null : value);


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
                        formatter: (title, context) => {
                            if (context.dataset.data[context.dataIndex] === null) {
                              return 'Н/Д';
                            }
                            return title; // Use the default title if the value is not null
                        },
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
        <div className='signout_by_depts_chart'>
          <Bar data={arrived_data} options={chartOptions} />
        </div>
    );
};

export default DeadsChartDetail;