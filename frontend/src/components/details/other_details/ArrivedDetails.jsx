import React, { useState, useEffect, useCallback } from 'react';
import { useLocation } from 'react-router-dom';

const ArrivedDetails = () => {
    const location = useLocation();
    const date = new URLSearchParams(location.search).get('date');


    const [detailsData, setDetailsData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    const fetchDataFromApi = useCallback(async () => {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/details/?type=arrived&date=${date}`);
            const newData = await response.json();

            // Update sessionStorage with the new data
            sessionStorage.setItem('kis', JSON.stringify(newData));
            setDetailsData(newData); // Set the state with new data
            setIsLoading(false); // Set loading to false after data is fetched

        } catch (error) {
            console.error('Error fetching new data:', error);
            setIsLoading(false); // Set loading to false in case of error
        }
    }, [date]); // Empty dependency array ensures it only gets created once

    useEffect(() => {
        fetchDataFromApi(); // Fetch data when component mounts
    }, [fetchDataFromApi]); // Include fetchDataFromApi in the dependency array

    return (
        <div>
            {isLoading ? (
                <h2>Loading...</h2>
            ) : (
                <>
                    <h2>{detailsData && JSON.stringify(detailsData)}</h2>
                    <h2>Details for Bar: {date}</h2>
                </>
            )}
        </div>
    );
};

export default ArrivedDetails;
