import React from "react";
import { useTable } from 'react-table';
import { RefuseDetailTableProcess } from "../../../Feauters";

const refuseDetailColumns = ['ФИО пациента', '№ ИБ', 'Диагноз', 'Причина отказа', 'Дата отказа'];


const RefuseDetailTable = React.memo(({ doctorName }) => {

  let refuseDetailData = sessionStorage.getItem('emergency_data');
  refuseDetailData = refuseDetailData ? JSON.parse(refuseDetailData) : null;
  const flattenDetailArray = refuseDetailData.detail_refuses.flat();
  const readyRuData = refuseDetailData ? RefuseDetailTableProcess(flattenDetailArray) : [];
  const filteredData = readyRuData.filter(dict => dict['ФИО врача'] === doctorName);

  const columns = React.useMemo(() =>
    refuseDetailColumns.map(column => ({
      Header: column,
      accessor: column,
    })),
    []
  );

  const data = React.useMemo(() => filteredData, [filteredData]);

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({ columns, data });

  return (
    <div className='deads-table-container'>
      <span className='detail_block_header'> Детализация отказов по врачу {doctorName} </span>
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
    </div>
  );
});

export default RefuseDetailTable;
