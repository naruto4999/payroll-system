import React, { useMemo } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useState } from "react";
import {
    createColumnHelper,
    flexRender,
    getCoreRowModel,
    useReactTable,
    getSortedRowModel,
} from "@tanstack/react-table";
import {
    FaRegTrashAlt,
    FaPen,
    FaCircleNotch,
    FaCheck,
    FaWindowMinimize,
    FaAngleUp,
    FaAngleDown,
} from "react-icons/fa";
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
                {indeterminate ? (
                    <FaWindowMinimize className="absolute text-teal-600 dark:text-teal-500 left-[3px] bottom-[7px]" />
                ) : (
                    <FaCheck className="absolute text-teal-600 dark:text-teal-500 left-[3px] bottom-[3px] peer-[&:not(:checked)]:hidden" />
                )}
                {/* {console.log(rest)} */}
                {/* {console.log(indeterminate)} */}
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
        const selectedRows = table.getSelectedRowModel().flatRows;
        console.log(selectedRows);
        for (let i = 0; i < selectedRows.length; i++) {
            const original = selectedRows[i].original;
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
    const columnHelper = createColumnHelper();

    const columns = [
        columnHelper.accessor("id", {
            header: () => "ID",
            cell: (props) => props.renderValue(),
            //   footer: props => props.column.id,
        }),
        columnHelper.accessor("name", {
            header: () => "Company Head Name",
            cell: (props) => props.renderValue(),
            //   footer: info => info.column.id,
        }),
        columnHelper.display({
            id: "select",
            header: ({ table }) => (
                <IndeterminateCheckbox
                    {...{
                        checked: table.getIsAllRowsSelected(),
                        indeterminate: table.getIsSomeRowsSelected(),
                        onChange: table.getToggleAllRowsSelectedHandler(),
                    }}
                />
            ),
            cell: ({ row }) => (
                <div>
                    <IndeterminateCheckbox
                        {...{
                            checked: row.getIsSelected(),
                            disabled: !row.getCanSelect(),
                            indeterminate: row.getIsSomeSelected(),
                            onChange: row.getToggleSelectedHandler(),
                        }}
                    />
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
        enableRowSelection: true,
        initialState: {
            sorting: [{ id: "name", desc: true }],
        },
        getCoreRowModel: getCoreRowModel(),
        getSortedRowModel: getSortedRowModel(),
    });
    console.log(table);
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
    }, [isLoading, isUpdatingVisibleCompanies]);

    useEffect(() => {
        if (fetchedData?.length > 0) {
            for (let i = 0; i < fetchedData.length; i++) {
                table.setRowSelection(fetchedData?.map((item) => item.visible));
            }
        }
    }, [fetchedData]);

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

                                                        {/* {console.log(
                                                            header.column.getIsSorted()
                                                        )} */}
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
            </section>
        );
    }
};

export default VisibleCompaniesForm;
