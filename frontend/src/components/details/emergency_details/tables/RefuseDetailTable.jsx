import React from "react";
import { useTable } from 'react-table';


const refuseDetailColumns = ['ФИО пациента', '№ ИБ', 'Диагноз', 'Причина отказа', 'Дата отказа']
const readyRuData = [
    ['Орлова Виктория Олеговна', '256-24', 'Неврологическое отделение', 'Не соответсвует профилю', '14.05.2024'],
    ['Шнуров Александр Павлович', '302-24', 'Кардиологическое отделение', 'Не соответсвует профилю', '14.05.2024']
]

const NewTable = ({ doctorName }) => {

    const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({
        columns: refuseDetailColumns.map(column => ({
            Header: column,
            accessor: column,
        })),
        data: readyRuData.map(dataRow =>  Object.fromEntries(refuseDetailColumns.map((col, index) => [col, dataRow[index]]))),
    });


    return (
        <div className='deads-table-container'>
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
};


export default NewTable;