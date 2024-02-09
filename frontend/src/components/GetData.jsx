import React, {useState, useEffect} from "react";


function Persents(today, yesterday) {

  let percent = ((today-yesterday)/yesterday*100).toFixed(1)
  percent = percent.toString() + '%'
  percent = percent.replace('-', '');
  return percent
};

function ensureArrayLength(array, desiredLength) {
  if (array.length !== desiredLength) {
    const numberOfTimesToInsert = desiredLength - array.length;

    for (let i = 0; i < numberOfTimesToInsert; i++) {
      array.unshift(null);
    }
  }
};

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
    // const currentDay = data[data.length - 1];
    // const yesterday = data[data.length - 2];

    // const arrivedArray = data.map(obj => obj.arrived);
    // const signOutArray = data.map(obj => obj.signout);
    // const deadsArray = data.map(obj => obj.deads);
    // ensureArrayLength(arrivedArray, 7);
    // ensureArrayLength(signOutArray, 7);
    // ensureArrayLength(deadsArray, 7);

    // const dates = [currentDay.dates, yesterday.dates];
    // const arrived = [currentDay.arrived, yesterday.arrived, Persents(currentDay.arrived, yesterday.arrived)];
    // const hosp = [currentDay.hosp, yesterday.hosp, Persents(currentDay.hosp, yesterday.hosp)];
    // const refused = [currentDay.refused, yesterday.refused, Persents(currentDay.refused, yesterday.refused)];
    // const signout = [currentDay.signout, yesterday.signout, Persents(currentDay.signout, yesterday.signout)];
    // const deads = [currentDay.deads, yesterday.deads, Persents(currentDay.deads, yesterday.deads)];
    // const reanimation = [currentDay.reanimation, yesterday.reanimation, Persents(currentDay.reanimation, yesterday.reanimation)];

    
    // return {
    //   dates, arrived, hosp, refused, signout, deads, reanimation,
    //   arrivedArray, signOutArray, deadsArray
    // };
    return {data};

};

export default GetData;