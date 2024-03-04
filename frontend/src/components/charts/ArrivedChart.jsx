import React, { useContext } from 'react';
import { useNavigate} from 'react-router-dom';
// import { useSpring, animated } from 'react-spring';
import {Bar} from 'react-chartjs-2';
import Chart from 'chart.js/auto';
import AnnotationPlugin from 'chartjs-plugin-annotation';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import DataContext from '../DataContext';
import GetWeekDays from '../dates/DatesFormat';
import { extractProperty } from '../Feauters';
import { ensureArrayLength } from '../Feauters';
import "./arrived_chart.css";

Chart.register(AnnotationPlugin);
Chart.register(ChartDataLabels);


Chart.defaults.font.size = 12;
Chart.defaults.color = '#090b1f';  


const ArrivedChart = () => {
    
    const navigate = useNavigate();
    const plan = 120;

    const dmk_charts = useContext(DataContext).dmk.main_dmk;
    const mappedData = extractProperty(dmk_charts, 'arrived');
    ensureArrayLength(mappedData, 7);

    const mappedWeek = GetWeekDays();

    const arrived_data = {
        labels: mappedWeek,
        datasets: [
            {
              label: 'total',
              data: mappedData,
              backgroundColor: ['#212e93b3'],
              borderColor: '#090b1f',
              borderWidth: 1,
            },
        ],
    };

    const chartOptions = {
        barThickness: 'flex',
        barPercentage: 0.9, 
        categoryPercentage: 0.9,
        // layout: {
        //     padding: {
        //       top: 20, // Adjust the top padding as needed
        //     }
        //   },
        scales: {
            x: {
                // stacked: true,
                grid: { 
                  drawOnChartArea: false,
                  drawTicks: false
                },
                ticks: {
                    // display: false,
                    beginAtZero: true,
                    color: '#090b1f',   
                    font: {
                    // size: 14,
                    // weight: 'bold' 
                },},
            },
            y: {
                // stacked: true,
                grid: {
                  drawOnChartArea: true,
                  drawTicks: false
                  },
             
                ticks: {
                    color: (context) => {
                        if (context.tick.value === plan) {
                            return '#860000'; // Customize the color of the custom grid lines
                        } else {
                            return '#090b1f'; // Default tick color
                        }
                    },
                    callback: (value, index, values) => {
                        // Customize the tick value
                        if (value === 125) {
                            return 'план 125'; // Change the tick label for the value 60
                        } else {
                            return value; // Use the default tick label for other values
                        }
                    },
                    font: {weight: 'bold'},
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
                        //   weight: 'bold',
                          },
                        anchor: 'end',
                        align: 'end',
                          formatter: (title, context) => {
                            if (context.dataset.data[context.dataIndex] === null) {
                              return 'N/A';
                            }
                            return title; // Use the default title if the value is not null
                          },
                    },
                    value: {
                        formatter: (title, context) => {
                            if (context.dataset.data[context.dataIndex] === null) {
                                return '';
                            }
                            const percernts = ((title / plan  * 100) - 100).toFixed(1);
                            const color = percernts < 0 ? '#b200ac' : 'blue';

                            return '\t' + percernts+'%';
                        },
                        font: {
                          size: 12,
                          weight: 'bold',
                          },
                        color: (context) => {
                          const value = context.dataset.data[context.dataIndex];
                          const percent = ((value / plan) * 100 - 100).toFixed(1);
  
                          return percent < 0 ? '#b200ac' : '#00a318';
                        },
                    },
                },

            },

            annotation: {
                    annotations: {
                      line1: {
                        type: 'line',
                        yMin: 120,
                        yMax: 120,
                        borderColor: '#ff6384',
                        borderWidth: 1.5,
                      },
                    },
              },
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: 'Динамика обращений за неделю',
                color: '#090b1f',
                font: {
                    size: 13,
            },                
            padding: {
            //   top: 20, // Adjust the top padding as needed
              bottom: 30,
            }
            },
        },
    };

    // Chart component
    return (
        <div className='arrived_chart'>
          <Bar data={arrived_data} options={chartOptions} />
        </div>

        // Code for animation chart itself
        // <animated.div className='arrived_chart' style={props}>
        //     <Bar data={arrived_data} options={chartOptions} />
        // </animated.div>
    );
};

export default ArrivedChart;