import React, { useContext } from 'react';
import { useTable } from 'react-table';
import { DateFormatting } from '../../Feauters';
import DataContext from '../../DataContext';
import { DeadsOarTable } from '../../Feauters';
import '../signout_detail_board/signout_table.css';



const DeadsOARDetailTable = ({ departament }) => {
  const oars = useContext(DataContext).kis;


  let deads = oars.oar_deads;
  deads = DeadsOarTable(deads);

  const filteredData = deads
  .filter(dict => dict['Отделение'] === departament)
  .map(({ Отделение, ...rest }) => rest);

  // Applying foramtting datetime field 
  const formattedArray = filteredData.map(item => ({
    ...item,
    'Дата поступления': DateFormatting(item['Дата поступления']),
  }));

  const columns = Object.keys(deads[0])
  .filter(key => key !== 'Отделение')
  .map(key => ({
    Header: key,
    accessor: key,
  }));

  // Create a table instance
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({
    columns,
    data: formattedArray, // Use filteredData directly
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

export default DeadsOARDetailTable;
