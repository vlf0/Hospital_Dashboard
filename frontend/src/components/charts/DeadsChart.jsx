import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bar } from 'react-chartjs-2';
import Chart from 'chart.js/auto';
import AnnotationPlugin from 'chartjs-plugin-annotation';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import DataContext from '../DataContext';
import GetWeekDays from '../dates/DatesFormat';
import { extractProperties } from '../Feauters';
import { mapArrivedValues } from '../Feauters';
import { GetDates } from '../dates/DatesFormat';
import "./arrived_chart.css";

Chart.register(AnnotationPlugin);
Chart.register(ChartDataLabels);


Chart.defaults.font.size = 12;
Chart.defaults.color = '#090b1f';  


const DeadsChart = () => {

    const planValue = 40;
    const navigate = useNavigate();

    const dmk_charts = useContext(DataContext).dmk.main_dmk;
    const pairValues = extractProperties(dmk_charts)
    const mappedData = mapArrivedValues(pairValues, GetDates());


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
        scales: {
            x: {
                grid: { 
                  drawOnChartArea: false,
                  drawTicks: false
                },
                ticks: {

                    beginAtZero: true,
                    color: '#090b1f',    
                },
            },
            y: {
                beginAtZero: true,
                grid: {
                  drawOnChartArea: true,
                  drawTicks: false
                  },
             
                ticks: {
                    color: (context) => {
                        if (context.tick.value === planValue) {
                            return '#860000'; // Customize the color of the custom grid lines
                        } else {
                            return '#090b1f'; // Default tick color
                        }
                    },
                    callback: (value, index, values) => {
                        // Customize the tick value
                        if (value === planValue) {
                            return `план ${planValue}`; // Change the tick label for the value 60
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
                            const percernts = ((title / planValue  * 100) - 100).toFixed(1);
                            return '\t' + percernts+'%';
                        },
                        font: {
                          size: 12,
                          weight: 'bold',
                        },
                        color: (context) => {
                          const value = context.dataset.data[context.dataIndex];
                          const percent = ((value / planValue) * 100 - 100).toFixed(1);
  
                          return percent < 0 ? '#b200ac' : '#049d00';
                        },
                    },
                },

            },

            annotation: {
                    annotations: {
                      line1: {
                        type: 'line',
                        yMin: planValue,
                        yMax: planValue,
                        borderColor: '#ff6384',
                        borderWidth: 1,
                      },
                    },
              },
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: 'Динамика умерших за неделю',
                color: '#090b1f',
                font: {
                    size: 13
                },
                padding: {
                    bottom: 30,
              }
            },
        },
        onClick: function () {
            var link = '/signout';
            navigate(link); // Changes the current page's URL
        }
    };

    return (
        <div className='arrived_chart'>
          <Bar data={arrived_data} options={chartOptions} />
        </div>
    );
};

export default DeadsChart;