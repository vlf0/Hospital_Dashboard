import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import GetAnalysis from './components/dashboard/Analysis';
import DetailBoard from './components/details/Details';



function App() {


  return (
      <Routes>
        <Route path="/" element={<GetAnalysis />} />
        <Route path="/arrived_detail" element={<DetailBoard sign={'in'} textHeader={'Детализация обратившихся'} />} />
        <Route path="/signout_detail" element={<DetailBoard sign={'out'} textHeader={'Детализация выписанных'} />} />
        <Route path="/OAR_detail" element={<DetailBoard sign={'oar'} textHeader={'Детализация реанимационных отделений'} />} />
      </Routes>
  );
}

export default App;
