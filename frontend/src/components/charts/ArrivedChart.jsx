import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import {Bar} from 'react-chartjs-2';
import Chart from 'chart.js/auto';
import AnnotationPlugin from 'chartjs-plugin-annotation';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import DataContext from '../DataContext';
import GetWeekDays from '../dates/DatesFormat';
import { mapArrivedValues } from '../Feauters';
import { extractProperties } from '../Feauters';
import { GetDates } from '../dates/DatesFormat';
import "./arrived_chart.css";

Chart.register(AnnotationPlugin);
Chart.register(ChartDataLabels);


const ArrivedChart = () => {
    
    const navigate = useNavigate();
    const handleClick = (event, chartElements) => {
      if (chartElements.length > 0) {
      const clickedBarIndex = chartElements[0].index;
      const clickedBarCustomData = arrived_data['datasets'][0]['srtDates'][clickedBarIndex]['date'];
          const link = `/details?type=arrived&date=${clickedBarCustomData}`;
          navigate(link);
      }
    };


    const planValue = 135;

    const dmk_charts = useContext(DataContext).dmk.main_dmk;
    const pairValues = extractProperties(dmk_charts, 'arrived');
    const mappedData = mapArrivedValues(pairValues, GetDates(), 'arrived');

    const mappedWeek = GetWeekDays();
    const barOptions = GetDates();

    const dataWithDates = mappedWeek.map((weekDay, index) => ({
      label: weekDay,
      date: barOptions[index]
    }));
    
    const arrived_data = {
        labels: mappedWeek,
        datasets: [
            {
              label: 'total',
              data: mappedData,
              backgroundColor: ['#1a2a56'],
              borderColor: '#e9306a',
              borderWidth: 1,
              srtDates: dataWithDates
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
                  drawTicks: true
                },
                ticks: {
                    beginAtZero: true,
                    color: '#090b1f',  
                    font: {
                        weight: 'bold',
                        family: 'nbold',
                    }
                },
            },
            y: {
                grid: {
                  drawOnChartArea: true,
                  drawTicks: true,
                },
                ticks: {
                    color: (context) => {
                        if (context.tick.value === planValue) {
                            return '#860000'; // Customize the color of the custom grid lines
                        } else {
                            return '#001a3f'; // Default tick color
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
                    font: {
                        weight: 'bold',
                        family: 'nbold',
                        size: 20
                    },
                },
            },
        },
        plugins: { 
            datalabels: {
                display: true,
                labels: {
                    title: {
                        color: '#001a3f',
                        font: {
                          size: 25,
                          family:'nbold'
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
                    value: {
                        formatter: (title, context) => {
                            if (context.dataset.data[context.dataIndex] === null) {
                                return '';
                            }
                            const percernts = ((title / planValue  * 100) - 100).toFixed(1);
                            const color = percernts < 0 ? '#e9306a' : 'blue';

                            return '\t' + percernts+'%';
                        },
                        font: {
                          size: 20,
                          weight: 'bold',
                          family: 'nbold'
                          },
                        color: (context) => {
                          const value = context.dataset.data[context.dataIndex];
                          const percent = ((value / planValue) * 100 - 100).toFixed(1);
  
                          return percent < 0 ? '#e9306a' : '#25c445';
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
                        borderColor: '#e9306a',
                        borderWidth: 2,
                      },
                    },
              },
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: 'Динамика обращений за неделю',
                color: '#001a3f',
                font: {
                    size: 30,
                    family: 'nbold'
                    
            },                
            padding: {
              bottom: 30,
            }
            },
        },
        onClick: handleClick
    };

    return (
        <div className='arrived_chart'>
          <Bar data={arrived_data} options={chartOptions} />
        </div>
    );
};

export default ArrivedChart;