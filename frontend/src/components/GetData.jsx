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
    console.log(data);



    // Accessing specific properties of the first object
    const currentDay = data[1];
    const yesterday = data[0];


    const dates = [currentDay.dates, yesterday.dates];
    const arrived = [currentDay.arrived, yesterday.arrived];
    const hosp = [currentDay.hosp, yesterday.hosp];
    const refused = [currentDay.refused, yesterday.refused];
    const signout = [currentDay.signout, yesterday.signout];
    const deads = [currentDay.deads, yesterday.deads];
    const reanimation = [currentDay.reanimation, yesterday.reanimation];;

    
    return {
      dates, arrived, hosp, refused, signout, deads, reanimation
    };
};

export default GetData;