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
import { extractDetailsProperties } from '../Feauters';
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

    let arrivedPlanValue = 100;
    let mainData = sessionStorage.getItem('main_data');
    mainData = JSON.parse(mainData);
    if (mainData.dmk.plans_dmk.length !== 0) {
      arrivedPlanValue = mainData.dmk.plans_dmk[0].plan_value
    }

    const dmkData = useContext(DataContext).dmk
    const dmk_charts = dmkData.main_dmk;
    const mainPairValues = extractProperties(dmk_charts, 'arrived');
    const detailsPairValues = extractDetailsProperties(dmk_charts, 'detailing')

    const mappedMainData = mapArrivedValues(mainPairValues, GetDates(), 'arrived');
    const mappedDetailsData = mapArrivedValues(detailsPairValues, GetDates(), 'detailing');
    const otherPatients = mappedMainData.map((num, index) => num - mappedDetailsData[index]);

    const mappedWeek = GetWeekDays();
    const barOptions = GetDates();

    let dynamicPadding = 0;
    if (mappedDetailsData.every(value => value >= 8)) {
      if (mappedDetailsData.every(value => value >= 4)) {
        dynamicPadding = 20;
      } else {dynamicPadding = 14;}
      dynamicPadding = 0;
    }

    const dataWithDates = mappedWeek.map((weekDay, index) => ({
      label: weekDay,
      date: barOptions[index]
    }));
    
    const arrived_data = {
        labels: mappedWeek,
        datasets: [
            {
              label: 'Зарегистрированные',
              data: mappedDetailsData,
              backgroundColor: ['#647fda'],
              borderColor: '#e9306a',
              borderWidth: 1,
              srtDates: dataWithDates,
              datalabels: {
                display: true,
                labels: {
                    title: {
                        color: '#001a3f',
                        font: {
                          size: 25,
                          family:'nbold'
                          },
                        // anchor: 'start',
                        align: 'center',
                          formatter: (title, context) => {
                            if (context.dataset.data[context.dataIndex] === null) {
                              return 'Н/Д';
                            }
                            return title; 
                          },
                    },
                    value: {
                        formatter: (title, context) => {
                            if (context.dataset.data[context.dataIndex] === null) {
                                return '';
                            }
                            const percernts = (title / arrivedPlanValue  * 100).toFixed(1);

                            return '\t' + percernts+'%';
                        },
                        // anchor: 'center',
                        align: 'start',
                        padding: 8,
                        font: {
                          size: 19,
                          weight: 'bold',
                          family: 'nbold'
                          },
                        color: (context) => {
                          const value = context.dataset.data[context.dataIndex];
                          const percent = ((value / arrivedPlanValue) * 100).toFixed(1);

                          return percent < 100 ? '#e9306a' : '#25c445';
                        },
                    },
                },

            },
            },
            {
              label: 'Всего',
              data: otherPatients,
              backgroundColor: ['#1a2a56'],
              borderColor: '#e9306a',
              borderWidth: 1,
              srtDates: dataWithDates,
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
                          // Use value from mappedMainData
                          const mainDataValue = mappedMainData[context.dataIndex];
                          return mainDataValue;
                      },
                    },
                },
            },
            },
        ],
    };

    const chartOptions = {
        barThickness: 'flex',
        barPercentage: 0.9, 
        categoryPercentage: 0.9,
        scales: {
            x: {
                stacked: true,
                grid: { 
                  drawOnChartArea: false,
                  drawTicks: true
                },
                ticks: {
                    padding: dynamicPadding,
                    beginAtZero: true,
                    color: '#090b1f',  
                    font: {
                        weight: 'bold',
                        family: 'nbold',
                    }
                },
            },
            y: {
                stacked: true,
                grid: {
                  drawOnChartArea: true,
                  drawTicks: true,
                },
                ticks: {
                    color: (context) => {
                        if (context.tick.value === arrivedPlanValue) {
                            return '#860000';
                        } else {
                            return '#001a3f'; 
                        }
                    },
                    callback: (value, index, values) => {
                        if (value === arrivedPlanValue) {
                            return `план ${arrivedPlanValue}`; 
                        } else {
                            return value; 
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
            annotation: {
                    annotations: {
                      line1: {
                        type: 'line',
                        yMin: arrivedPlanValue,
                        yMax: arrivedPlanValue,
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
              bottom: 40,
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