import React, { useMemo } from "react";
import { useTable } from "react-table";
import { FaRegTrashAlt, FaPen } from "react-icons/fa";

const DepartmentEntryForm = () => {

    const deleteButtonClicked = (id) => {
        console.log(id);
    }
    const columns = useMemo(
        () => [
            {
                Header: "ID",
                accessor: "id",
            },
            {
                Header: "Department Name",
                accessor: "name",
            },
        ],
        []
    );

    const data = useMemo(() => [
        {
            id: "1",
            name: "account",
        },
        {
            id: "2",
            name: "admin",
        },
    ]);

    console.log(data);
    const tableHooks = (hooks) => {
        hooks.visibleColumns.push((columns) => [
            ...columns,
            {
                id: "actions",
                Header: "Actions",
                Cell: ({ row }) => (
                    <div className="flex justify-center gap-4">
                        <div
                            className="p-1.5 dark:bg-redAccent-700 rounded bg-redAccent-500 dark:hover:bg-redAccent-500 hover:bg-redAccent-700"
                            onClick={() => deleteButtonClicked(row.values.id)}
                        >
                            <FaRegTrashAlt className="h-4" />
                        </div>
                        <div
                            className="p-1.5 dark:bg-teal-700 rounded bg-teal-600 dark:hover:bg-teal-600 hover:bg-teal-700"
                            // onClick={() => editCompanyPopoverHandler(row.values)}
                        >
                            <FaPen className="h-4" />
                        </div>
                    </div>
                ),
            },
        ]);
    };

    const tableInstance = useTable({ columns, data }, tableHooks);
    const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = tableInstance;



    return (
        <section className="mx-6 mt-2">
            <div className="overflow-hidden rounded border border-black border-opacity-50 shadow-md m-5 max-w-5xl mx-auto">
                <table className="w-full border-collapse text-center text-sm" {...getTableProps()}>
                    <thead className="bg-blueAccet-600 dark:bg-blueAccent-700">
                        {headerGroups.map((headerGroup) => (
                            <tr {...headerGroup.getHeaderGroupProps()}>
                                {headerGroup.headers.map((column) => (
                                    <th scope="col" className="px-6 py-4 font-medium" {...column.getHeaderProps()}>
                                        {column.render("Header")}
                                    </th>
                                ))}
                            </tr>
                        ))}
                    </thead>
                    <tbody
                        className="divide-y divide-black divide-opacity-50 border-t border-black border-opacity-50"
                        {...getTableBodyProps()}
                    >
                        {rows.map((row) => {
                            prepareRow(row);
                            return (
                                <tr className="dark:hover:bg-zinc-800 hover:bg-zinc-200" {...row.getRowProps()}>
                                    {row.cells.map((cell) => {
                                        return (
                                            <td className="px-6 py-4 font-normal" {...cell.getCellProps()}>
                                                <div className="text-sm">
                                                    <div className="font-medium">{cell.render("Cell")}</div>
                                                </div>
                                            </td>
                                        );
                                    })}
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </section>
    );
};

export default DepartmentEntryForm;
