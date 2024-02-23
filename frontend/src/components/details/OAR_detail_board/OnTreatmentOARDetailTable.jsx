import React, { useContext } from 'react';
import { useTable } from 'react-table';
import { CurrentOarTable } from '../../Feauters';
import DataContext from '../../DataContext';
import '../signout_detail_board/signout_table.css';

const InOARDetailTable = ({ departament }) => {
  const oars = useContext(DataContext).kis[0];

  let current = oars.oar_current;
  current = CurrentOarTable(current);

  const filteredData = current
  .filter(dict => dict['Отделение'] === departament);

  const columns = Object.keys(current[0])
  .filter(key => key !== 'Отделение')
  .map(key => ({
    Header: key,
    accessor: key,
  }));

  // Create a table instance
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({
    columns,
    data: filteredData, // Use filteredData directly
  });

  return (
    <div className='deads-table-container'>
      <h2 className='detail_block_header'> Детализация по отделению </h2>
      <table className='deads-table' {...getTableProps()} >
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

export default InOARDetailTable;
