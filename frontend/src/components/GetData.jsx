import {useState, useEffect} from "react";


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

    return data;
};

export default GetData;