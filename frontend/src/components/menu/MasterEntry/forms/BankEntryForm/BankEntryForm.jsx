import React, { useEffect, useMemo, useState } from "react";
import { useTable } from "react-table";
import { FaRegTrashAlt, FaPen } from "react-icons/fa";
import { useSelector } from "react-redux";
import {
    useGetBanksQuery,
    useAddBankMutation,
    useUpdateBankMutation,
    useDeleteBankMutation
} from "../../../../authentication/api/bankEntryApiSlice";
import EditBank from "./EditBank";
import { useOutletContext } from "react-router-dom";
import ReactModal from "react-modal";
import { Formik } from "formik";
import AddBank from "./AddBank";
import {
    addBankSchema,
    editBankSchema,
} from "./BankEntrySchema";

ReactModal.setAppElement("#root");

const BankEntryForm = () => {
    const globalCompany = useSelector((state) => state.globalCompany);

    console.log(globalCompany);
    const {
        data: fetchedData,
        isLoading,
        isSuccess,
        isError,
        error,
        isFetching,
        refetch,
    } = useGetBanksQuery(globalCompany);
    // console.log(fetchedData)
    const [addBank, { isLoading: isAddingBank }] =
        useAddBankMutation();
    const [updateBank, { isLoading: isUpdatingBank }] =
        useUpdateBankMutation();
    const [deleteBank, { isLoading: isDeletingBank }] =
        useDeleteBankMutation();
    const [addBankPopover, setAddBankPopover] = useState(false);
    const [showLoadingBar, setShowLoadingBar] = useOutletContext();
    const [editBankPopover, setEditBankPopover] = useState(false);
    const [updateBankId, setUpdateBankId] = useState("");
    const [msg, setMsg] = useState("");

    console.log(updateBankId);

    const editBankPopoverHandler = (bank) => {
        console.log(bank);
        setUpdateBankId(bank.id);
        setEditBankPopover(!editBankPopover);
    };

    const addButtonClicked = async (values, formikBag) => {
        console.log(values);
        console.log(formikBag);
        
        try {
            const data = await addBank({
                company: globalCompany.id,
                name: values.newBank,
            }).unwrap();
            console.log(data);
        } catch (err) {
            console.log(err);
        }
        setAddBankPopover(!addBankPopover);4
        formikBag.resetForm();
    };

    const updateButtonClicked = async (values, formikBag) => {
        console.log(values);
        try {
            const data = await updateBank({
                id: updateBankId,
                name: values.updatedBank,
                company: globalCompany.id,
            }).unwrap();
            console.log(data);
        } catch (err) {
            console.log(err);
        }

        formikBag.resetForm();
        editBankPopoverHandler({ id: "" });
    };

    const deleteButtonClicked = async (id) => {
        console.log(id);
        deleteBank({ id: id, company: globalCompany.id });
    };
    const columns = useMemo(
        () => [
            {
                Header: "ID",
                accessor: "id",
            },
            {
                Header: "Bank Name",
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
                            onClick={() =>
                                editBankPopoverHandler(row.values)
                            }
                        >
                            <FaPen className="h-4" />
                        </div>
                    </div>
                ),
            },
        ]);
    };

    const tableInstance = useTable({ columns, data }, tableHooks);
    const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
        tableInstance;

    useEffect(() => {
        setShowLoadingBar(
            isLoading ||
                isAddingBank ||
                isDeletingBank ||
                isUpdatingBank
        );
    }, [
        isLoading,
        isAddingBank,
        isDeletingBank,
        isUpdatingBank,
    ]);

    if (globalCompany.id == null) {
        return (
            <section className="flex flex-col items-center">
                <h4 className="mt-10 text-x text-redAccent-500 dark:text-redAccent-600 font-bold">
                    Please Select a Company First
                </h4>
            </section>
        );
    }
    if (isLoading) {
        return <div></div>;
    } else {
        return (
            <section className="mx-5 mt-2">
                <div className="flex flex-row place-content-between flex-wrap">
                    <div className="mr-4">
                        <h1 className="text-3xl font-medium">Banks</h1>
                        <p className="text-sm my-2">
                            Add more banks here
                        </p>
                    </div>
                    <button
                        className="dark:bg-teal-700 my-auto rounded p-2 text-base font-medium bg-teal-500 hover:bg-teal-600 dark:hover:bg-teal-600 whitespace-nowrap"
                        onClick={() => setAddBankPopover(true)}
                    >
                        Add Bank
                    </button>
                </div>
                <div className="overflow-hidden rounded border border-black border-opacity-50 shadow-md m-5 max-w-5xl mx-auto">
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

                <ReactModal
                    className="fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-lg h-fit bg-zinc-300 dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl"
                    isOpen={addBankPopover}
                    onRequestClose={() => setAddBankPopover(false)}
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <Formik
                        initialValues={{ newBank: "" }}
                        validationSchema={addBankSchema}
                        onSubmit={addButtonClicked}
                        component={(props) => (
                            <AddBank
                                {...props}
                                setAddBankPopover={
                                    setAddBankPopover
                                }
                            />
                        )}
                    />
                </ReactModal>

                <ReactModal
                    className="fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-lg h-fit bg-zinc-300 dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl"
                    isOpen={editBankPopover}
                    onRequestClose={() =>
                        editBankPopoverHandler({ id: "" })
                    }
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <Formik
                        initialValues={{ updatedBank: "" }}
                        validationSchema={editBankSchema}
                        onSubmit={updateButtonClicked}
                        component={(props) => (
                            <EditBank
                                {...props}
                                editBankPopoverHandler={
                                    editBankPopoverHandler
                                }
                            />
                        )}
                    />
                </ReactModal>
            </section>
        );
    }
};

export default BankEntryForm;
