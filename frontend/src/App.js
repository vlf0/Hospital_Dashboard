import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import GetAnalysis from './components/dashboard/Analysis';
import DetailBoard from './components/details/Details';
import DataContext from './components/DataContext';
import GetData from './components/GetData';
import NoConnection from './components/NoConnection';
import ArrivedDetails from './components/details/other_details/ArrivedDetails';



function App() {

  let data = sessionStorage.getItem('data')

  if (sessionStorage.getItem('data')) {
    data = JSON.parse(data)
  }
  else {
    const fetchedData = GetData('http://localhost:8000/api/v1/main_data/')
    if (fetchedData) {
      sessionStorage.setItem('data', JSON.stringify(fetchedData))
      data = JSON.parse(sessionStorage.getItem('data'))
    };
  }


  if (data) {

    return (
      <DataContext.Provider value={data}>
        <Router>
          <Routes>
            <Route path="/" element={<GetAnalysis />} />
            <Route path="/arrived_detail" element={<DetailBoard sign={'in'} textHeader={'Детализация обратившихся'} />} />
            <Route path="/signout_detail" element={<DetailBoard sign={'out'} textHeader={'Детализация выписанных'} />} />
            <Route path="/OAR_detail" element={<DetailBoard sign={'oar'} textHeader={'Детализация реанимационных отделений'} />} />
            <Route path="/details" element={<ArrivedDetails />} />
            {/* <Route path="/arrived" element={<ArrivedDetails />} /> */}
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
