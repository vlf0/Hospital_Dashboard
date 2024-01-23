import React, {useState, useEffect} from "react";


function GetData() {
    const [data, userData] = useState(null);
    
    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await fetch('http://localhost:8000/api/v1/main_data/');
          const jsonData = await response.json();
          userData(jsonData);
        }
        catch (error) {
          console.error('Error fetching data:', error);
        }
      };
      fetchData();
    }, []);


    if (!data || data.length === 0) {
      return '';
    }
  
    // Accessing specific properties of the first object
    const firstData = data[0];
    const chosen_date = firstData.dates;
    const arrived = firstData.arrived;
    const hosp = firstData.hosp;
    const refused = firstData.refused;
    const signout = firstData.signout;
    const deads = firstData.deads;
    const reanimation = firstData.reanimation;
  

    
    return {
      chosen_date,
      arrived,
      hosp,
      refused,
      signout,
      deads,
      reanimation
    };
};

export default GetData;