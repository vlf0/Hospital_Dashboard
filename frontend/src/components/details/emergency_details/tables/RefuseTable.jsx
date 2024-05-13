import React, { useContext } from 'react';
import { useTable } from 'react-table';


const refuseColumns = ['ФИО врача', 'кол-во отказов']
const readyData = ['Поляков И.С.', 13]

const RefuseDetailTable = () => {
    const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({
      columns: refuseColumns.map(column => ({
        Header: column,
        accessor: column,
      })),
      data: [Object.fromEntries(refuseColumns.map((col, index) => [col, readyData[index]]))], // Wrap readyData in an array and convert it to object
    });
  
    return (
      <div className='deads-table-container'>
        <table {...getTableProps()} className='table'>
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

export default RefuseDetailTable;