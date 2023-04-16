import React, { useEffect, useMemo, useState } from "react";
import { useTable } from "react-table";
import { FaRegTrashAlt, FaPen } from "react-icons/fa";
import { useSelector } from "react-redux";
import {
    useGetDepartmentsQuery,
    useAddDepartmentMutation,
    useDeleteDepartmentMutation,
    useUpdateDepartmentMutation,
} from "../../../../authentication/api/departmentEntryApiSlice";
import EditDepartment from "./EditDepartment";
import { useOutletContext } from "react-router-dom";
import ReactModal from "react-modal";
import { Formik, Field, Form } from "formik";
import AddDepartment from "./AddDepartment";
import {
    addDepartmentSchema,
    editDepartmentSchema,
} from "./DepartmentEntrySchema";

ReactModal.setAppElement("#root");

const DepartmentEntryForm = () => {
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
    } = useGetDepartmentsQuery(globalCompany);
    // console.log(fetchedData)
    const [addDepartment, { isLoading: isAddingDepartment }] =
        useAddDepartmentMutation();
    const [updateDepartment, { isLoading: isUpdatingDepartment }] =
        useUpdateDepartmentMutation();
    const [deleteDepartment, { isLoading: isDeletingDepartment }] =
        useDeleteDepartmentMutation();
    const [addDepartmentPopover, setAddDepartmentPopover] = useState(false);
    const [showLoadingBar, setShowLoadingBar] = useOutletContext();
    const [editDepartmentPopover, setEditDepartmentPopover] = useState(false);
    const [updateDepartmentId, setUpdateDepartmentId] = useState("");

    console.log(updateDepartmentId);

    const editDepartmentPopoverHandler = (department) => {
        console.log(department);
        setUpdateDepartmentId(department.id);
        setEditDepartmentPopover(!editDepartmentPopover);
    };

    const updateDepartmentIdChangeHandler = (event) => {
        setUpdateDepartmentId((prevState) => {
            return { ...prevState, name: event.target.value };
        });
    };

    const addButtonClicked = async (values, formikBag) => {
        console.log(values);
        console.log(formikBag);
        formikBag.resetForm();
        setAddDepartmentPopover(!addDepartmentPopover);
        addDepartment({
            company: globalCompany.id,
            name: values.newDepartment,
        });
        console.log(isAddingDepartment);
        // setNewDepartment("");
    };

    const updateButtonClicked = async (values, formikBag) => {
        console.log(values);
        updateDepartment({
            id: updateDepartmentId,
            name: values.updatedDepartment,
            company: globalCompany.id,
        });
        editDepartmentPopoverHandler({ id: "" });
    };

    const deleteButtonClicked = async (id) => {
        console.log(id);
        deleteDepartment({ id: id, company: globalCompany.id });
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

    const data = useMemo(
        () => (fetchedData ? [...fetchedData] : []),
        [fetchedData]
    );
    // console.log(newDepartment);
    // console.log(fullname)
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
                                editDepartmentPopoverHandler(row.values)
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
                isAddingDepartment ||
                isDeletingDepartment ||
                isUpdatingDepartment
        );
    }, [
        isLoading,
        isAddingDepartment,
        isDeletingDepartment,
        isUpdatingDepartment,
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
                        <h1 className="text-3xl font-medium">Departments</h1>
                        <p className="text-sm my-2">
                            Add more departments here
                        </p>
                    </div>
                    <button
                        className="dark:bg-teal-700 my-auto rounded p-2 text-base font-medium bg-teal-500 hover:bg-teal-600 dark:hover:bg-teal-600 whitespace-nowrap"
                        onClick={() => setAddDepartmentPopover(true)}
                    >
                        Add Department
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
                    isOpen={addDepartmentPopover}
                    onRequestClose={() => setAddDepartmentPopover(false)}
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <Formik
                        initialValues={{ newDepartment: "" }}
                        validationSchema={addDepartmentSchema}
                        onSubmit={addButtonClicked}
                        component={(props) => (
                            <AddDepartment
                                {...props}
                                setAddDepartmentPopover={
                                    setAddDepartmentPopover
                                }
                            />
                        )}
                    />
                </ReactModal>
                {/* <ReactModal
                    className="fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-lg h-fit bg-zinc-300 dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl"
                    isOpen={editDepartmentPopover}
                    onRequestClose={() => editDepartmentPopoverHandler({id: "", name: ""})}
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <EditDepartment
                        editDepartmentPopoverHandler={editDepartmentPopoverHandler}
                        updateDepartmentIdChangeHandler={updateDepartmentIdChangeHandler}
                        updateButtonClicked={updateButtonClicked}
                    />
                </ReactModal> */}
                <ReactModal
                    className="fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-lg h-fit bg-zinc-300 dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl"
                    isOpen={editDepartmentPopover}
                    onRequestClose={() =>
                        editDepartmentPopoverHandler({ id: "" })
                    }
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <Formik
                        initialValues={{ updatedDepartment: "" }}
                        validationSchema={editDepartmentSchema}
                        onSubmit={updateButtonClicked}
                        component={(props) => (
                            <EditDepartment
                                {...props}
                                editDepartmentPopoverHandler={
                                    editDepartmentPopoverHandler
                                }
                            />
                        )}
                    />
                </ReactModal>
            </section>
        );
    }
};

export default DepartmentEntryForm;
