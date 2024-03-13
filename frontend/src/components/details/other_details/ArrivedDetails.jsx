import React from 'react';
import { useLocation } from 'react-router-dom';

const ArrivedDetails = () => {
    const location = useLocation();
    const date = new URLSearchParams(location.search).get('date');

    return (
        <div>
            <h2>Details for Bar: {date}</h2>
        </div>
    );
};

export default ArrivedDetails;
