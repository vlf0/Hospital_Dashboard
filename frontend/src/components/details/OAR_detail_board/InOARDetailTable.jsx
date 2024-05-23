import React, { useContext } from 'react';
import { useTable } from 'react-table';
import { ArrivedOarTable } from '../../Feauters';
import DataContext from '../../DataContext';
import '../signout_detail_board/signout_table.css';




const InOARDetailTable = ({ departament }) => {
  const oars = useContext(DataContext).kis;

  let arrived = oars.oar_arrived;
  arrived = ArrivedOarTable(arrived);

  // Отделение реанимации и интенсивной терапии № 1
  const filteredData = arrived
      .filter(dict => dict['Отделение'] === departament)
      .map(({ Отделение, ...rest }) => rest);

  const columns = Object.keys(arrived[0])
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

export default InOARDetailTable;
