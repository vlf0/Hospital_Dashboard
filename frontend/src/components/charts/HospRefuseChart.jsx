import React from 'react';
// import { useSpring, animated } from 'react-spring';
import { Bar } from 'react-chartjs-2';
import Chart from 'chart.js/auto';
import "./arrived_chart.css";


Chart.defaults.font.size = 12;
Chart.defaults.color = '#090b1f';  


const HospRefuseChart = () => {

    const hosp_refuse_data = {
        labels: ['Вчера', 'Сегодня'],
        datasets: [
            {
                label: 'Госпитализации',
                data: [94, 84],//data ? [data.data, data.data, data.data] : [10,20,10],
                backgroundColor: ['#289c22', '#289c22'],
                borderColor: '#090b1f',
                borderWidth: 1,
                // barThickness: 30
            },
            {
                label: 'Отказы',
                data: [29, 15],//data ? [data.data, data.data, data.data] : [10,20,10],
                backgroundColor: ['#994228', '#994228'],
                borderColor: '#090b1f',
                borderWidth: 1,
                // barThickness: 30
            }
        ]
    };

    const chartOptions = {
        scales: {
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    beginAtZero: true,
                    color: '#090b1f',   
                    font: {
                        // size: 14,
                        weight: 'bold' // Set the font weight to bold
                        
                    },
                },
            },
            y: {
                // min: -20, // Set the minimum value
                // max: 150, // Set the maximum value
                grid: {
                    // display: false,
                },
                ticks: {
                    beginAtZero: true,
                    color: '#090b1f',
                    stepSize: 20, // Set the interval between ticks
                    font: {
                        // size: 14,
                        weight: 'bold' // Set the font weight to bold
                        
                    },
                }
            },
        },
        barThickness: 'flex',
        // maxBarThickness: 30,  
        barPercentage: 0.9, // Adjust the space between columns (0.8 means 80% of the available space)
        categoryPercentage: 0.6,
        plugins: {
            datalabels: {
                display: false
            },
            legend: {
                display: true,
            },
            title: {
                display: true,
                text: 'Отношение госпитализированных к отказным',
                color: '#090b1f',
            },
        },
    };

    // Chart component
    return (
        <div className='arrived_chart'>
          <Bar data={hosp_refuse_data} options={chartOptions} />
        </div>

        // Code for animation chart itself
        // <animated.div className='arrived_chart' style={props}>
        //     <Bar data={arrived_data} options={chartOptions} />
        // </animated.div>
    );

}

export default HospRefuseChart;
