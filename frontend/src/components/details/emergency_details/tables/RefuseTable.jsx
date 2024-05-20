import React from 'react';
import { useTable } from 'react-table';
import { TotalRefuseTableProcess } from '../../../Feauters';
import NoData from '../../../no_data/NoData';


const refuseColumns = ['ФИО врача', 'кол-во отказов'];


const RefuseTable = React.memo(({ onRowClick }) => {

  let refuseData = null;
  refuseData = refuseData ? JSON.parse(refuseData) : null;


  // const readyRuData = refuseData ? TotalRefuseTableProcess(refuseData.total_refuses) : [];

  const columns = React.useMemo(() =>
    refuseColumns.map(column => ({
      Header: column,
      accessor: column,
    })),
    []
  );

  const data = React.useMemo(() => {
    return refuseData ? TotalRefuseTableProcess(refuseData.total_refuses) : [];
  }, [refuseData]);

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({ columns, data });

  return (
    <>
      <span className='detail_block_header'> Список сгруппированных отказов </span>
      {refuseData ? (
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
              <tr
                {...row.getRowProps()}
                onClick={() => onRowClick(row.original['ФИО врача'])}
              >
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
      )
      }
    </>
  );
});

export default RefuseTable;
