import React, { useEffect } from 'react';
import { useTable } from 'react-table';
import ScaleX from '../ScaleX';


const SignInDetailTable = () => {

    let data = JSON.parse(sessionStorage.getItem('data')).dmk.accum_dmk

  const columns = [
    { Header: 'Профиль', 
      accessor: 'name',
        Cell: ({ cell }) => (
          <div style={{ 
            color: '#1a1a1a', // Text color
            fontSize: 16,     // Font size
            fontWeight: 700,  // Font weight
            fontFamily: 'sans-serif', // Font family
          }}>{cell.value}</div>
    ) },
    {
      Header: 'План',
      accessor: 'total',
      Cell: ({ cell, row }) => (<ScaleX hospFact={cell.value} hospPlan={row.original.plan} />), 
    },
    {
      Header: 'Percents',
      Cell: ({ row }) => {
        const percent = ((row.values.total / row.original.plan) * 100);
        const formattedPercent = percent.toFixed(0) + '%'; // Add "%" at the end
        return <div style={{ color: percent > 100 ? '#12702b' : '#47010f',
                             fontSize: 14,
                             fontWeight: 700,
                             fontFamily: 'sans-serif'
                            }
                          }>{formattedPercent}</div>;
      }
    }
  ];

  // Create a table instance
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({
    columns,
    data, // Use the provided data directly
  });

  
  // Use useEffect to trigger table update when data changes
  useEffect(() => {
    prepareRow(rows);
  }, [data, prepareRow, rows]);

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
