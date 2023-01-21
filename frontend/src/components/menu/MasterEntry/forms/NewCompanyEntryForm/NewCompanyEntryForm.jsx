import React, { useMemo } from "react";
import { useSelector } from "react-redux";
import { useState } from "react";
import { useTable } from "react-table";
import { FaRegTrashAlt, FaPen, FaCircleNotch } from "react-icons/fa";
import EditCompany from "./EditCompany";
import { useOutletContext } from "react-router-dom";
import { useEffect } from "react";

//imports after using RTK query
import {
    useGetCompaniesQuery,
    useAddCompaniesMutation,
    useDeleteCompanyMutation,
    useUpdateCompaniesMutation,
} from "../../../../authentication/api/newCompanyEntryApiSlice";
import { useUpdateCompanyDetailsMutation } from "../../../../authentication/api/companyEntryApiSlice";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const NewCompanyEntryForm = () => {
    //using RTK query
    const { data: fetchedData, isLoading, isSuccess, isError, error } = useGetCompaniesQuery();
    // console.log(fetchedData);
    // console.log(error);
    const [addCompanies, { isLoading: isAddingCompany }] = useAddCompaniesMutation();
    const [deleteCompany, { isLoading: isDeletingComapny }] = useDeleteCompanyMutation();
    const [updateCompany, { isLoading: isUpdatingCompany }] = useUpdateCompaniesMutation();
    const [addComapnyPopover, setAddCompanyPopover] = useState(false);
    const [editCompanyPopover, setEditCompanyPopover] = useState(false);
    const [showLoadingBar, setShowLoadingBar] = useOutletContext()
    

    const auth = useSelector((state) => state.auth);
    const [newCompany, setNewCompany] = useState("");
    const [updatedCompany, setUpdatedCompany] = useState({
        id: "",
        name: "",
    });

    const addComapnyPopoverHandler = () => {
        setAddCompanyPopover(!addComapnyPopover);
    };

    const editCompanyPopoverHandler = (company) => {
        console.log(company);
        setUpdatedCompany((prevState) => {
            return { ...prevState, id: company.id };
        });
        setEditCompanyPopover(!editCompanyPopover);
    };

    const newCompanyChangeHandler = (event) => {
        setNewCompany(event.target.value);
    };
    console.log(updatedCompany)
    const updateCompanyChangeHandler = (event) => {
        setUpdatedCompany((prevState) => {
            return { ...prevState, name: event.target.value };
        });
    };

    // console.log(newCompany);
    // console.log(isAddingCompany);
    const addButtonClicked = async () => {
        setAddCompanyPopover(!addComapnyPopover);
        addCompanies({
            user: auth.account.id,
            name: newCompany,
        });
        console.log(isAddingCompany);
        setNewCompany("");
    };

    const updateButtonClicked = async () => {
        console.log(updatedCompany);
        updateCompany({
            id: updatedCompany.id,
            user: auth.account.id,
            name: updatedCompany.name,
        });
        editCompanyPopoverHandler({id: "", name: ""});
    };

    const deleteButtonClicked = async (id) => {
        console.log(id);
        deleteCompany({ id });
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

    const data = useMemo(() => (fetchedData ? [...fetchedData] : []), [fetchedData]);

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
                            onClick={() => editCompanyPopoverHandler(row.values)}
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

    console.log(showLoadingBar)
    useEffect(() => {
        setShowLoadingBar(isAddingCompany || isDeletingComapny || isUpdatingCompany)
    }, [isAddingCompany, isDeletingComapny, isUpdatingCompany])

    if (isLoading) {
        return (
            <div className="fixed inset-0 mx-auto my-auto bg-indigo-600 w-fit h-fit rounded flex p-2 items-center font-medium z-50">
                <FaCircleNotch className="animate-spin text-white mr-2" />
                Processing...
            </div>
        );
    } else {
        return (
            <section className="relative">
                <div className="flex flex-row place-content-between mx-5 mt-2">
                    <div className="">
                        <h1 className="text-3xl font-medium">Companies</h1>
                        <p className="text-sm my-2">Add more companies here</p>
                    </div>
                    <button
                        className="dark:bg-teal-700 m-4 rounded p-2 text-base font-medium bg-teal-500 hover:bg-teal-600 dark:hover:bg-teal-600"
                        onClick={addComapnyPopoverHandler}
                    >
                        Add Company
                    </button>
                </div>

                {/* Popover */}
                <div
                    className={classNames(
                        addComapnyPopover == false ? "hidden" : "",
                        "fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-lg h-fit bg-zinc-300  dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl"
                    )}
                >
                    <h1 className="font-medium text-2xl mb-2">Add New Company</h1>

                    <form action="" className="flex flex-col gap-2 justify-center">
                        <label
                            htmlFor="comapny-name"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Company Name
                        </label>
                        <div className="relative">
                            <input
                                className="rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2 border-gray-800 border-opacity-25 dark:border-opacity-25 dark:border-slate-100 p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                type="text"
                                id="comapny-name"
                                name="comapny-name"
                                value={newCompany}
                                placeholder=" "
                                onChange={newCompanyChangeHandler}
                            />
                        </div>
                    </form>
                    <section className="flex flex-row gap-4 mt-4 mb-2">
                        <button
                            className="bg-teal-500 hover:bg-teal-600 dark:bg-teal-700 rounded w-20 p-2 text-base font-medium dark:hover:bg-teal-600"
                            onClick={addButtonClicked}
                        >
                            Add
                        </button>
                        <button
                            className="bg-zinc-400 hover:bg-zinc-500 dark:bg-zinc-600 rounded w-20 p-2 text-base font-medium dark:hover:bg-zinc-700"
                            onClick={addComapnyPopoverHandler}
                        >
                            Cancel
                        </button>
                    </section>
                </div>
                {/* Popover End */}

                <div className={`overflow-hidden rounded border border-black border-opacity-50 shadow-md m-5`}>
                    <table className="w-full border-collapse text-center text-sm" {...getTableProps()}>
                        <thead className="bg-blueAccent-600 dark:bg-blueAccent-700">
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
                {editCompanyPopover ? (
                    <EditCompany
                        editCompanyPopoverHandler={editCompanyPopoverHandler}
                        updateCompanyChangeHandler={updateCompanyChangeHandler}
                        updateButtonClicked={updateButtonClicked}
                    />
                ) : (
                    ""
                )}
                <div
                    className={classNames(
                        isAddingCompany || isDeletingComapny || isUpdatingCompany ? "" : "hidden",
                        "bg-indigo-600 w-fit h-fit rounded flex p-2 items-center font-medium z-50 mx-auto"
                    )}
                >
                    <FaCircleNotch className="animate-spin text-white mr-2" />
                    Processing...
                </div>
            </section>
        );
    }
};

export default NewCompanyEntryForm;
