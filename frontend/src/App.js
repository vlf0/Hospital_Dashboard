import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import GetAnalysis from './components/dashboard/Analysis';
import DetailBoard from './components/details/Details';
import DataContext from './components/DataContext';
import GetData from './components/GetData';




function App() {

  let data = sessionStorage.getItem('q')

  if (sessionStorage.getItem('q')) {
    data = JSON.parse(data)
  }
  else {
    const fetchedData = GetData()
    if (fetchedData) {
      console.log('get data')
      sessionStorage.setItem('q', JSON.stringify(fetchedData))
      data = JSON.parse(sessionStorage.getItem('q'))
    };
  }


  return (
  <DataContext.Provider value={data}>
    <Router>
      <Routes>
        <Route path="/" element={<GetAnalysis />} />
        <Route path="/arrived_detail" element={<DetailBoard sign={'in'} textHeader={'Детализация обратившихся'} />} />
        <Route path="/signout_detail" element={<DetailBoard sign={'out'} textHeader={'Детализация выписанных'} />} />
        <Route path="/OAR_detail" element={<DetailBoard sign={'oar'} textHeader={'Детализация реанимационных отделений'} />} />
      </Routes>
    </Router>
  // </DataContext.Provider>
  );
}

export default App;
