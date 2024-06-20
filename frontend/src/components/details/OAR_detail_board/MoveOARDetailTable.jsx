import React, { useContext } from 'react';
import { useTable } from 'react-table';
import { MovedOarTable } from '../../Feauters';
import DataContext from '../../DataContext';
import '../signout_detail_board/signout_table.css';

const moveOarColumns = ['ФИО', '№ ИБ', 'Возраст', 'Лечащий врач', 
                        'Диагноз при поступлении', 'Дата перевода', 'Переведён из']

const MoveOARDetailTable = ({ departament }) => {
  const oars = useContext(DataContext).kis;

  let moved;
  let filteredData;

  if (oars.oar_moved.length > 0) {
    moved = MovedOarTable(oars.oar_moved);
    filteredData = moved
      .sort((a, b) => {
        if (a['ФИО'] < b['ФИО']) return -1;
        if (a['ФИО'] > b['ФИО']) return 1;
        return 0;
      })
      .filter(dict => dict['Отделение'] === departament)
      .map(({ Отделение, ...rest }) => rest);
  } else {
    filteredData = [];
  }

  const columns = moveOarColumns.map(key => ({
    Header: key,
    accessor: key,
  }));


  // Create a table instance
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({
    columns,
    data: filteredData, 
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

export default MoveOARDetailTable;
