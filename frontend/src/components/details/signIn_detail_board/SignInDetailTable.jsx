import React from 'react';
import { useTable } from 'react-table';
import ScaleX from '../ScaleX';

const SignInDetailTable = ({data}) => {

  // Full List of profiles corresponding for mapping
  const profilesMap = {
    'cardiology': 'Кардиология',
    'surgery': 'Хирургия',
    'therapy': 'Терапия',
    'neurology': 'Неврология',
    'urology': 'Урология'
  }

  // Processing received data dict to get separated lists of values and then mapping
  const enProfiles = Object.keys(data); //List of depts from KISDB
  const ruProfiles = enProfiles.map(profile => profilesMap[profile]);
  const numbers = Object.values(data); //List of fact arrived patients
  const combinedData = ruProfiles.map((profile, index) => ({ профиль: profile, план: numbers[index] }));
  
/* NEED IMPLEMENT SAVING AND STORAGE depts_hosp data FOR CUMULATING FACT DATA*/
  const columns = [
    { Header: 'Профиль', accessor: 'профиль' },
    { Header: 'План', accessor: 'план', Cell: ({ row }) => <ScaleX arrivedFact={row.original.план} /> },
  ];

  // Create a table instance
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({ columns, data: combinedData });

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
