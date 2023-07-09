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
    useAddEmployeeProfessionalDetailMutation,
    useLazyGetSingleEmployeePersonalDetailQuery,
    useUpdateEmployeePersonalDetailMutation,
    useUpdateEmployeeProfessionalDetailMutation,
    useLazyGetSingleEmployeeProfessionalDetailQuery,
} from "../../../../authentication/api/employeeEntryApiSlice";
import { useGetEarningsHeadsQuery } from "../../../../authentication/api/earningsHeadEntryApiSlice";

// import EditEmployee from "./EditEmployee";
// import ViewEmployee from "./ViewEmployee";
import { useOutletContext } from "react-router-dom";
import ReactModal from "react-modal";
import { Formik } from "formik";
import EmployeePersonalDetail from "./EmployeePersonalDetail";
import {
    EmployeePersonalDetailSchema,
    EmployeeProfessionalDetailSchema,
} from "./EmployeeEntrySchema";
import AddEmployeeNavigationBar from "./AddEmployeeNavigationBar";
import EmployeeProfessionalDetail from "./EmployeeProfessionalDetail";
import EmployeeSalaryDetail from "./EmployeeSalaryDetail";
import * as yup from "yup";

ReactModal.setAppElement("#root");

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

function getObjectDifferences(obj1, obj2) {
    const diffObj = {};
    if (Object.keys(obj1).length === 0) {
        return obj2;
    }

    for (const key in obj1) {
        if (obj1.hasOwnProperty(key) && obj2.hasOwnProperty(key)) {
            let value1 = obj1[key];
            let value2 = obj2[key];

            if (value1 === null) {
                obj1[key] = "";
            }

            if (value2 === null) {
                obj2[key] = "";
            }
            if (obj1[key] !== obj2[key]) {
                diffObj[key] = obj2[key];
            }
        }
    }

    return diffObj;
}

const checkNullUndefinedValues = (obj) => {
    for (let key in obj) {
        if (obj[key] === null || obj[key] === undefined) {
            obj[key] = "";
        }
    }
    return obj;
};

