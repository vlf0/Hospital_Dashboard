import React, { useState, useEffect, useCallback } from 'react';
import { useLocation } from 'react-router-dom';

const ArrivedDetails = () => {
    const location = useLocation();

    const date = new URLSearchParams(location.search).get('date');
    const srcUrl = window.location.href;
    const urlParams = srcUrl.split('/').pop();
    const dataType = srcUrl.split('=')[1].split('&')[0];  

    const [detailsData, setDetailsData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    const fetchDataFromApi = useCallback(async () => {
        try {
            let newData;

            // Check if data with the specified key exists in sessionStorage
            const storedData = sessionStorage.getItem(`${dataType}_${date}`);
            if (storedData) {
                // If data exists, parse it and setDetailsData
                newData = JSON.parse(storedData);
            } else {
                // If data doesn't exist, fetch it from the API
                const response = await fetch(`http://localhost:8000/api/v1/${urlParams}`);
                newData = await response.json();

                // Save the fetched data to sessionStorage
                sessionStorage.setItem(`${dataType}_${date}`, JSON.stringify(newData));
            }

            setDetailsData(newData);
            setIsLoading(false); // Set loading to false after data is fetched
        } catch (error) {
            console.error('Error fetching new data:', error);
            setIsLoading(false); // Set loading to false in case of error
        }
    }, [dataType, date, urlParams]);

    useEffect(() => {
        fetchDataFromApi(); // Fetch data when component mounts
    }, [fetchDataFromApi]);

    console.log(detailsData['data'])


    
    return (
        <div>
            {isLoading ? (
                <h2>Loading...</h2>
            ) : (
                <>
                    <div className='details'>{JSON.stringify(detailsData['data'][0]['ch103'])}</div>
                    <h2>Details for Bar: {urlParams}</h2>
                </>
            )}
        </div>
    );


    
};

export default ArrivedDetails;
