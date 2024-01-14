import React from 'react';
import { useTable } from 'react-table';
import '../signout_detail_board/signout_table.css';


const oarDetail = [
                      ['Иван', 126, 43, 'ОРИТ №1', 'Климов А.Е.', '4.01.2024', 'Неврологическое', 'J06.9'],
                      ['Ольга', 126, 43, 'ОРИТ №2', 'Молунова В.В.', '6.01.2024', 'Кардиологическое', 'G80.3'],
                      ['Олег', 126, 43, 'ОРИТ №3', 'Красиков Е.Н.', '1.01.2024', 'Урологическое', 'E80.0'],
                      ['Ольга', 126, 43, 'ОРИТ №2', 'Быков А.И.', '9.01.2024', 'Хирургическое', 'K76.2'],
                    ];

const columnAccessorMap = {
  'ФИО': 0,
  '№ ИБ': 1,
  'возраст': 2,
  'отделение': 3,
  'лечащий врач': 4,
  'дата перевода': 5,
  'переведен из': 6,
  'диагноз при поступлении': 7,
};


const MoveOARDetailTable = ({ departament }) => {

  const filteredData = oarDetail.filter(tuple => tuple[columnAccessorMap['отделение']] === departament);

  // Sample data
  const data = filteredData.map(tuple => {
    return {
      'ФИО': tuple[columnAccessorMap['ФИО']],
      '№ ИБ': tuple[columnAccessorMap['№ ИБ']],
      'возраст': tuple[columnAccessorMap['возраст']],
      // 'отделение': tuple[columnAccessorMap['отделение']],
      'лечащий врач': tuple[columnAccessorMap['лечащий врач']],
      'дата перевода': tuple[columnAccessorMap['дата перевода']],
      'переведен из': tuple[columnAccessorMap['переведен из']],
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
    { Header: 'Дата перевода', accessor: 'дата перевода' },
    { Header: 'Переведен из', accessor: 'переведен из' },
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

export default MoveOARDetailTable;
