import React from 'react';
import { useTable } from 'react-table';
import ScaleX from '../ScaleX';

const SignInDetailTable = ({ data }) => {
  console.log(data);

  const columns = [
    { Header: 'Профиль', accessor: 'profile_name' },
    {
      Header: 'План',
      accessor: 'number',
      Cell: ({ cell }) => <ScaleX hospFact={cell.value} hospPlan={50} />, // Adjust this line
    },
  ];

  // Create a table instance
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({
    columns,
    data, // Use the provided data directly
  });

  return (
    <div className='detail_block_header'>
      ПЛАН/ФАКТ по профилям
      <table className='signin-table' {...getTableProps()}>
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
