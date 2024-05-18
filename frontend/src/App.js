import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import GetAnalysis from './components/dashboard/Analysis';
import DetailBoard from './components/details/Details';
import DataContext from './components/DataContext';
import GetData from './components/GetData';
import NoConnection from './components/no_data/NoConnection';
import ArrivedDetails from './components/details/other_details/ArrivedDetails';



function App() {

  let mainData = sessionStorage.getItem('main_data')

  if (sessionStorage.getItem('main_data')) {
    mainData = JSON.parse(mainData)
  }
  else {
    const fetchedMainData = GetData('http://localhost:8000/api/v1/main_data/')
    const fethcedEmergencyData = GetData('http://localhost:8000/api/v1/emergency/')
    if (fetchedMainData && fethcedEmergencyData) {
      sessionStorage.setItem('main_data', JSON.stringify(fetchedMainData))
      sessionStorage.setItem('emergency_data', JSON.stringify(fethcedEmergencyData))
      mainData = JSON.parse(sessionStorage.getItem('main_data'))
    };
  }

  if (mainData !== null) {

    return (
      <DataContext.Provider value={mainData}>
        <Router>
          <Routes>
            <Route path="/" element={<GetAnalysis />} />
            <Route path="/arrived_detail" element={<DetailBoard sign={'in'} />} />
            <Route path="/signout_detail" element={<DetailBoard sign={'out'} />} />
            <Route path="/OAR_detail" element={<DetailBoard sign={'oar'} />} />
            <Route path="/details" element={<ArrivedDetails />} />
            <Route path="/emergency_detail" element={<DetailBoard sign={'emergencyRoom'} />} />

          </Routes>
        </Router>
      </DataContext.Provider>
    );
  }
  else {
    return (
      <>
        <NoConnection />
      </>
    );
  }
}

export default App;
