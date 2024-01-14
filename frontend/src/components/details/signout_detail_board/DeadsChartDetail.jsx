import React from 'react';
import { useNavigate} from 'react-router-dom';
import { Bar } from 'react-chartjs-2';
import Chart from 'chart.js/auto';
import AnnotationPlugin from 'chartjs-plugin-annotation';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import current_date from '../../dates/DatesFormat';
import '../../charts/arrived_chart.css';

Chart.register(AnnotationPlugin);
Chart.register(ChartDataLabels);


Chart.defaults.font.size = 12;
Chart.defaults.color = '#090b1f';  


const DeadsChartDetail = ({ profiles }) => {

    const navigate = useNavigate();

    const plan = 60

    const arrived_data = {
        labels: profiles,
        datasets: [
            {
              label: 'total',
              data: [80, 73, 84],//data ? [data.data, data.data, data.data] : [10,20,10],
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
                        weight: 'bold' 
                },},
            },
            y: {
                // stacked: true,
                min: 0, 
                max: 100, 
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
                          size: 10,
                          weight: 'bold',
                          },
                        anchor: 'end',
                        align: 'end',
                    },
                    // Values inside the bars
                    // value: {
                    //     formatter: title => {
                    //         const percernts = ((title / plan  * 100) - 100).toFixed(1);
                    //         return '\t' + percernts+'%';
                    //     },
                    //     color: 'blue',
                    //     font: {
                    //       size: 10,
                    //       weight: 'bold',
                    //       },
                    // },
                },
            },
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: 'Выписанные по отделениям',
                color: '#090b1f',
            },
    
        },
        onClick: function () {
                var link = '/deads'; 
                navigate(link); // Changes the current page's URL
        }
    };

    // Chart component
    return (
        <div className='arrived_chart'>
          <Bar data={arrived_data} options={chartOptions} />
        </div>
    );
};

export default DeadsChartDetail;
