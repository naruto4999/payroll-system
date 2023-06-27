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
    useGetEarningsHeadsQuery,
    useAddEarningsHeadMutation,
    useUpdateEarningsHeadMutation,
    useDeleteEarningsHeadMutation,
} from "../../../../authentication/api/earningsHeadEntryApiSlice";
import EditEarningsHead from "./EditEarningsHead";
import { useOutletContext } from "react-router-dom";
import ReactModal from "react-modal";
import { Formik } from "formik";
import AddEarningsHead from "./AddEarningsHead";
import { EarningsHeadSchema } from "./EarningsHeadEntrySchema";

ReactModal.setAppElement("#root");

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const EarningsHeadEntry = () => {
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
    } = useGetEarningsHeadsQuery(globalCompany);
    // console.log(fetchedData)
    const [addEarningsHead, { isLoading: isAddingEarningsHead }] =
        useAddEarningsHeadMutation();
    const [updateEarningsHead, { isLoading: isUpdatingEarningsHead }] =
        useUpdateEarningsHeadMutation();
    const [deleteEarningsHead, { isLoading: isDeletingEarningsHead }] =
        useDeleteEarningsHeadMutation();
    const [addEarningsHeadPopover, setAddEarningsHeadPopover] = useState(false);
    const [showLoadingBar, setShowLoadingBar] = useOutletContext();
    const [editEarningsHeadPopover, setEditEarningsHeadPopover] =
        useState(false);
    const [updateEarningsHeadId, setUpdateEarningsHeadId] = useState("");
    // const [msg, setMsg] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    console.log(updateEarningsHeadId);

    const editEarningsHeadPopoverHandler = (earningsHead) => {
        console.log(earningsHead);
        setUpdateEarningsHeadId(earningsHead.id);
        setEditEarningsHeadPopover(!editEarningsHeadPopover);
    };

    const addButtonClicked = async (values, formikBag) => {
        console.log(values);
        console.log(formikBag);

        try {
            const data = await addEarningsHead({
                company: globalCompany.id,
                name: values.earningsHeadName,
            }).unwrap();
            console.log(data);
            setErrorMessage("");
            setAddEarningsHeadPopover(!addEarningsHeadPopover);
            formikBag.resetForm();
        } catch (err) {
            console.log(err);
            if (err.status === 400) {
                setErrorMessage("Earnings Head with this name already exists");
            } else {
                console.log(err);
            }
        }
    };

    const updateButtonClicked = async (values, formikBag) => {
        console.log(values);
        try {
            const data = await updateEarningsHead({
                id: updateEarningsHeadId,
                name: values.earningsHeadName,
                company: globalCompany.id,
            }).unwrap();
            console.log(data);
            setErrorMessage("");
            formikBag.resetForm();
            editEarningsHeadPopoverHandler({ id: "" });
        } catch (err) {
            console.log(err);
            if (err.status === 400) {
                setErrorMessage("Earnings Head with this name already exists");
            } else {
                console.log(err);
            }
        }
    };

    const deleteButtonClicked = async (id) => {
        console.log(id);
        deleteEarningsHead({ id: id, company: globalCompany.id });
    };

    const columnHelper = createColumnHelper();

    const columns = [
        columnHelper.accessor("id", {
            header: () => "ID",
            cell: (props) => props.renderValue(),
            //   footer: props => props.column.id,
        }),
        columnHelper.accessor("name", {
            header: () => "Earnings Head Name",
            cell: (props) => props.renderValue(),
            //   footer: info => info.column.id,
        }),
        columnHelper.display({
            id: "actions",
            header: () => "Actions",
            cell: (props) => (
                <div className="flex justify-center gap-4">
                    {props.row.original.mandatory_earning ? (
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
                                    editEarningsHeadPopoverHandler(
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
                isAddingEarningsHead ||
                isDeletingEarningsHead ||
                isUpdatingEarningsHead
        );
    }, [
        isLoading,
        isAddingEarningsHead,
        isDeletingEarningsHead,
        isUpdatingEarningsHead,
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
                        <h1 className="text-3xl font-medium">Earnings Head</h1>
                        <p className="text-sm my-2">
                            Add more earnings head here
                        </p>
                    </div>
                    <button
                        className="dark:bg-teal-700 my-auto rounded p-2 text-base font-medium bg-teal-500 hover:bg-teal-600 dark:hover:bg-teal-600 whitespace-nowrap"
                        onClick={() => setAddEarningsHeadPopover(true)}
                    >
                        Add Earnings Head
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
                    isOpen={addEarningsHeadPopover}
                    onRequestClose={() => setAddEarningsHeadPopover(false)}
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <Formik
                        initialValues={{ earningsHeadName: "" }}
                        validationSchema={EarningsHeadSchema}
                        onSubmit={addButtonClicked}
                        component={(props) => (
                            <AddEarningsHead
                                {...props}
                                errorMessage={errorMessage}
                                setErrorMessage={setErrorMessage}
                                setAddEarningsHeadPopover={
                                    setAddEarningsHeadPopover
                                }
                            />
                        )}
                    />
                </ReactModal>

                <ReactModal
                    className="fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-lg h-fit bg-zinc-300 dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl"
                    isOpen={editEarningsHeadPopover}
                    onRequestClose={() =>
                        editEarningsHeadPopoverHandler({ id: "" })
                    }
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <Formik
                        initialValues={{
                            earningsHeadName: updateEarningsHeadId
                                ? fetchedData.find(
                                      (earningsHead) =>
                                          earningsHead.id ===
                                          updateEarningsHeadId
                                  )?.name
                                : "",
                        }}
                        validationSchema={EarningsHeadSchema}
                        onSubmit={updateButtonClicked}
                        component={(props) => (
                            <EditEarningsHead
                                {...props}
                                errorMessage={errorMessage}
                                setErrorMessage={setErrorMessage}
                                editEarningsHeadPopoverHandler={
                                    editEarningsHeadPopoverHandler
                                }
                            />
                        )}
                    />
                </ReactModal>
            </section>
        );
    }
};

export default EarningsHeadEntry;
