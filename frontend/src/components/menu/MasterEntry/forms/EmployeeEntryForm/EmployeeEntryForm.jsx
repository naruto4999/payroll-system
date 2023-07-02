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
    useGetEmployeePersonalDetailsQuery,
    useAddEmployeePersonalDetailMutation,
} from "../../../../authentication/api/employeeEntryApiSlice";
// import EditEmployee from "./EditEmployee";
// import ViewEmployee from "./ViewEmployee";
import { useOutletContext } from "react-router-dom";
import ReactModal from "react-modal";
import { Formik } from "formik";
import AddEmployee from "./AddEmployee";
import { EmployeePersonalDetailSchema } from "./EmployeeEntrySchema";

ReactModal.setAppElement("#root");

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const EmployeeEntryForm = () => {
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
    } = useGetEmployeePersonalDetailsQuery(globalCompany);
    console.log(fetchedData);
    const [
        addEmployeePersonalDetail,
        { isLoading: isAddingEmployeePersonalDetail },
    ] = useAddEmployeePersonalDetailMutation();
    // const [updateEmployeePersonalDetail, { isLoading: isUpdatingEmployeePersonalDetail }] =
    //     useUpdateEmployeePersonalDetailMutation();
    // const [deleteEmployeePersonalDetail, { isLoading: isDeletingEmployeePersonalDetail }] =
    //     useDeleteEmployeePersonalDetailMutation();
    const [addEmployeePopover, setAddEmployeePopover] = useState(false);
    const [showLoadingBar, setShowLoadingBar] = useOutletContext();
    const [editEmployeePopover, setEditEmployeePopover] = useState(false);
    const [viewEmployeePopover, setViewEmployeePopover] = useState(false);
    const [updateEmployeeId, setUpdateEmployeeId] = useState("");
    // const [msg, setMsg] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    // const [viewEmployeeId, setViewEmployeeId] = useState("");

    const editEmployeePopoverHandler = (employee) => {
        console.log(employee);
        setUpdateEmployeeId(employee.id);
        setEditEmployeePopover(!editEmployeePopover);
    };

    const viewEmployeePopoverHandler = (employee) => {
        console.log(employee);
        setViewEmployeePopover(!viewEmployeePopover);
        setViewEmployeeId(employee.id);
    };

    const addButtonClicked = async (values, formikBag) => {
        console.log(values);
        // const formData = new FormData();
        // formData.append("company", globalCompany.id);
        // formData.append("name", values.employeeName);
        // formData.append("paycode", values.paycode);
        // formData.append("attendance_card_no", values.attendanceCardNumber);
        // formData.append("photo", values.photo);
        const formData = new FormData();
        formData.append("company", globalCompany.id);
        formData.append("name", values.employeeName);
        formData.append("paycode", values.paycode);
        formData.append("attendance_card_no", values.attendanceCardNumber);
        formData.append("photo", values.photo);
        formData.append("father_or_husband_name", values.fatherOrHusbandName);
        formData.append("mother_name", values.motherName);
        formData.append("wife_name", values.wifeName);
        formData.append("dob", values.dob);
        formData.append("phone_number", values.phoneNumber);
        formData.append("alternate_phone_number", values.alternatePhoneNumber);
        formData.append("email", values.email);
        formData.append("pan_number", values.panNumber);
        formData.append("driving_licence", values.drivingLicence);
        formData.append("passport", values.passport);
        formData.append("aadhaar", values.aadhaar);
        formData.append("handicapped", values.handicapped);
        formData.append("gender", values.gender);
        formData.append("marital_status", values.maritalStatus);
        formData.append("blood_group", values.bloodGroup);
        formData.append("religion", values.religion);
        formData.append(
            "education_qualification",
            values.educationQualification
        );
        formData.append(
            "technical_qualification",
            values.technicalQualification
        );
        formData.append("local_address", values.localAddress);
        formData.append("local_district", values.localDistrict);
        formData.append(
            "local_state_or_union_territory",
            values.localStateOrUnionTerritory
        );
        formData.append("local_pincode", values.localPincode);
        formData.append("permanent_address", values.permanentAddress);
        formData.append("permanent_district", values.permanentDistrict);
        formData.append(
            "permanent_state_or_union_territory",
            values.permanentStateOrUnionTerritory
        );
        formData.append("permanent_pincode", values.permanentPincode);

        try {
            const data = await addEmployeePersonalDetail({
                formData,
            }).unwrap();
            console.log(data);
            setErrorMessage("");
            setAddEmployeePopover(!addEmployeePopover);
            formikBag.resetForm();
        } catch (err) {
            console.log(err);
            if (err.status === 400) {
                console.log(err.data.error);
                setErrorMessage(err.data.error);
            } else {
                console.log(err);
            }
        }
    };

    // const updateButtonClicked = async (values, formikBag) => {
    //     console.log(values);
    //     try {
    //         const data = await updateShift({
    //             id: updateShiftId,
    //             name: values.shiftName,
    //             company: globalCompany.id,
    //             beginning_time: values.shiftBeginningTime + ":00",
    //             end_time: values.shiftEndTime + ":00",
    //             lunch_time: values.lunchTime,
    //             tea_time: values.teaTime,
    //             late_grace: values.lateGrace,
    //             ot_begin_after: values.otBeginAfter,
    //             next_shift_dealy: values.nextShiftDelay,
    //             accidental_punch_buffer: values.accidentalPunchBuffer,
    //             half_day_minimum_minutes: values.halfDayMinimumMinutes,
    //             full_day_minimum_minutes: values.fullDayMinimumMinutes,
    //             short_leaves: values.shortLeaves,
    //         }).unwrap();
    //         console.log(data);
    //         setErrorMessage("");
    //         formikBag.resetForm();
    //         editShiftPopoverHandler({ id: "" });
    //     } catch (err) {
    //         console.log(err);
    //         if (err.status === 400) {
    //             setErrorMessage("Shift with this name already exists");
    //         } else {
    //             console.log(err);
    //         }
    //     }
    // };

    const deleteButtonClicked = async (id) => {
        console.log(id);
        // deleteShift({ id: id, company: globalCompany.id });
    };

    const columnHelper = createColumnHelper();

    const columns = [
        columnHelper.accessor("paycode", {
            header: () => "Paycode",
            cell: (props) => props.renderValue(),
            //   footer: props => props.column.id,
        }),
        columnHelper.accessor("name", {
            header: () => "Employee Name",
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
                            editEmployeePopoverHandler(props.row.original)
                        }
                    >
                        <FaPen className="h-4" />
                    </div>
                    <div
                        className="p-1.5 dark:bg-blueAccent-600 rounded bg-blueAccent-600 dark:hover:bg-blueAccent-500 hover:bg-blueAccent-700"
                        onClick={() =>
                            viewEmployeePopoverHandler(props.row.original)
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
        setShowLoadingBar(isLoading);
    }, [isLoading]);

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
                        <h1 className="text-3xl font-medium">Employees</h1>
                        <p className="text-sm my-2">
                            Add and manage employees here
                        </p>
                    </div>
                    <button
                        className="dark:bg-teal-700 my-auto rounded p-2 text-base font-medium bg-teal-500 hover:bg-teal-600 dark:hover:bg-teal-600 whitespace-nowrap"
                        onClick={() => setAddEmployeePopover(true)}
                    >
                        Add Employee
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
                    className="fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-[1100px] max-h-screen h-fit bg-zinc-300 dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl overflow-y-scroll scrollbar"
                    isOpen={addEmployeePopover}
                    onRequestClose={() => setAddEmployeePopover(false)}
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <Formik
                        initialValues={{
                            photo: "",

                            // 1st column
                            paycode: "",
                            attendanceCardNumber: "",
                            employeeName: "",
                            fatherOrHusbandName: "",
                            motherName: "",
                            wifeName: "",
                            dob: "",
                            phoneNumber: "",

                            // 2nd column
                            alternatePhoneNumber: "",
                            religion: "",
                            email: "",
                            handicapped: false,
                            gender: "",
                            maritalStatus: "",
                            bloodGroup: "",

                            // 3rd column
                            panNumber: "",
                            drivingLicence: "",
                            passport: "",
                            aadhaar: "",
                            educationQualification: "",
                            technicalQualification: "",
                            localAddress: "",

                            // 4th column
                            localDistrict: "",
                            localStateOrUnionTerritory: "",
                            localPincode: "",
                            permanentAddress: "",
                            permanentDistrict: "",
                            permanentStateOrUnionTerritory: "",
                            permanentPincode: "",
                        }}
                        validationSchema={EmployeePersonalDetailSchema}
                        onSubmit={addButtonClicked}
                        component={(props) => (
                            <AddEmployee
                                {...props}
                                errorMessage={errorMessage}
                                setErrorMessage={setErrorMessage}
                                setAddEmployeePopover={setAddEmployeePopover}
                            />
                        )}
                    />
                </ReactModal>

                {/* <ReactModal
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
                </ReactModal> */}
            </section>
        );
    }
};

export default EmployeeEntryForm;
