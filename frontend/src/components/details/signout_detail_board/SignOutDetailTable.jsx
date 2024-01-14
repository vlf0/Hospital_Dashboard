import React from 'react';
import { useTable } from 'react-table';
import './signout_table.css';


const deadsDetail = [
                      ['Иван', 126, 'муж', 43, '2.01.2024', 'тяжелое', 8, 'J06.9', 'U07.1'],
                      ['Ольга', 126, 'жен', 43, '4.01.2024', 'срежней тяжести', 5, 'G80.3', 'U07.1'],
                      ['Олег', 126, 'муж', 43, '7.01.2024', 'срежней тяжести', 4, 'E80.0', 'U07.2'],
                      ['Ольга', 126, 'жен', 43, '3.01.2024', 'крайне тяжелое', 9, 'K76.2', 'U07.1'],
                    ];

const columnAccessorMap = {
  'ФИО': 0,
  '№ ИБ': 1,
  'пол': 2,
  'возраст': 3,
  'дата поступления': 4,
  'состояние при поступлении': 5,
  'кол-во койко дней': 6,
  'дигноз при поступлении': 7,
  'дигноз при выписке': 8,
};


const SignOutDetailTable = () => {
    // Sample data
    const data = deadsDetail.map(tuple => {
      return {
        'ФИО': tuple[columnAccessorMap['ФИО']],
        '№ ИБ': tuple[columnAccessorMap['№ ИБ']],
        'пол': tuple[columnAccessorMap['пол']],
        'возраст': tuple[columnAccessorMap['возраст']],
        'дата поступления': tuple[columnAccessorMap['дата поступления']],
        'состояние при поступлении': tuple[columnAccessorMap['состояние при поступлении']],
        'кол-во койко дней': tuple[columnAccessorMap['кол-во койко дней']],
        'дигноз при поступлении': tuple[columnAccessorMap['дигноз при поступлении']],
        'дигноз при выписке': tuple[columnAccessorMap['дигноз при выписке']],
      };
    });
  
    // Define columns
    const columns = [
      { Header: 'ФИО', accessor: 'ФИО' },
      { Header: '№ ИБ', accessor: '№ ИБ' },
      { Header: 'Пол', accessor: 'пол' },
      { Header: 'Возраст', accessor: 'возраст' },
      { Header: 'Дата поступления', accessor: 'дата поступления' },
      { Header: 'Состояние при поступлении', accessor: 'состояние при поступлении' },
      { Header: 'Кол-во койко дней', accessor: 'кол-во койко дней' },
      { Header: 'Дигноз при поступлении', accessor: 'дигноз при поступлении' },
      { Header: 'Дигноз при выписке', accessor: 'дигноз при выписке' },

    ];
  
    // Create a table instance
    const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({ columns, data });

    return (
      <div className='deads-table-container'>
        <h2 className='detail_block_header'> Детализация по умершим </h2>
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

export default SignOutDetailTable;
