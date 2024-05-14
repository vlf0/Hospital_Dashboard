import React, { useContext } from 'react';
import { useTable } from 'react-table';


const waitingColumns = ['ФИО пациента', '№ ИБ', 'Отделение', 'Время ожидания', 'ФИО врача']
const readyRuData = [
    ['Малышева Ольга Викторовна', '256-24', 'Неврологическое отделение', '145', 'Рыкова О.В.'],
    ['Бобров Павел Максимович.', '302-24', 'Кардиологическое отделение','129', 'Буйлов А.В.']
]

const WaitingDetailTable = () => {

    const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({
      columns: waitingColumns.map(column => ({
        Header: column,
        accessor: column,
      })),
      data: readyRuData.map(dataRow =>  Object.fromEntries(waitingColumns.map((col, index) => [col, dataRow[index]]))),
    });

    return (
      <>
        <span className='detail_block_header'> Детализация по превышенному времени ожидания </span>
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
      </>
    );
};

export default WaitingDetailTable;