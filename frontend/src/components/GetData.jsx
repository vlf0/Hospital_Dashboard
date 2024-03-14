import {useState, useEffect} from "react";


function GetData(urlPath) {
    const [data, userData] = useState(null);
    
    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await fetch(urlPath);
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