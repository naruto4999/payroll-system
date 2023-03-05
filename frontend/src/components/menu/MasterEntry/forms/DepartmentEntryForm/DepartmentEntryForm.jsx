import React, { useMemo, useState } from "react";
import { useTable } from "react-table";
import { FaRegTrashAlt, FaPen } from "react-icons/fa";
import { useSelector } from "react-redux";
import {
    useGetDepartmentsQuery,
    useAddDepartmentMutation,
} from "../../../../authentication/api/departmentEntryApiSlice";
import AddDepartment from "./AddDepartment";

const DepartmentEntryForm = () => {
    const globalCompany = useSelector((state) => state.globalCompany);
    // console.log(globalCompany)
    const { data: fetchedData, isLoading, isSuccess, isError, error } = useGetDepartmentsQuery(globalCompany);
    console.log(fetchedData)
    const [addDepartment, { isLoading: isAddingDepartment }] = useAddDepartmentMutation();
    const [addDepartmentPopover, setAddDepartmentPopover] = useState(false);
    const [newDepartment, setNewDepartment] = useState("");

    const addDepartmentPopoverHandler = () => {
        setAddDepartmentPopover(!addDepartmentPopover);
    };

    const addDepartmentChangeHandler = (event) => {
        setNewDepartment(event.target.value);
    };

    const addButtonClicked = () => {
        setAddDepartmentPopover(!addDepartmentPopover);
        addDepartment({
            company: { id: globalCompany.id, name: globalCompany.name },
            name: newDepartment,
        });
        console.log(isAddingDepartment);
        setNewDepartment("");
    };

    const deleteButtonClicked = (id) => {
        console.log(id);
    };
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

    const data = useMemo(() => (fetchedData ? [...fetchedData] : []), [fetchedData]);
    // console.log(newDepartment);

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
            <div className="flex flex-row place-content-between mx-5 mt-2">
                <div className="">
                    <h1 className="text-3xl font-medium">Departments</h1>
                    <p className="text-sm my-2">Add more departments here</p>
                </div>
                <button
                    className="dark:bg-teal-700 m-4 rounded p-2 text-base font-medium bg-teal-500 hover:bg-teal-600 dark:hover:bg-teal-600"
                    onClick={addDepartmentPopoverHandler}
                >
                    Add Department
                </button>
            </div>

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

                {addDepartmentPopover ? (
                    <AddDepartment
                        addDepartmentPopoverHandler={addDepartmentPopoverHandler}
                        addDepartmentChangeHandler={addDepartmentChangeHandler}
                        addButtonClicked={addButtonClicked}
                    />
                ) : (
                    ""
                )}
            </div>
        </section>
    );
};

export default DepartmentEntryForm;
