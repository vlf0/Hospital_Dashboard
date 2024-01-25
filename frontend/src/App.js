import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import GetAnalysis from './components/dashboard/Analysis';
import DetailBoard from './components/details/Details';
import DataContext from './components/DataContext';
import { storedData } from './components/dashboard/Analysis';




function App() {
  return (
  <DataContext.Provider value={storedData}>
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
