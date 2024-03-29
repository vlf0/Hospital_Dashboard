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


Chart.defaults.font.size = 12;
Chart.defaults.color = '#090b1f';  


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