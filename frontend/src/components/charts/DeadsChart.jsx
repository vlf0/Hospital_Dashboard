import React, { useContext } from 'react';
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


const DeadsChart = () => {

    const dmk_charts = useContext(DataContext).dmk.main_dmk;
    const pairValues = extractProperties(dmk_charts, 'deads')
    const mappedData = mapArrivedValues(pairValues, GetDates(), 'deads');

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
                    font: {
                        weight: 'bold',
                        size: 13,
                    },
                    color: 'black'
                },
            },
            y: {
                beginAtZero: true,
                grid: {
                  drawOnChartArea: true,
                  drawTicks: false
                  },
                ticks: {
                    font: {
                        weight: 'bold',
                        size: 13,
                    },
                    color: 'black'
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
    };

    return (
        <div className='arrived_chart'>
          <Bar data={arrived_data} options={chartOptions} />
        </div>
    );
};

export default DeadsChart;