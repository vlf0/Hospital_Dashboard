import React, { useContext } from 'react';
import { useTable } from 'react-table';
import DataContext from "../../DataContext";
import { DeadTableProcess } from '../../Feauters';
import './signout_table.css';


const deadsColumns = ['ФИО', '№ ИБ', 'Пол', 'Возраст', 'Отделение', 'Дата поступления',
                      'Состояние при поступлении', 'Кол-во койко дней',
                      'Диагноз при поступлении', 'Диагноз при выписке', 'Лечащий врач']

const SignOutDetailTable = () => {
  let kisDeads = useContext(DataContext).kis;
  kisDeads = kisDeads.deads;
  const readyRuData = DeadTableProcess(kisDeads);

  let columns;

  if (readyRuData.length !== 0) {
  // Define columns
    columns = Object.keys(readyRuData[0]).map(key => ({
      Header: key,
      accessor: key,
    }))} else {
    columns = deadsColumns.map(key => ({
      Header: key,
      accessor: key,
    }))
  }

  // Create a table instance
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({
    columns,
    data: readyRuData, // Wrap readyRuData in an array to use with react-table
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
