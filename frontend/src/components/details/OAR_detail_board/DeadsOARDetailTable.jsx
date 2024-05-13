import React, { useContext } from 'react';
import { useTable } from 'react-table';
import DataContext from '../../DataContext';
import { DeadsOarTable } from '../../Feauters';
import '../signout_detail_board/signout_table.css';



const oarDeadsColumns = ['ФИО', '№ ИБ', 'Пол', 'Возраст', 'Дата поступления',
                      'Состояние при поступлении', 'Кол-во койко дней',
                      'Дигноз при поступлении', 'Дигноз при выписке']


const DeadsOARDetailTable = ({ departament }) => {
  const oars = useContext(DataContext).kis;


  let deads = oars.oar_deads;
  deads = DeadsOarTable(deads);



  let filteredData;
  let columns;

  if (deads.length !== 0) {

    filteredData = deads
    .filter(dict => dict['Отделение'] === departament)
    .map(({ Отделение, ...rest }) => rest);

    columns = Object.keys(deads[0])
    .filter(key => key !== 'Отделение')
    .map(key => ({
      Header: key,
      accessor: key,
    }));
  } else {
    filteredData = [];
    columns = oarDeadsColumns.map(key => ({
      Header: key,
      accessor: key,
    }));
  }


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
