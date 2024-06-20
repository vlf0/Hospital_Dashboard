import React from 'react';
import { useTable } from 'react-table';
import NoData from '../../../no_data/NoData';
import { EmergencyTableProcess } from '../../../Feauters';

const waitingColumns = ['ФИО пациента', '№ ИБ', 'Отделение', 'Время ожидания', 'ФИО врача'];

const WaitingDetailTable = () => {

  let waitingData = sessionStorage.getItem('emergency_data');
  waitingData = waitingData ? JSON.parse(waitingData) : null;

  const readyRuData = waitingData ? EmergencyTableProcess(waitingData.waitings).sort((a, b) => {
    if (a['ФИО пациента'] < b['ФИО пациента']) return -1;
    if (a['ФИО пациента'] > b['ФИО пациента']) return 1;
    return 0;
  }) : [];

  const columns = waitingColumns.map(key => ({
    Header: key,
    accessor: key,
  }));

  const tableInstance = useTable({
    columns,
    data: readyRuData
  });

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = tableInstance;

  return (
    <>
      <span className='detail_block_header'> Детализация по превышенному времени ожидания </span>
      {waitingData ? (
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
      ) : (
        <NoData />
      )}
    </>
  );
};

export default WaitingDetailTable;
