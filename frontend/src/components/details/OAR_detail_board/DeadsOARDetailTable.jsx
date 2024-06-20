import React, { useContext } from 'react';
import { useTable } from 'react-table';
import DataContext from '../../DataContext';
import { DeadsOarTable } from '../../Feauters';
import '../signout_detail_board/signout_table.css';



const oarDeadsColumns = ['ФИО', '№ ИБ', 'Пол', 'Возраст', 'Дата поступления',
                         'Состояние при поступлении', 'Кол-во койко дней',
                         'Диaгноз при поступлении', 'Диaгноз при выписке']


const DeadsOARDetailTable = ({ departament }) => {
  const oars = useContext(DataContext).kis;

  let deads;
  let filteredData;

  if (oars.deads.length > 0) {
    deads = DeadsOarTable(oars.deads);
    filteredData = deads
      .sort((a, b) => {
        if (a['ФИО'] < b['ФИО']) return -1;
        if (a['ФИО'] > b['ФИО']) return 1;
        return 0;
      })
      .filter(dict => dict['Отделение'] === departament)
      .map(({ Отделение, ...rest }) => rest);
  } else {
    filteredData = [];
  }

  const columns = oarDeadsColumns.map(key => ({
    Header: key,
    accessor: key,
  }));

  // Create a table instance
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({
    columns,
    data: filteredData, 
  });

  return (
    <div className='deads-table-container'>
      <h2 className='detail_block_header'> Детализация по отделению </h2>
      <table className='table' {...getTableProps()} >
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps()}>{column.render('Header')}</th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map(row => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map(cell => (
                  <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default DeadsOARDetailTable;
