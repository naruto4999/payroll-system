import React, { useMemo } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useState } from "react";
import { useReactTable, useRowSelect } from '@tanstack/react-table'
import { FaRegTrashAlt, FaPen, FaCircleNotch, FaCheck, FaWindowMinimize } from "react-icons/fa";
import { useOutletContext } from "react-router-dom";
import { useEffect } from "react";

//imports after using RTK query
import {
    useGetCompaniesQuery,
    useVisibleCompanyMutation,
} from "../../authentication/api/newCompanyEntryApiSlice";
import ReactModal from "react-modal";
import { Formik } from "formik";

ReactModal.setAppElement("#root");

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const IndeterminateCheckbox = React.forwardRef(
    ({ indeterminate, ...rest }, ref) => {
        const defaultRef = React.useRef();
        const resolvedRef = ref || defaultRef;

        React.useEffect(() => {
            resolvedRef.current.indeterminate = indeterminate;
        }, [resolvedRef, indeterminate]);

        return (
            <label className="cursor-pointer relative flex flex-col ">
                <input
                    type="checkbox"
                    ref={resolvedRef}
                    className="appearance-none border border-slate-400 rounded-md w-5 h-5 peer"
                    {...rest}
                />
                { indeterminate ? (<FaWindowMinimize className="absolute text-teal-600 dark:text-teal-500 left-[3px] bottom-[7px]"/>) : (<FaCheck className="absolute text-teal-600 dark:text-teal-500 left-[3px] bottom-[3px] peer-[&:not(:checked)]:hidden"/>)}
                {console.log(rest)}
                {console.log(indeterminate)}
            </label>
        );
    }
);

const VisibleCompaniesForm = () => {
    //using RTK query
    const {
        data: fetchedData,
        isLoading,
        isSuccess,
        isError,
        error,
        isFetching,
    } = useGetCompaniesQuery();
    console.log(fetchedData);
    const [visibleCompany, { isLoading: isUpdatingVisibleCompanies }] =
        useVisibleCompanyMutation();
    const [showLoadingBar, setShowLoadingBar] = useOutletContext();
    const [confirmDelete, setConfirmDelete] = useState({ id: "", phrase: "" });
    const dispatch = useDispatch();

    const [updatedCompanyId, setUpdatedCompanyId] = useState();

    const editCompanyPopoverHandler = (company) => {
        setUpdatedCompanyId(company.id);
        setEditCompanyPopover(!editCompanyPopover);
    };

    const saveButtonClicked = async () => {
        const body = [];
        console.log(selectedFlatRows);
        for (let i = 0; i < selectedFlatRows.length; i++) {
            const original = selectedFlatRows[i].original;
            // Do something with the original property, for example:
            // console.log(original);
            body.push({
                company_id: original.id,
                visible: true,
            });
        }
        console.log(body);
        try {
            const data = await visibleCompany(body).unwrap();
            console.log(data);
        } catch (err) {
            console.log(err);
        }
    };

    const columns = useMemo(
        () => [
            {
                Header: "ID",
                accessor: "id",
            },
            {
                Header: "Company Name",
                accessor: "name",
            },
        ],
        []
    );

    const data = useMemo(
        () => (fetchedData ? [...fetchedData] : []),
        [fetchedData]
    );

    const tableHooks = (hooks) => {
        hooks.visibleColumns.push((columns) => [
            ...columns,
            {
                id: "selection",
                Header: ({ getToggleAllRowsSelectedProps }) => (
                    <div>
                        <IndeterminateCheckbox
                            {...getToggleAllRowsSelectedProps()}

                        />
                    </div>
                ),
                Cell: ({ row }) => (
                    <div>
                        <IndeterminateCheckbox
                            {...row.getToggleRowSelectedProps()}
                        />
                    </div>
                ),
            },
        ]);
    };

    const tableInstance = useTable({ columns, data }, useRowSelect, tableHooks);
    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow,
        selectedFlatRows,
        state: { selectedRowIds },
    } = tableInstance;

    console.log(rows);
    console.log(selectedRowIds);
    // console.log(showLoadingBar)
    useEffect(() => {
        setShowLoadingBar(isLoading || isUpdatingVisibleCompanies);
        // if (rows.length > 0) {
        //     for (let i = 0; i < rows.length; i++) {
        //         console.log(`${rows[0].original.id} fetched data: ${fetchedData[0].id}`)
        //         if (rows[i].original.id == fetchedData[i].id) {
        //             rows[i].toggleRowSelected(fetchedData[i].visible)
        //         }
        //     }
        // }
    }, [isLoading, tableInstance, rows, isUpdatingVisibleCompanies]);
    useEffect(() => {
        if (rows.length > 0) {
            for (let i = 0; i < rows.length; i++) {
                console.log(`${rows[0].original.id} fetched data: ${fetchedData[0].id}`)
                if (rows[i].original.id == fetchedData[i].id) {
                    rows[i].toggleRowSelected(fetchedData[i].visible)
                }
            }
        }
    }, [fetchedData])

    if (isLoading) {
        return (
            <div className="fixed inset-0 mx-auto my-auto bg-indigo-600 w-fit h-fit rounded flex p-2 items-center font-medium z-50">
                <FaCircleNotch className="animate-spin text-white mr-2" />
                Processing...
            </div>
        );
    } else {
        return (
            <section className="mx-5 mt-2">
                <div className="flex flex-row place-content-between">
                    <div className="">
                        <h1 className="text-3xl font-medium">Companies</h1>
                        <p className="text-sm my-2">Add more companies here</p>
                    </div>
                    <button
                        className="dark:bg-teal-700 my-4 rounded p-2 text-base font-medium bg-teal-500 hover:bg-teal-600 dark:hover:bg-teal-600"
                        onClick={saveButtonClicked}
                    >
                        Save
                    </button>
                </div>

                <div
                    className={`overflow-hidden rounded border border-black border-opacity-50 shadow-md m-5 mx-auto`}
                >
                    <table
                        className="w-full border-collapse text-center text-sm"
                        {...getTableProps()}
                    >
                        <thead className="bg-blueAccent-600 dark:bg-blueAccent-700">
                            {headerGroups.map((headerGroup) => (
                                <tr {...headerGroup.getHeaderGroupProps()}>
                                    {headerGroup.headers.map((column) => (
                                        <th
                                            scope="col"
                                            className="px-4 py-4 font-medium"
                                            {...column.getHeaderProps()}
                                        >
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
                                    <tr
                                        className="dark:hover:bg-zinc-800 hover:bg-zinc-200"
                                        {...row.getRowProps()}
                                    >
                                        {row.cells.map((cell) => {
                                            return (
                                                <td
                                                    className="px-4 py-4 font-normal"
                                                    {...cell.getCellProps()}
                                                >
                                                    <div className="text-sm">
                                                        <div className="font-medium">
                                                            {cell.render(
                                                                "Cell"
                                                            )}
                                                        </div>
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
    }
};

export default VisibleCompaniesForm;
