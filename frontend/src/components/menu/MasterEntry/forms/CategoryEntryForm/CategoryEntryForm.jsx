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
    useGetCategoriesQuery,
    useAddCategoryMutation,
    useUpdateCategoryMutation,
    useDeleteCategoryMutation,
} from "../../../../authentication/api/categoryEntryApiSlice";
import EditCategory from "./EditCategory";
import { useOutletContext } from "react-router-dom";
import ReactModal from "react-modal";
import { Formik } from "formik";
import AddCategory from "./AddCategory";
import { addCategorySchema, editCategorySchema } from "./CategoryEntrySchema";

ReactModal.setAppElement("#root");

const CategoryEntryForm = () => {
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
    } = useGetCategoriesQuery(globalCompany);
    // console.log(fetchedData)
    const [addCategory, { isLoading: isAddingCategory }] =
        useAddCategoryMutation();
    const [updateCategory, { isLoading: isUpdatingCategory }] =
        useUpdateCategoryMutation();
    const [deleteCategory, { isLoading: isDeletingCategory }] =
        useDeleteCategoryMutation();
    const [addCategoryPopover, setAddCategoryPopover] = useState(false);
    const [showLoadingBar, setShowLoadingBar] = useOutletContext();
    const [editCategoryPopover, setEditCategoryPopover] = useState(false);
    const [updateCategoryId, setUpdateCategoryId] = useState("");
    const [msg, setMsg] = useState("");

    console.log(updateCategoryId);

    const editCategoryPopoverHandler = (category) => {
        console.log(category);
        setUpdateCategoryId(category.id);
        setEditCategoryPopover(!editCategoryPopover);
    };

    const addButtonClicked = async (values, formikBag) => {
        console.log(values);
        console.log(formikBag);

        try {
            const data = await addCategory({
                company: globalCompany.id,
                name: values.newCategory,
            }).unwrap();
            console.log(data);
        } catch (err) {
            console.log(err);
        }
        setAddCategoryPopover(!addCategoryPopover);
        4;
        formikBag.resetForm();
    };

    const updateButtonClicked = async (values, formikBag) => {
        console.log(values);
        try {
            const data = await updateCategory({
                id: updateCategoryId,
                name: values.updatedCategory,
                company: globalCompany.id,
            }).unwrap();
            console.log(data);
        } catch (err) {
            console.log(err);
        }

        formikBag.resetForm();
        editCategoryPopoverHandler({ id: "" });
    };

    const deleteButtonClicked = async (id) => {
        console.log(id);
        deleteCategory({ id: id, company: globalCompany.id });
    };

    const columnHelper = createColumnHelper();

    const columns = [
        columnHelper.accessor("id", {
            header: () => "ID",
            cell: (props) => props.renderValue(),
        }),
        columnHelper.accessor("name", {
            header: () => "Category Name",
            cell: (props) => props.renderValue(),
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
                            editCategoryPopoverHandler(props.row.original)
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
                isAddingCategory ||
                isDeletingCategory ||
                isUpdatingCategory
        );
    }, [isLoading, isAddingCategory, isDeletingCategory, isUpdatingCategory]);

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
                        <h1 className="text-3xl font-medium">Categories</h1>
                        <p className="text-sm my-2">Add more categories here</p>
                    </div>
                    <button
                        className="dark:bg-teal-700 my-auto rounded p-2 text-base font-medium bg-teal-500 hover:bg-teal-600 dark:hover:bg-teal-600 whitespace-nowrap"
                        onClick={() => setAddCategoryPopover(true)}
                    >
                        Add Category
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
                    isOpen={addCategoryPopover}
                    onRequestClose={() => setAddCategoryPopover(false)}
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <Formik
                        initialValues={{ newCategory: "" }}
                        validationSchema={addCategorySchema}
                        onSubmit={addButtonClicked}
                        component={(props) => (
                            <AddCategory
                                {...props}
                                setAddCategoryPopover={setAddCategoryPopover}
                            />
                        )}
                    />
                </ReactModal>

                <ReactModal
                    className="fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-lg h-fit bg-zinc-300 dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl"
                    isOpen={editCategoryPopover}
                    onRequestClose={() =>
                        editCategoryPopoverHandler({ id: "" })
                    }
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <Formik
                        initialValues={{ updatedCategory: "" }}
                        validationSchema={editCategorySchema}
                        onSubmit={updateButtonClicked}
                        component={(props) => (
                            <EditCategory
                                {...props}
                                editCategoryPopoverHandler={
                                    editCategoryPopoverHandler
                                }
                            />
                        )}
                    />
                </ReactModal>
            </section>
        );
    }
};

export default CategoryEntryForm;
