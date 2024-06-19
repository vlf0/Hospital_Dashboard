import React, { useContext } from 'react';
import { useTable } from 'react-table';
import DataContext from '../../DataContext';
import { PlanHospProcess } from '../../Feauters'
import '../signout_detail_board/signout_table.css';

const hospPlanColumns = ['Отделение', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс', 'Вне диапазона']

const PlanHospDetailTable = () => {

  let planHospData = useContext(DataContext).plan_hosp;
  const readyRuData = PlanHospProcess(planHospData);

  const columns = hospPlanColumns.map(key => ({
    Header: key,
    accessor: key,
  }))

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({
    columns,
    data: readyRuData,
  });


  return (
    <div className='deads-table-container'>
      <h2 className='detail_block_header'> Запланированные пациенты по дням </h2>
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

export default PlanHospDetailTable;