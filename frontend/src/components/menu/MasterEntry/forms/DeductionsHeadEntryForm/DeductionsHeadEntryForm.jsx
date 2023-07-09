import React, { useEffect, useMemo, useState } from "react";
import {
    createColumnHelper,
    flexRender,
    getCoreRowModel,
    useReactTable,
    getSortedRowModel,
} from "@tanstack/react-table";
import { FaRegTrashAlt, FaPen, FaAngleUp, FaAngleDown } from "react-icons/fa";
import { useSelector } from "react-redux";
import {
    useGetDeductionsHeadsQuery,
    useAddDeductionsHeadMutation,
    useUpdateDeductionsHeadMutation,
    useDeleteDeductionsHeadMutation,
} from "../../../../authentication/api/deductionsHeadEntryApiSlice";
import EditDeductionsHead from "./EditDeductionsHead";
import { useOutletContext } from "react-router-dom";
import ReactModal from "react-modal";
import { Formik } from "formik";
import AddDeductionsHead from "./AddDeductionsHead";
import { DeductionsHeadSchema } from "./DeductionsHeadEntrySchema";

ReactModal.setAppElement("#root");

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const DeductionsHeadEntryForm = () => {
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
    } = useGetDeductionsHeadsQuery(globalCompany);
    // console.log(fetchedData)
    const [addDeductionsHead, { isLoading: isAddingDeductionsHead }] =
        useAddDeductionsHeadMutation();
    const [updateDeductionsHead, { isLoading: isUpdatingDeductionsHead }] =
        useUpdateDeductionsHeadMutation();
    const [deleteDeductionsHead, { isLoading: isDeletingDeductionsHead }] =
        useDeleteDeductionsHeadMutation();
    const [addDeductionsHeadPopover, setAddDeductionsHeadPopover] =
        useState(false);
    const [showLoadingBar, setShowLoadingBar] = useOutletContext();
    const [editDeductionsHeadPopover, setEditDeductionsHeadPopover] =
        useState(false);
    const [updateDeductionsHeadId, setUpdateDeductionsHeadId] = useState("");
    // const [msg, setMsg] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    console.log(updateDeductionsHeadId);

    const editDeductionsHeadPopoverHandler = (deductionsHead) => {
        console.log(deductionsHead);
        setUpdateDeductionsHeadId(deductionsHead.id);
        setEditDeductionsHeadPopover(!editDeductionsHeadPopover);
    };

    const addButtonClicked = async (values, formikBag) => {
        console.log(values);
        console.log(formikBag);

        try {
            const data = await addDeductionsHead({
                company: globalCompany.id,
                name: values.deductionsHeadName,
            }).unwrap();
            console.log(data);
            setErrorMessage("");
            setAddDeductionsHeadPopover(!addDeductionsHeadPopover);
            formikBag.resetForm();
        } catch (err) {
            console.log(err);
            if (err.status === 400) {
                setErrorMessage(
                    "Deductions Head with this name already exists"
                );
            } else {
                console.log(err);
            }
        }
    };

    const updateButtonClicked = async (values, formikBag) => {
        console.log(values);
        try {
            const data = await updateDeductionsHead({
                id: updateDeductionsHeadId,
                name: values.deductionsHeadName,
                company: globalCompany.id,
            }).unwrap();
            console.log(data);
            setErrorMessage("");
            formikBag.resetForm();
            editDeductionsHeadPopoverHandler({ id: "" });
        } catch (err) {
            console.log(err);
            if (err.status === 400) {
                setErrorMessage(
                    "Deductions Head with this name already exists"
                );
            } else {
                console.log(err);
            }
        }
    };

    const deleteButtonClicked = async (id) => {
        console.log(id);
        deleteDeductionsHead({ id: id, company: globalCompany.id });
    };

    const columnHelper = createColumnHelper();
    console.log(fetchedData)

    const columns = [
        columnHelper.accessor("id", {
            header: () => "ID",
            cell: (props) => props.renderValue(),
            //   footer: props => props.column.id,
        }),
        columnHelper.accessor("name", {
            header: () => "Deductions Head Name",
            cell: (props) => props.renderValue(),
            //   footer: info => info.column.id,
        }),
        columnHelper.display({
            id: "actions",
            header: () => "Actions",
            cell: (props) => (
                <div className="flex justify-center gap-4">
                    {props.row.original.mandatoryDeduction ? (
                        ""
                    ) : (
                        <>
                            <div
                                className="p-1.5 dark:bg-redAccent-700 rounded bg-redAccent-500 dark:hover:bg-redAccent-500 hover:bg-redAccent-700"
                                onClick={() =>
                                    deleteButtonClicked(props.row.original.id)
                                }
                            >
                                <FaRegTrashAlt className="h-4" />
                            </div>
                            <div
                                className="p-1.5 dark:bg-teal-700 rounded bg-teal-600 dark:hover:bg-teal-600 hover:bg-teal-700"
                                onClick={() =>
                                    editDeductionsHeadPopoverHandler(
                                        props.row.original
                                    )
                                }
                            >
                                <FaPen className="h-4" />
                            </div>
                        </>
                    )}
                </div>
            ),
        }),
    ];

    const data = useMemo(
        () => (fetchedData ? [...fetchedData] : []),
        [fetchedData]
    );

    const table = useReactTable({
        data,
        columns,
        initialState: {
            sorting: [{ id: "name", desc: false }],
        },
        getCoreRowModel: getCoreRowModel(),
        getSortedRowModel: getSortedRowModel(),
        enableSortingRemoval: false,
    });

    useEffect(() => {
        setShowLoadingBar(
            isLoading ||
                isAddingDeductionsHead ||
                isDeletingDeductionsHead ||
                isUpdatingDeductionsHead
        );
    }, [
        isLoading,
        isAddingDeductionsHead,
        isDeletingDeductionsHead,
        isUpdatingDeductionsHead,
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
                        <h1 className="text-3xl font-medium">
                            Deductions Head
                        </h1>
                        <p className="text-sm my-2">
                            Add more Deductions head here
                        </p>
                    </div>
                    <button
                        className="dark:bg-teal-700 my-auto rounded p-2 text-base font-medium bg-teal-500 hover:bg-teal-600 dark:hover:bg-teal-600 whitespace-nowrap"
                        onClick={() => setAddDeductionsHeadPopover(true)}
                    >
                        Add Deductions Head
                    </button>
                </div>
                <div className="overflow-hidden rounded border border-black border-opacity-50 shadow-md m-5 max-w-5xl mx-auto">
                    <table className="w-full border-collapse text-center text-sm">
                        <thead className="bg-blueAccent-600 dark:bg-blueAccent-700">
                            {table.getHeaderGroups().map((headerGroup) => (
                                <tr key={headerGroup.id}>
                                    {headerGroup.headers.map((header) => (
                                        <th
                                            key={header.id}
                                            scope="col"
                                            className="px-4 py-4 font-medium"
                                        >
                                            {header.isPlaceholder ? null : (
                                                <div className="">
                                                    <div
                                                        {...{
                                                            className:
                                                                header.column.getCanSort()
                                                                    ? "cursor-pointer select-none flex flex-row justify-center"
                                                                    : "",
                                                            onClick:
                                                                header.column.getToggleSortingHandler(),
                                                        }}
                                                    >
                                                        {flexRender(
                                                            header.column
                                                                .columnDef
                                                                .header,
                                                            header.getContext()
                                                        )}

                                                        {console.log(
                                                            header.column.getIsSorted()
                                                        )}
                                                        {header.column.getCanSort() ? (
                                                            <div className="relative pl-2">
                                                                <FaAngleUp
                                                                    className={classNames(
                                                                        header.column.getIsSorted() ==
                                                                            "asc"
                                                                            ? "text-teal-700"
                                                                            : "",
                                                                        "absolute text-lg -translate-y-2"
                                                                    )}
                                                                />
                                                                <FaAngleDown
                                                                    className={classNames(
                                                                        header.column.getIsSorted() ==
                                                                            "desc"
                                                                            ? "text-teal-700"
                                                                            : "",
                                                                        "absolute text-lg translate-y-2"
                                                                    )}
                                                                />
                                                            </div>
                                                        ) : (
                                                            ""
                                                        )}
                                                    </div>
                                                </div>
                                            )}
                                        </th>
                                    ))}
                                </tr>
                            ))}
                        </thead>
                        <tbody className="divide-y divide-black divide-opacity-50 border-t border-black border-opacity-50">
                            {table.getRowModel().rows.map((row) => (
                                <tr
                                    className="dark:hover:bg-zinc-800 hover:bg-zinc-200"
                                    key={row.id}
                                >
                                    {row.getVisibleCells().map((cell) => (
                                        <td
                                            className="px-4 py-4 font-normal"
                                            key={cell.id}
                                        >
                                            <div className="text-sm">
                                                <div className="font-medium">
                                                    {flexRender(
                                                        cell.column.columnDef
                                                            .cell,
                                                        cell.getContext()
                                                    )}
                                                </div>
                                            </div>
                                        </td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <ReactModal
                    className="fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-lg h-fit bg-zinc-300 dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl"
                    isOpen={addDeductionsHeadPopover}
                    onRequestClose={() => setAddDeductionsHeadPopover(false)}
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <Formik
                        initialValues={{ deductionsHeadName: "" }}
                        validationSchema={DeductionsHeadSchema}
                        onSubmit={addButtonClicked}
                        component={(props) => (
                            <AddDeductionsHead
                                {...props}
                                errorMessage={errorMessage}
                                setErrorMessage={setErrorMessage}
                                setAddDeductionsHeadPopover={
                                    setAddDeductionsHeadPopover
                                }
                            />
                        )}
                    />
                </ReactModal>

                <ReactModal
                    className="fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-lg h-fit bg-zinc-300 dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl"
                    isOpen={editDeductionsHeadPopover}
                    onRequestClose={() =>
                        editDeductionsHeadPopoverHandler({ id: "" })
                    }
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <Formik
                        initialValues={{
                            deductionsHeadName: updateDeductionsHeadId
                                ? fetchedData.find(
                                      (deductionsHead) =>
                                          deductionsHead.id ===
                                          updateDeductionsHeadId
                                  )?.name
                                : "",
                        }}
                        validationSchema={DeductionsHeadSchema}
                        onSubmit={updateButtonClicked}
                        component={(props) => (
                            <EditDeductionsHead
                                {...props}
                                errorMessage={errorMessage}
                                setErrorMessage={setErrorMessage}
                                editDeductionsHeadPopoverHandler={
                                    editDeductionsHeadPopoverHandler
                                }
                            />
                        )}
                    />
                </ReactModal>
            </section>
        );
    }
};

export default DeductionsHeadEntryForm;
