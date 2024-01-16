import React from 'react';
import { useNavigate} from 'react-router-dom';
// import { useSpring, animated } from 'react-spring';
import { Bar } from 'react-chartjs-2';
import Chart from 'chart.js/auto';
import AnnotationPlugin from 'chartjs-plugin-annotation';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import current_date from '../dates/DatesFormat';
import "./arrived_chart.css";

Chart.register(AnnotationPlugin);
Chart.register(ChartDataLabels);


Chart.defaults.font.size = 12;
Chart.defaults.color = '#090b1f';  


const DeadsChart = () => {

    const navigate = useNavigate();

    const plan = 60


    const arrived_data = {
        labels: [
            `${current_date.day-6}.${current_date.month}`,
            `${current_date.day-5}.${current_date.month}`,
            `${current_date.day-4}.${current_date.month}`,
            `${current_date.day-3}.${current_date.month}`,
            `${current_date.day-2}.${current_date.month}`,
            `${current_date.day-1}.${current_date.month}`,
            `${current_date.day}.${current_date.month}`,
        ],
        datasets: [
            {
              label: 'total',
              data: [80, 73, 84, 35, 69, 76, 92],//data ? [data.data, data.data, data.data] : [10,20,10],
              backgroundColor: ['#2d8587', '#2d8587', '#2d8587'],
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
                        if (value === 60) {
                            return 'план 60'; // Change the tick label for the value 60
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
                          size: 10,
                          weight: 'bold',
                          },
                        anchor: 'end',
                        align: 'end',
                        // formatter: title => {
                        //     const percernts = ((title / plan  * 100) - 100).toFixed(1);
                        //     return '\t' + percernts+'%';
                        // },
                    },
                    value: {
                        formatter: title => {
                            const percernts = ((title / plan  * 100) - 100).toFixed(1);
                            return '\t' + percernts+'%';
                        },
                        color: 'blue',
                        font: {
                          size: 10,
                          weight: 'bold',
                          },
                    },
                },

            },

            annotation: {
                    annotations: {
                      line1: {
                        type: 'line',
                        yMin: 60,
                        yMax: 60,
                        borderColor: '#ff6384',
                        borderWidth: 2,
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
            },
        },
    };

    // Chart component
    return (
        <div className='arrived_chart'>
          <Bar data={arrived_data} options={chartOptions} />
        </div>
    );
};

export default DeadsChart;
