import React, { useContext } from 'react';
import { useTable } from 'react-table';
import DataContext from '../../DataContext';
import { DeadTableProcess } from '../../Feauters';
import './signout_table.css';


const deadsColumns = ['ФИО', '№ ИБ', 'Пол', 'Возраст', 'Отделение', 'Дата поступления',
                      'Состояние при поступлении', 'Кол-во койко дней',
                      'Диагноз при поступлении', 'Диагноз при выписке', 'Лечащий врач']

const SignOutDetailTable = () => {
  let kisDeads = useContext(DataContext).kis;
  kisDeads = kisDeads.deads;
  const readyRuData = DeadTableProcess(kisDeads).sort((a, b) => {
    if (a['ФИО'] < b['ФИО']) return -1;
    if (a['ФИО'] > b['ФИО']) return 1;
    return 0;
  });

  const columns = deadsColumns.map(key => ({
    Header: key,
    accessor: key,
  }))

  // Create a table instance
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({
    columns,
    data: readyRuData,
  });

  return (
    <div className='deads-table-container'>
      <h2 className='detail_block_header'> Детализация по умершим </h2>
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

export default SignOutDetailTable;
