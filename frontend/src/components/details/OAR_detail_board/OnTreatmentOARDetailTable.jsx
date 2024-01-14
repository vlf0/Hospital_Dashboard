import React from 'react';
import { useTable } from 'react-table';
import '../signout_detail_board/signout_table.css';


const oarDetail = [
                      ['Иван', 126, 43, 'ОРИТ №2', 'Климов А.Е.', 3, 'J06.9'],
                      ['Ольга', 126, 43, 'ОРИТ №1', 'Молунова В.В.', 6, 'G80.3'],
                      ['Олег', 126, 43, 'ОРИТ №2', 'Красиков Е.Н.', 1, 'E80.0'],
                      ['Ольга', 126, 43, 'ОРИТ №3', 'Быков А.И.', 4, 'K76.2'],
                    ];

const columnAccessorMap = {
  'ФИО': 0,
  '№ ИБ': 1,
  'возраст': 2,
  'отделение': 3,
  'лечащий врач': 4,
  'кол-во койко дней': 5,
  'диагноз при поступлении': 6,
};


const OnTreatmentOARDetailTable = ({ departament }) => {

  const filteredData = oarDetail.filter(tuple => tuple[columnAccessorMap['отделение']] === departament);

  const data = filteredData.map(tuple => {
    return {
      'ФИО': tuple[columnAccessorMap['ФИО']],
      '№ ИБ': tuple[columnAccessorMap['№ ИБ']],
      'возраст': tuple[columnAccessorMap['возраст']],
      // 'отделение': tuple[columnAccessorMap['отделение']],
      'лечащий врач': tuple[columnAccessorMap['лечащий врач']],
      'кол-во койко дней': tuple[columnAccessorMap['кол-во койко дней']],
      'диагноз при поступлении': tuple[columnAccessorMap['диагноз при поступлении']],
    };
  });
  
  // Define columns
  const columns = [
    { Header: 'ФИО', accessor: 'ФИО' },
    { Header: '№ ИБ', accessor: '№ ИБ' },
    { Header: 'Возраст', accessor: 'возраст' },
    // { Header: 'Отделение', accessor: 'отделение' },
    { Header: 'Лечащий врач', accessor: 'лечащий врач' },
    { Header: 'Кол-во койко дней', accessor: 'кол-во койко дней' },
    { Header: 'Диагноз при поступлении', accessor: 'диагноз при поступлении' },
  ];
  
    // Create a table instance
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({ columns, data });
  return (
    <div className='deads-table-container'>
      <h2 className='detail_block_header'> Детализация по отделению </h2>
      <table className='deads-table' {...getTableProps()} >
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

export default OnTreatmentOARDetailTable;
