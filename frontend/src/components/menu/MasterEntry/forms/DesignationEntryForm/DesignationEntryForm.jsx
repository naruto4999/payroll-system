import React, { useEffect, useMemo, useState } from "react";
import {
    createColumnHelper,
    flexRender,
    getCoreRowModel,
    useReactTable,
} from "@tanstack/react-table";
import { FaRegTrashAlt, FaPen } from "react-icons/fa";
import { useSelector } from "react-redux";
import {
    useGetDesignationsQuery,
    useAddDesignationMutation,
    useUpdateDesignationMutation,
    useDeleteDesignationMutation,
} from "../../../../authentication/api/designationEntryApiSlice";
import AddDesignation from "./AddDesignation";
import EditDesignation from "./EditDesignation";
import { useOutletContext } from "react-router-dom";
import ReactModal from "react-modal";
import {
    addDesignationSchema,
    editDesignationSchema,
} from "./DesignationEntrySchema";
import { Formik } from "formik";

ReactModal.setAppElement("#root");

const DesignationEntryForm = () => {
    const globalCompany = useSelector((state) => state.globalCompany);

    const {
        data: fetchedData,
        isLoading,
        isSuccess,
        isError,
        error,
        isFetching,
        refetch,
    } = useGetDesignationsQuery(globalCompany);
    // console.log(fetchedData)
    const [addDesignation, { isLoading: isAddingDesignation }] =
        useAddDesignationMutation();
    const [updateDesignation, { isLoading: isUpdatingDesignation }] =
        useUpdateDesignationMutation();
    const [deleteDesignation, { isLoading: isDeletingDesignation }] =
        useDeleteDesignationMutation();
    const [addDesignationPopover, setAddDesignationPopover] = useState(false);
    const [newDesignation, setNewDesignation] = useState("");
    const [showLoadingBar, setShowLoadingBar] = useOutletContext();
    const [editDesignationPopover, setEditDesignationPopover] = useState(false);
    const [updatedDesignationId, setUpdatedDesignationId] = useState("");

    console.log(isFetching);

    const editDesignationPopoverHandler = (designation) => {
        console.log(designation);
        setUpdatedDesignationId(designation.id);
        setEditDesignationPopover(!editDesignationPopover);
    };

    const addButtonClicked = async (values, formikBag) => {
        setAddDesignationPopover(!addDesignationPopover);
        addDesignation({
            company: globalCompany.id,
            name: values.newDesignation,
        });
        formikBag.resetForm();
    };

    const updateButtonClicked = async (values, formikBag) => {
        console.log(values);
        updateDesignation({
            id: updatedDesignationId,
            name: values.updatedDesignation,
            company: globalCompany.id,
        });
        editDesignationPopoverHandler({ id: "" });
    };

    const deleteButtonClicked = async (id) => {
        console.log(id);
        deleteDesignation({ id: id, company: globalCompany.id });
    };
    const columnHelper = createColumnHelper();

    const columns = [
        columnHelper.accessor("id", {
            header: () => "ID",
            cell: (props) => props.renderValue(),
            //   footer: props => props.column.id,
        }),
        columnHelper.accessor("name", {
            header: () => "Designation Name",
            cell: (props) => props.renderValue(),
            //   footer: info => info.column.id,
        }),
        columnHelper.display({
            id: "actions",
            header: () => "Actions",
            cell: (props) => (
                <div className="flex justify-center gap-4">
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
                            editDesignationPopoverHandler(props.row.original)
                        }
                    >
                        <FaPen className="h-4" />
                    </div>
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
        getCoreRowModel: getCoreRowModel(),
    });

    useEffect(() => {
        setShowLoadingBar(
            isLoading ||
                isAddingDesignation ||
                isDeletingDesignation ||
                isUpdatingDesignation
        );
    }, [
        isLoading,
        isAddingDesignation,
        isDeletingDesignation,
        isUpdatingDesignation,
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
                        <h1 className="text-3xl font-medium">Designations</h1>
                        <p className="text-sm my-2">
                            Add more Designations here
                        </p>
                    </div>
                    <button
                        className="dark:bg-teal-700 my-auto rounded p-2 text-base font-medium bg-teal-500 hover:bg-teal-600 dark:hover:bg-teal-600 whitespace-nowrap"
                        onClick={() => setAddDesignationPopover(true)}
                    >
                        Add Designation
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
                                            {header.isPlaceholder
                                                ? null
                                                : flexRender(
                                                      header.column.columnDef
                                                          .header,
                                                      header.getContext()
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
                    isOpen={addDesignationPopover}
                    onRequestClose={() => setAddDesignationPopover(false)}
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <Formik
                        initialValues={{ newDesignation: "" }}
                        validationSchema={addDesignationSchema}
                        onSubmit={addButtonClicked}
                        component={(props) => (
                            <AddDesignation
                                {...props}
                                setAddDesignationPopover={
                                    setAddDesignationPopover
                                }
                            />
                        )}
                    />
                </ReactModal>

                <ReactModal
                    className="fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-lg h-fit bg-zinc-300 dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl"
                    isOpen={editDesignationPopover}
                    onRequestClose={() =>
                        editDesignationPopoverHandler({ id: "" })
                    }
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <Formik
                        initialValues={{ updatedDesignation: "" }}
                        validationSchema={editDesignationSchema}
                        onSubmit={updateButtonClicked}
                        component={(props) => (
                            <EditDesignation
                                {...props}
                                editDesignationPopoverHandler={
                                    editDesignationPopoverHandler
                                }
                            />
                        )}
                    />
                </ReactModal>
            </section>
        );
    }
};

export default DesignationEntryForm;
