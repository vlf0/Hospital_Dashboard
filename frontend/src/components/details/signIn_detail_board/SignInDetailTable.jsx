import React from 'react';
import { useTable } from 'react-table';
import ScaleX from '../ScaleX';

const SignInDetailTable = ({ data }) => {
  // Define columns
  const columns = [
    { Header: 'Профиль', accessor: 'профиль' },
    { Header: 'План', accessor: 'план', Cell: ({ row }) => <ScaleX arrivedFact={row.original.план} /> },
  ];

  // Create a table instance
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({ columns, data });

  return (
    <div className='detail_block_header'> ПЛАН/ФАКТ по профилям
      <table className='signin-table' {...getTableProps()} >
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

export default SignInDetailTable;