const EmployeeEntryForm = () => {
    const globalCompany = useSelector((state) => state.globalCompany);
    const [
        getSingleEmployeePersonalDetail,
        {
            data: {
                user: PersonalDetailUser,
                company: PersonalDetailCompany,
                isActive: PersonalDetailIsActive,
                createdAt: PersonalDetailCreatedAt,
                ...singleEmployeePersonalDetail
            } = {},
        } = {},
        // lastPromiseInfo,
    ] = useLazyGetSingleEmployeePersonalDetailQuery();

    const [
        getSingleEmployeeProfessionalDetail,
        {
            data: {
                user: ProfessionalDetailUser,
                company: ProfessionalDetailCompany,
                ...singleEmployeeProfessionalDetail
            } = {},
        } = {},
        // lastPromiseInfo,
    ] = useLazyGetSingleEmployeeProfessionalDetailQuery();
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
    const [
        addEmployeeProfessionalDetail,
        { isLoading: isAddingEmployeeProfessionalDetail },
    ] = useAddEmployeeProfessionalDetailMutation();

    const [
        updateEmployeePersonalDetail,
        { isLoading: isUpdatingEmployeePersonalDetail },
    ] = useUpdateEmployeePersonalDetailMutation();
    const [
        updateEmployeeProfessionalDetail,
        { isLoading: isUpdatingEmployeeProfessionalDetail },
    ] = useUpdateEmployeeProfessionalDetailMutation();
    const {
        data: fetchedEarningsHeads,
        isLoading: isLoadingEarningsHeads,
        isSuccess: EarningsHeadsSuccess,
    } = useGetEarningsHeadsQuery(globalCompany);

    let earningHeadOptions = [];
    if (EarningsHeadsSuccess) {
        earningHeadOptions = fetchedEarningsHeads.map((earningHead) => ({
            id: earningHead.id,
            name: earningHead.name,
        }));
    }
    let earningHeadInitialValues = {};
    if (EarningsHeadsSuccess) {
        fetchedEarningsHeads.forEach((earningHead) => {
            earningHeadInitialValues[earningHead.name] = "";
        });
    }
    // const [deleteEmployeePersonalDetail, { isLoading: isDeletingEmployeePersonalDetail }] =
    //     useDeleteEmployeePersonalDetailMutation();
    const [addEmployeePopover, setAddEmployeePopover] = useState({
        addEmployeePersonalDetail: false,
        addEmployeeProfessionalDetail: false,
        addEmployeeSalaryDetail: false,
        addEmployeePfEsiDetail: false,
    });
    const [editEmployeePopover, setEditEmployeePopover] = useState({
        editEmployeePersonalDetail: false,
        editEmployeeProfessionalDetail: false,
        editEmployeeSalaryDetail: false,
        editEmployeePfEsiDetail: false,
    });
    const [showLoadingBar, setShowLoadingBar] = useOutletContext();
    const [viewEmployeePopover, setViewEmployeePopover] = useState(false);
    const [updateEmployeeId, setUpdateEmployeeId] = useState(null);
    const [addedEmployeeId, setAddedEmployeeId] = useState(null);
    // const [msg, setMsg] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    // const [viewEmployeeId, setViewEmployeeId] = useState("");

    const addEmployeePopoverHandler = (popoverName) => {
        setAddEmployeePopover((prevState) => {
            const updatedState = {};
            Object.keys(prevState).forEach((key) => {
                updatedState[key] = key === popoverName;
            });
            return updatedState;
        });
    };
    console.log(updateEmployeeId);

    const currentDate = new Date();
    const formattedDate = currentDate.toISOString().split("T")[0];

    const editEmployeeProfessionalDetailInitialValues = {
        dateOfJoining: formattedDate,
        dateOfConfirm: "",
        department: "",
        designation: "",
        category: "",
        salaryGrade: "",
        shift: "",
        weeklyOff: "sun",
        extraOff: "no_off",
    };

    const editEmployeePopoverHandler = async ({ popoverName, id }) => {
        console.log(popoverName);
        console.log(id);
        setUpdateEmployeeId(id);
        setAddedEmployeeId(id);
        console.log(updateEmployeeId);
        if (popoverName === "editEmployeePersonalDetail") {
            try {
                const data = await getSingleEmployeePersonalDetail({
                    id: id,
                    company: globalCompany.id,
                }).unwrap();
                console.log(data);
                setEditEmployeePopover((prevState) => {
                    const updatedState = {};
                    Object.keys(prevState).forEach((key) => {
                        updatedState[key] = key === popoverName;
                    });
                    return updatedState;
                });
                console.log(updateEmployeeId);
            } catch (err) {
                console.log(err);
            }
        } else if (popoverName === "editEmployeeProfessionalDetail") {
            console.log("ishhhhhhhhh meeeeeeeee bish");
            try {
                const data = await getSingleEmployeeProfessionalDetail({
                    id: id,
                    company: globalCompany.id,
                }).unwrap();
                console.log(data);
                setEditEmployeePopover((prevState) => {
                    const updatedState = {};
                    Object.keys(prevState).forEach((key) => {
                        updatedState[key] = key === popoverName;
                    });
                    return updatedState;
                });
                console.log(updateEmployeeId);
            } catch (err) {
                if (err.status === 404) {
                    console.log("me hereeeeeeeeeeeeeeeeeeeeeeeeeeeeee");
                    setEditEmployeePopover((prevState) => {
                        const updatedState = {};
                        Object.keys(prevState).forEach((key) => {
                            updatedState[key] = key === popoverName;
                        });
                        return updatedState;
                    });
                }
                console.log(err);
            }
        }

        // setEditEmployeePopover(!editEmployeePopover);
    };

    const viewEmployeePopoverHandler = (employee) => {
        console.log(employee);
        setViewEmployeePopover(!viewEmployeePopover);
        setViewEmployeeId(employee.id);
    };

    const cancelButtonClicked = (isEditing) => {
        if (isEditing) {
            setUpdateEmployeeId(null);
            setEditEmployeePopover({
                editEmployeePersonalDetail: false,
                editEmployeeProfessionalDetail: false,
                editEmployeeSalaryDetail: false,
                editEmployeePfEsiDetail: false,
            });
        } else {
            setAddEmployeePopover({
                addEmployeePersonalDetail: false,
                addEmployeeProfessionalDetail: false,
                addEmployeeSalaryDetail: false,
                addEmployeePfEsiDetail: false,
            });
        }
    };

    const addPersonalDetailButtonClicked = async (values, formikBag) => {
        console.log(values);
        const formData = new FormData();
        for (const key in values) {
            if (values.hasOwnProperty(key)) {
                formData.append(key, values[key]);
            }
        }
        formData.append("company", globalCompany.id);

        try {
            const data = await addEmployeePersonalDetail({
                formData,
            }).unwrap();
            console.log(data);
            setErrorMessage("");
            setAddedEmployeeId(data.id);
            // setAddEmployeePopover(!addEmployeePopover);
            formikBag.resetForm();
            addEmployeePopoverHandler("addEmployeeProfessionalDetail");
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
    console.log(Object.keys(singleEmployeeProfessionalDetail).length === 0);

    const addProfessionalDetailButtonClicked = async (values, formikBag) => {
        console.log(values);
        console.log(addedEmployeeId);

        try {
            const data = await addEmployeeProfessionalDetail({
                ...values,
                employee: addedEmployeeId,
                company: globalCompany.id,
            }).unwrap();
            console.log(data);
            setErrorMessage("");
            // setAddedEmployeeId(data.id)
            // setAddEmployeePopover(!addEmployeePopover);
            formikBag.resetForm();
            addEmployeePopoverHandler("addEmployeeSalaryDetail");
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

    const updatePersonalDetailButtonClicked = async (values, formikBag) => {
        // console.log(formikBag);
        console.log(values);
        console.log(singleEmployeePersonalDetail);
        const differences = getObjectDifferences(
            singleEmployeePersonalDetail,
            values
        );
        console.log(differences);
        if (Object.keys(differences).length !== 0) {
            console.log("in if fucking whatever");
            const formData = new FormData();
            for (const key in differences) {
                if (differences.hasOwnProperty(key)) {
                    formData.append(key, differences[key]);
                }
            }
            formData.append("company", globalCompany.id);
            formData.append("id", values.id);
            // console.log(globalCompany.id)

            try {
                const data = await updateEmployeePersonalDetail({
                    formData,
                    id: values.id,
                    globalCompany: globalCompany.id,
                }).unwrap();
                console.log(data);
                setErrorMessage("");
                setAddedEmployeeId(data.id);
                // setAddEmployeePopover(!addEmployeePopover);
                // addEmployeePopoverHandler("addEmployeeProfessionalDetail");
            } catch (err) {
                console.log(err);
                if (err.status === 400) {
                    console.log(err.data.error);
                    setErrorMessage(err.data.error);
                } else {
                    console.log(err);
                }
            }
        }
    };

    const updateProfessionalDetailButtonClicked = async (values, formikBag) => {
        console.log(values);
        console.log(singleEmployeeProfessionalDetail);
        const differences = getObjectDifferences(
            singleEmployeeProfessionalDetail,
            values
        );
        console.log(differences);
        if (Object.keys(differences).length !== 0) {
            console.log("in if fucking whatever");

            try {
                const data = await updateEmployeeProfessionalDetail({
                    ...differences,
                    employee: values.employee,
                    globalCompany: globalCompany.id,
                }).unwrap();
                console.log(data);
                setErrorMessage("");
            } catch (err) {
                console.log(err);
                if (err.status === 400) {
                    console.log(err.data.error);
                    setErrorMessage(err.data.error);
                } else {
                    console.log(err);
                }
            }
        }
    };

    const addSalaryDetailButtonClicked = async (values, formikBag) => {
        console.log(values);
    };

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
        columnHelper.accessor("attendanceCardNo", {
            header: () => "ACN",
            cell: (props) => props.renderValue(),
            //   footer: props => props.column.id,
        }),

        columnHelper.accessor("name", {
            header: () => "Employee Name",
            cell: (props) => props.renderValue(),
            //   footer: info => info.column.id,
        }),
        columnHelper.accessor("dateOfJoining", {
            header: () => "DOJ",
            cell: (props) => props.renderValue(),
            //   footer: info => info.column.id,
        }),
        columnHelper.accessor("designation", {
            header: () => "Designation",
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
                        onClick={() => {
                            editEmployeePopoverHandler({
                                id: props.row.original.id,
                                popoverName: "editEmployeePersonalDetail",
                            });
                        }}
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

    let EmployeeSalaryDetailSchema = yup.object().shape({
        earningsHead: yup.object().shape(
            Object.keys(earningHeadInitialValues).reduce((schema, key) => {
                return {
                    ...schema,
                    [key]: yup.number().required(`${key} is required`),
                };
            }, {})
        ),
    });

    useEffect(() => {
        // Add more for adding, editing and deleting later on
        setShowLoadingBar(
            isLoading ||
                isAddingEmployeePersonalDetail ||
                isAddingEmployeeProfessionalDetail ||
                isUpdatingEmployeePersonalDetail
        );
    }, [
        isLoading,
        isAddingEmployeePersonalDetail,
        isAddingEmployeeProfessionalDetail,
        isUpdatingEmployeePersonalDetail,
    ]);
    console.log(checkNullUndefinedValues(singleEmployeeProfessionalDetail));
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
                        onClick={() =>
                            addEmployeePopoverHandler(
                                "addEmployeePersonalDetail"
                            )
                        }
                    >
                        Add Employee
                    </button>
                </div>
                <div className="rounded border border-black border-opacity-50 shadow-md max-w-6xl mx-auto max-h-[80dvh] lg:max-h-[84dvh] overflow-y-auto scrollbar">
                    <table className="w-full border-collapse text-center text-sm">
                        <thead className="bg-blueAccent-600 dark:bg-blueAccent-700 sticky top-0">
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
                        <tbody className="divide-y divide-black divide-opacity-50 border-t border-black border-opacity-50 max-h-20 overflow-y-auto">
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

                {/* For Adding */}
                <ReactModal
                    className="fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-[1100px] w-fit max-h-[100dvh] h-fit bg-zinc-300 dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl overflow-y-scroll scrollbar"
                    isOpen={
                        addEmployeePopover.addEmployeePersonalDetail ||
                        addEmployeePopover.addEmployeeProfessionalDetail ||
                        addEmployeePopover.addEmployeeSalaryDetail ||
                        addEmployeePopover.addEmployeePfEsiDetail
                    }
                    onRequestClose={() =>
                        setAddEmployeePopover({
                            addEmployeePersonalDetail: false,
                            addEmployeeProfessionalDetail: false,
                            addEmployeeSalaryDetail: false,
                            addEmployeePfEsiDetail: false,
                        })
                    }
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <>
                        <AddEmployeeNavigationBar
                            addEmployeePopover={addEmployeePopover}
                            addEmployeePopoverHandler={
                                addEmployeePopoverHandler
                            }
                            editEmployeePopover={editEmployeePopover}
                            editEmployeePopoverHandler={
                                editEmployeePopoverHandler
                            }
                            isEditing={false}
                            updateEmployeeId={updateEmployeeId}
                            getSingleEmployeeProfessionalDetail={
                                getSingleEmployeeProfessionalDetail
                            }
                            globalCompany={globalCompany.id}
                        />
                        {addEmployeePopover.addEmployeePersonalDetail && (
                            <Formik
                                initialValues={{
                                    photo: "",

                                    // 1st column
                                    paycode: "",
                                    attendanceCardNo: "",
                                    name: "",
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
                                onSubmit={addPersonalDetailButtonClicked}
                                component={(props) => (
                                    <>
                                        <EmployeePersonalDetail
                                            {...props}
                                            errorMessage={errorMessage}
                                            setErrorMessage={setErrorMessage}
                                            cancelButtonClicked={
                                                cancelButtonClicked
                                            }
                                            isEditing={false}
                                        />
                                    </>
                                )}
                            />
                        )}

                        {addEmployeePopover.addEmployeeProfessionalDetail && (
                            <Formik
                                initialValues={
                                    editEmployeeProfessionalDetailInitialValues
                                }
                                validationSchema={
                                    EmployeeProfessionalDetailSchema
                                }
                                onSubmit={addProfessionalDetailButtonClicked}
                                component={(props) => (
                                    <>
                                        <EmployeeProfessionalDetail
                                            {...props}
                                            errorMessage={errorMessage}
                                            setErrorMessage={setErrorMessage}
                                            // setAddEmployeePopover={
                                            //     setAddEmployeePopover
                                            // }
                                            globalCompany={globalCompany}
                                            setShowLoadingBar={
                                                setShowLoadingBar
                                            }
                                            isEditing={false}
                                            cancelButtonClicked={
                                                cancelButtonClicked
                                            }
                                        />
                                    </>
                                )}
                            />
                        )}

                        {addEmployeePopover.addEmployeeSalaryDetail && (
                            <Formik
                                initialValues={{
                                    earningsHead: {
                                        ...earningHeadInitialValues,
                                    },
                                }}
                                validationSchema={EmployeeSalaryDetailSchema}
                                onSubmit={addSalaryDetailButtonClicked}
                                component={(props) => (
                                    <>
                                        <EmployeeSalaryDetail
                                            {...props}
                                            errorMessage={errorMessage}
                                            setErrorMessage={setErrorMessage}
                                            // setAddEmployeePopover={
                                            //     setAddEmployeePopover
                                            // }
                                            globalCompany={globalCompany}
                                            setShowLoadingBar={
                                                setShowLoadingBar
                                            }
                                            isEditing={false}
                                            cancelButtonClicked={
                                                cancelButtonClicked
                                            }
                                        />
                                    </>
                                )}
                            />
                        )}
                    </>
                </ReactModal>

                {/* For Editing */}
                <ReactModal
                    className="fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-[1100px] w-fit max-h-[100dvh] h-fit bg-zinc-300 dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl overflow-y-scroll scrollbar"
                    isOpen={
                        editEmployeePopover.editEmployeePersonalDetail ||
                        editEmployeePopover.editEmployeeProfessionalDetail ||
                        editEmployeePopover.editEmployeeSalaryDetail ||
                        editEmployeePopover.editEmployeePfEsiDetail
                    }
                    onRequestClose={() =>
                        setEditEmployeePopover({
                            editEmployeePersonalDetail: false,
                            editEmployeeProfessionalDetail: false,
                            editEmployeeSalaryDetail: false,
                            editEmployeePfEsiDetail: false,
                        })
                    }
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <>
                        <AddEmployeeNavigationBar
                            addEmployeePopover={addEmployeePopover}
                            addEmployeePopoverHandler={
                                addEmployeePopoverHandler
                            }
                            editEmployeePopover={editEmployeePopover}
                            editEmployeePopoverHandler={
                                editEmployeePopoverHandler
                            }
                            isEditing={true}
                            updateEmployeeId={updateEmployeeId}
                            getSingleEmployeeProfessionalDetail={
                                getSingleEmployeeProfessionalDetail
                            }
                            globalCompany={globalCompany.id}
                        />
                        {editEmployeePopover.editEmployeePersonalDetail && (
                            <Formik
                                initialValues={
                                    singleEmployeePersonalDetail !== undefined
                                        ? checkNullUndefinedValues(
                                              singleEmployeePersonalDetail
                                          )
                                        : {}
                                }
                                validationSchema={EmployeePersonalDetailSchema}
                                onSubmit={updatePersonalDetailButtonClicked}
                                component={(props) => (
                                    <>
                                        <EmployeePersonalDetail
                                            {...props}
                                            errorMessage={errorMessage}
                                            setErrorMessage={setErrorMessage}
                                            cancelButtonClicked={
                                                cancelButtonClicked
                                            }
                                            isEditing={true}
                                        />
                                    </>
                                )}
                            />
                        )}

                        {editEmployeePopover.editEmployeeProfessionalDetail && (
                            <Formik
                                initialValues={
                                    singleEmployeeProfessionalDetail !==
                                    undefined
                                        ? checkNullUndefinedValues(
                                              singleEmployeeProfessionalDetail
                                          )
                                        : editEmployeeProfessionalDetailInitialValues
                                }
                                validationSchema={
                                    EmployeeProfessionalDetailSchema
                                }
                                onSubmit={
                                    Object.keys(
                                        singleEmployeeProfessionalDetail
                                    ).length === 0
                                        ? addProfessionalDetailButtonClicked
                                        : updateProfessionalDetailButtonClicked
                                }
                                component={(props) => (
                                    <>
                                        <EmployeeProfessionalDetail
                                            {...props}
                                            errorMessage={errorMessage}
                                            setErrorMessage={setErrorMessage}
                                            // setEditEmployeePopover={
                                            //     setEditEmployeePopover
                                            // }
                                            globalCompany={globalCompany}
                                            setShowLoadingBar={
                                                setShowLoadingBar
                                            }
                                            isEditing={true}
                                            cancelButtonClicked={
                                                cancelButtonClicked
                                            }
                                        />
                                    </>
                                )}
                            />
                        )}
                    </>
                </ReactModal>

                {/* <ReactModal
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
