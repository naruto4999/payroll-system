import React, { useEffect, useMemo, useState } from "react";
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
    FaAngleUp,
    FaAngleDown,
    FaEye,
} from "react-icons/fa";
import { useSelector } from "react-redux";
import {
    useGetShiftsQuery,
    useAddShiftMutation,
    useUpdateShiftMutation,
    useDeleteShiftMutation,
} from "../../../../authentication/api/shiftEntryApiSlice";
import EditShift from "./EditShift";
import ViewShift from "./ViewShift";
import { useOutletContext } from "react-router-dom";
import ReactModal from "react-modal";
import { Formik } from "formik";
import AddShift from "./AddShift";
import { ShiftSchema } from "./ShiftEntrySchema";

ReactModal.setAppElement("#root");

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const ShiftEntryForm = () => {
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
    } = useGetShiftsQuery(globalCompany);
    // console.log(fetchedData)
    const [addShift, { isLoading: isAddingShift }] = useAddShiftMutation();
    const [updateShift, { isLoading: isUpdatingShift }] =
        useUpdateShiftMutation();
    const [deleteShift, { isLoading: isDeletingShift }] =
        useDeleteShiftMutation();
    const [addShiftPopover, setAddShiftPopover] = useState(false);
    const [showLoadingBar, setShowLoadingBar] = useOutletContext();
    const [editShiftPopover, setEditShiftPopover] = useState(false);
    const [viewShiftPopover, setViewShiftPopover] = useState(false);
    const [updateShiftId, setUpdateShiftId] = useState("");
    // const [msg, setMsg] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    const [viewShiftId, setViewShiftId] = useState("");

    const editShiftPopoverHandler = (shift) => {
        console.log(shift);
        setUpdateShiftId(shift.id);
        setEditShiftPopover(!editShiftPopover);
    };

    const viewShiftPopoverHandler = (shift) => {
        console.log(shift);
        setViewShiftPopover(!viewShiftPopover);
        setViewShiftId(shift.id);
    };

    const addButtonClicked = async (values, formikBag) => {
        console.log(formikBag);
        const toSend = {
            company: globalCompany.id,
            name: values.shiftName,
            beginning_time: values.shiftBeginningTime + ":00",
            end_time: values.shiftEndTime + ":00",
            lunch_time: values.lunchTime,
            tea_time: values.teaTime,
            late_grace: values.lateGrace,
            ot_begin_after: values.otBeginAfter,
            next_shift_dealy: values.nextShiftDelay,
            accidental_punch_buffer: values.accidentalPunchBuffer,
            half_day_minimum_minutes: values.halfDayMinimumMinutes,
            full_day_minimum_minutes: values.fullDayMinimumMinutes,
            short_leaves: values.shortLeaves,
        };
        try {
            const data = await addShift(toSend).unwrap();
            console.log(data);
            setErrorMessage("");
            setAddShiftPopover(!addShiftPopover);
            formikBag.resetForm();
        } catch (err) {
            console.log(err);
            if (err.status === 400) {
                setErrorMessage("Shift with this name already exists");
            } else {
                console.log(err);
            }
        }
    };

    const updateButtonClicked = async (values, formikBag) => {
        console.log(values);
        try {
            const data = await updateShift({
                id: updateShiftId,
                name: values.shiftName,
                company: globalCompany.id,
                beginning_time: values.shiftBeginningTime + ":00",
                end_time: values.shiftEndTime + ":00",
                lunch_time: values.lunchTime,
                tea_time: values.teaTime,
                late_grace: values.lateGrace,
                ot_begin_after: values.otBeginAfter,
                next_shift_dealy: values.nextShiftDelay,
                accidental_punch_buffer: values.accidentalPunchBuffer,
                half_day_minimum_minutes: values.halfDayMinimumMinutes,
                full_day_minimum_minutes: values.fullDayMinimumMinutes,
                short_leaves: values.shortLeaves,
            }).unwrap();
            console.log(data);
            setErrorMessage("");
            formikBag.resetForm();
            editShiftPopoverHandler({ id: "" });
        } catch (err) {
            console.log(err);
            if (err.status === 400) {
                setErrorMessage("Shift with this name already exists");
            } else {
                console.log(err);
            }
        }
    };

    const deleteButtonClicked = async (id) => {
        console.log(id);
        deleteShift({ id: id, company: globalCompany.id });
    };

    const columnHelper = createColumnHelper();

    const columns = [
        columnHelper.accessor("id", {
            header: () => "ID",
            cell: (props) => props.renderValue(),
            //   footer: props => props.column.id,
        }),
        columnHelper.accessor("name", {
            header: () => "Shift Name",
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
                            editShiftPopoverHandler(props.row.original)
                        }
                    >
                        <FaPen className="h-4" />
                    </div>
                    <div
                        className="p-1.5 dark:bg-blueAccent-600 rounded bg-blueAccent-600 dark:hover:bg-blueAccent-500 hover:bg-blueAccent-700"
                        onClick={() =>
                            viewShiftPopoverHandler(props.row.original)
                        }
                    >
                        <FaEye className="h-4" />
                    </div>
                </div>
            ),
        }),
    ];

    const data = useMemo(
        () => (fetchedData ? [...fetchedData] : []),
        [fetchedData]
    );

    const shiftForEdit = () => {
        const shift = fetchedData.find((shift) => shift.id === updateShiftId);
        return {
            shiftName: shift.name,
            shiftBeginningTime: shift.beginning_time
                .split(":")
                .slice(0, 2)
                .join(":"),
            shiftEndTime: shift.end_time.split(":").slice(0, 2).join(":"),
            lunchTime: shift.lunch_time,
            teaTime: shift.tea_time,
            lateGrace: shift.late_grace,
            otBeginAfter: shift.ot_begin_after,
            nextShiftDelay: shift.next_shift_dealy,
            accidentalPunchBuffer: shift.accidental_punch_buffer,
            halfDayMinimumMinutes: shift.half_day_minimum_minutes,
            fullDayMinimumMinutes: shift.full_day_minimum_minutes,
            shortLeaves: shift.short_leaves,
        };
    };

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
        // Add more for adding, editing and deleting later on
        setShowLoadingBar(
            isLoading || isAddingShift || isUpdatingShift || isDeletingShift
        );
    }, [isLoading, isAddingShift, isUpdatingShift, isDeletingShift]);

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
                        <h1 className="text-3xl font-medium">Shifts</h1>
                        <p className="text-sm my-2">Add more shifts here</p>
                    </div>
                    <button
                        className="dark:bg-teal-700 my-auto rounded p-2 text-base font-medium bg-teal-500 hover:bg-teal-600 dark:hover:bg-teal-600 whitespace-nowrap"
                        onClick={() => setAddShiftPopover(true)}
                    >
                        Add Shift
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
                    className="fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-2xl h-fit bg-zinc-300 dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl"
                    isOpen={addShiftPopover}
                    onRequestClose={() => setAddShiftPopover(false)}
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <Formik
                        initialValues={{
                            shiftName: "",
                            shiftBeginningTime: "",
                            shiftEndTime: "",
                            lunchTime: "",
                            teaTime: "",
                            lateGrace: "",
                            otBeginAfter: "",
                            nextShiftDelay: "",
                            accidentalPunchBuffer: "",
                            halfDayMinimumMinutes: "",
                            fullDayMinimumMinutes: "",
                            shortLeaves: "",
                        }}
                        validationSchema={ShiftSchema}
                        onSubmit={addButtonClicked}
                        component={(props) => (
                            <AddShift
                                {...props}
                                errorMessage={errorMessage}
                                setErrorMessage={setErrorMessage}
                                setAddShiftPopover={setAddShiftPopover}
                            />
                        )}
                    />
                </ReactModal>

                <ReactModal
                    className="fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-2xl h-fit bg-zinc-300 dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl"
                    isOpen={editShiftPopover}
                    onRequestClose={() =>
                        editShiftPopoverHandler({
                            id: "",
                        })
                    }
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <Formik
                        initialValues={
                            updateShiftId
                                ? shiftForEdit(updateShiftId)
                                : {
                                      shiftName: "",
                                      shiftBeginningTime: "",
                                      shiftEndTime: "",
                                      lunchTime: "",
                                      teaTime: "",
                                      lateGrace: "",
                                      otBeginAfter: "",
                                      nextShiftDelay: "",
                                      accidentalPunchBuffer: "",
                                      halfDayMinimumMinutes: "",
                                      fullDayMinimumMinutes: "",
                                      shortLeaves: "",
                                  }
                        }
                        validationSchema={ShiftSchema}
                        onSubmit={updateButtonClicked}
                        component={(props) => (
                            <EditShift
                                {...props}
                                errorMessage={errorMessage}
                                setErrorMessage={setErrorMessage}
                                editShiftPopoverHandler={
                                    editShiftPopoverHandler
                                }
                            />
                        )}
                    />
                </ReactModal>

                <ReactModal
                    className="fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-2xl h-fit bg-zinc-300 dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl"
                    isOpen={viewShiftPopover}
                    onRequestClose={() =>
                        viewShiftPopoverHandler({
                            id: null,
                        })
                    }
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <ViewShift
                        shift={
                            viewShiftId
                                ? fetchedData.find(
                                      (shift) => shift.id === viewShiftId
                                  )
                                : null
                        }
                        viewShiftPopoverHandler={viewShiftPopoverHandler}
                    />
                </ReactModal>
            </section>
        );
    }
};

export default ShiftEntryForm;
