import { useRef, useEffect, useState } from "react";
import { FaUserPlus } from "react-icons/fa6";
import { FaPlus } from "react-icons/fa6";
import { Field, ErrorMessage, FieldArray } from "formik";
import {
    useLazyGetSingleEmployeePfEsiDetailQuery,
    useGetSingleEmployeePfEsiDetailQuery,
} from "../../../../authentication/api/employeeEntryApiSlice";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const EmployeeFamilyNomineeDetail = ({
    handleSubmit,
    handleChange,
    handleBlur,
    values,
    errors,
    isValid,
    touched,
    errorMessage,
    setErrorMessage,
    setFieldValue,
    globalCompany,
    setShowLoadingBar,
    cancelButtonClicked,
    isEditing,
    dirty,
    initialValues,
    addedEmployeeId,
    familyNomineeDetailInitailValues,
    updateEmployeeId,
    singleEmployeePfEsiDetail,
}) => {
    // console.log(errorMessage);
    let employeeId = addedEmployeeId;
    if (isEditing) {
        employeeId = updateEmployeeId;
    }

    // const {
    //     data: singleEmployeePfEsiDetail,
    //     isLoading,
    //     isSuccess,
    //     isError,
    //     error,
    //     isFetching,
    //     refetch,
    // } = useGetSingleEmployeePfEsiDetailQuery({
    //     company: globalCompany.id,
    //     id: isEditing,
    //     singleEmployeePfEsiDetail,
    // });

    // const [
    //     getSingleEmployeePfEsiDetail,
    //     {
    //         data: {
    //             user: PfEsiDetailDetailUser,
    //             company: PfEsiDetailDetailCompany,
    //             ...singleEmployeePfEsiDetail
    //         } = {},
    //         isLoading,
    //     } = {},
    //     // lastPromiseInfo,
    // ] = useLazyGetSingleEmployeePfEsiDetailQuery({ pollingInterval: 0 });
    // console.log(singleEmployeePfEsiDetail);
    // console.log(familyNomineeDetailInitailValues);
    // console.log(errors);
    // useEffect(() => {
    //     const fetchData = async () => {
    //         try {
    //             const data = await getSingleEmployeePfEsiDetail({
    //                 company: globalCompany.id,
    //                 id: employeeId,
    //             }).unwrap();
    //             console.log(data);

    //             console.log(updateEmployeeId);
    //         } catch (err) {
    //             console.log(err);
    //             getSingleEmployeePfEsiDetail.abort()
    //         }
    //     };
    //     fetchData();
    //     console.log("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    // }, [employeeId]);
    // useEffect(() => {
    //     setShowLoadingBar(isLoading);
    // }, [isLoading]);

    const useNomineeShare = (fieldName, nomineeFieldName) => {
        const previousNomineeRef = useRef([]);

        useEffect(() => {
            const hasNomineeChanged = values.familyNomineeDetail.some(
                (detail, index) =>
                    detail[fieldName] !== previousNomineeRef.current[index]
            );

            if (hasNomineeChanged) {
                const count = values.familyNomineeDetail.reduce(
                    (accumulator, detail) =>
                        detail[fieldName] ? accumulator + 1 : accumulator,
                    0
                );
                const divisionResult =
                    count > 0 ? (100 / count).toFixed(2) : "0.00";
                console.log(parseFloat(divisionResult));
                values.familyNomineeDetail.forEach((detail, index) => {
                    if (detail[fieldName]) {
                        setFieldValue(
                            `familyNomineeDetail.${index}.${nomineeFieldName}`,
                            parseFloat(divisionResult)
                        );
                    } else {
                        setFieldValue(
                            `familyNomineeDetail.${index}.${nomineeFieldName}`,
                            ""
                        );
                    }
                });
            }

            // Update the previousNomineeRef with the current nominee values
            previousNomineeRef.current = values.familyNomineeDetail.map(
                (detail) => detail[fieldName]
            );
        }, [values.familyNomineeDetail]);
    };

    // Usage
    useNomineeShare("isFaNominee", "faNomineeShare");
    useNomineeShare("isGratuityNominee", "gratuityNomineeShare");
    useNomineeShare("isEsiNominee", "esiNomineeShare");
    useNomineeShare("isPfNominee", "pfNomineeShare");

    useEffect(() => {
        values.familyNomineeDetail.forEach((detail, index) => {
            if (!detail.pfBenefits && detail.isPfNominee) {
                setFieldValue(
                    `familyNomineeDetail.${index}.isPfNominee`,
                    false
                );
            }
            if (!detail.esiBenefit && detail.isEsiNominee) {
                setFieldValue(
                    `familyNomineeDetail.${index}.isEsiNominee`,
                    false
                );
            }
        });
    }, [values.familyNomineeDetail]);

    if (!addedEmployeeId && !isEditing) {
        return (
            <div className="mt-1 text-xl dark:text-redAccent-600 text-redAccent-500 font-bold mx-auto">
                Please add Personal Details First
            </div>
        );
    } else if (singleEmployeePfEsiDetail === null) {
        return (
            <div className="mt-1 text-xl dark:text-redAccent-600 text-redAccent-500 font-bold mx-auto">
                Please add PF and ESI Details First
            </div>
        );
    } else {
        return (
            <div className="text-gray-900 dark:text-slate-100">
                {/* <h1 className="font-medium text-2xl mb-2">Add Employee</h1> */}
                <form
                    action=""
                    className="flex flex-col gap-2 justify-center"
                    onSubmit={handleSubmit}
                >
                    <section className="flex flex-row gap-10 flex-wrap lg:flex-nowrap justify-center">
                        <div className="w-fit">
                            <FieldArray
                                name="familyNomineeDetail"
                                render={(arrayHelpers) => {
                                    return (
                                        <div>
                                            {values.familyNomineeDetail.map(
                                                (member, index) => (
                                                    <div
                                                        key={index}
                                                        className="flex flex-row flex-wrap gap-1 border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25 border-2 rounded p-2 my-1"
                                                    >
                                                        <div className="flex flex-row justify-between w-full">
                                                            <div className="text-blueAccent-500 dark:text-blueAccent-600 mr-2">{`${
                                                                index + 1
                                                            }`}</div>
                                                            <div>
                                                                <button
                                                                    type="button"
                                                                    className="dark:bg-redAccent-700 bg-redAccent-500 dark:hover:bg-redAccent-600 hover:bg-redAccent-700 rounded-md p-2 inline-flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
                                                                    onClick={() =>
                                                                        arrayHelpers.remove(
                                                                            index
                                                                        )
                                                                    }
                                                                >
                                                                    <svg
                                                                        className="h-4 w-4"
                                                                        xmlns="http://www.w3.org/2000/svg"
                                                                        fill="none"
                                                                        viewBox="0 0 24 24"
                                                                        stroke="currentColor"
                                                                        aria-hidden="true"
                                                                    >
                                                                        <path
                                                                            strokeLinecap="round"
                                                                            strokeLinejoin="round"
                                                                            strokeWidth="2"
                                                                            d="M6 18L18 6M6 6l12 12"
                                                                        />
                                                                    </svg>
                                                                    {/* <svg
                                                                        class="h-6 w-6"
                                                                        xmlns="http://www.w3.org/2000/svg"
                                                                        fill="none"
                                                                        viewBox="0 0 24 24"
                                                                        stroke="currentColor"
                                                                        aria-hidden="true"
                                                                    >
                                                                        <path
                                                                            stroke-linecap="round"
                                                                            stroke-linejoin="round"
                                                                            stroke-width="2"
                                                                            d="M5 12h14M12 5v14"
                                                                        />
                                                                    </svg> */}
                                                                </button>
                                                            </div>
                                                        </div>
                                                        <div className="flex flex-row flex-wrap gap-1">
                                                            <div>
                                                                <label
                                                                    htmlFor={`familyNomineeDetail.${index}.name`}
                                                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                                                                >
                                                                    Name
                                                                </label>
                                                                <Field
                                                                    className={classNames(
                                                                        errors
                                                                            .familyNomineeDetail?.[
                                                                            index
                                                                        ]
                                                                            ?.name &&
                                                                            touched
                                                                                .familyNomineeDetail?.[
                                                                                index
                                                                            ]
                                                                                ?.name
                                                                            ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                                                            : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                                                        "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition min-w-32 block"
                                                                    )}
                                                                    type="text"
                                                                    name={`familyNomineeDetail.${index}.name`}
                                                                    maxLength={
                                                                        100
                                                                    }
                                                                />
                                                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                                                    <ErrorMessage
                                                                        name={`familyNomineeDetail.${index}.name`}
                                                                    />
                                                                </div>
                                                            </div>

                                                            <div>
                                                                <label
                                                                    htmlFor={`familyNomineeDetail.${index}.address`}
                                                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                                                                >
                                                                    Address
                                                                </label>
                                                                <Field
                                                                    className={classNames(
                                                                        errors
                                                                            .familyNomineeDetail?.[
                                                                            index
                                                                        ]
                                                                            ?.address &&
                                                                            touched
                                                                                .familyNomineeDetail?.[
                                                                                index
                                                                            ]
                                                                                ?.address
                                                                            ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                                                            : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                                                        "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition min-w-32 block"
                                                                    )}
                                                                    type="text"
                                                                    name={`familyNomineeDetail.${index}.address`}
                                                                />
                                                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                                                    <ErrorMessage
                                                                        name={`familyNomineeDetail.${index}.address`}
                                                                    />
                                                                </div>
                                                            </div>

                                                            <div>
                                                                <label
                                                                    htmlFor={`familyNomineeDetail.${index}.dob`}
                                                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                                                                >
                                                                    DOB
                                                                </label>
                                                                <Field
                                                                    className={classNames(
                                                                        errors
                                                                            .familyNomineeDetail?.[
                                                                            index
                                                                        ]
                                                                            ?.dob &&
                                                                            touched
                                                                                .familyNomineeDetail?.[
                                                                                index
                                                                            ]
                                                                                ?.dob
                                                                            ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                                                            : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                                                        "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-[132px] block"
                                                                    )}
                                                                    type="date"
                                                                    name={`familyNomineeDetail.${index}.dob`}
                                                                />
                                                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                                                    <ErrorMessage
                                                                        name={`familyNomineeDetail.${index}.dob`}
                                                                    />
                                                                </div>
                                                            </div>

                                                            <div>
                                                                <label
                                                                    htmlFor={`familyNomineeDetail.${index}.relation`}
                                                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                                                                >
                                                                    Relation
                                                                </label>
                                                                <Field
                                                                    as="select"
                                                                    name={`familyNomineeDetail.${index}.relation`}
                                                                    className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 block my-1"
                                                                >
                                                                    <option value="Father">
                                                                        Father
                                                                    </option>
                                                                    <option value="Mother">
                                                                        Mother
                                                                    </option>
                                                                    <option value="Wife">
                                                                        Wife
                                                                    </option>
                                                                    <option value="Son">
                                                                        Son
                                                                    </option>
                                                                    <option value="Brother">
                                                                        Brother
                                                                    </option>
                                                                    <option value="Sister">
                                                                        Sister
                                                                    </option>
                                                                    <option value="Daughter">
                                                                        Daughter
                                                                    </option>
                                                                    <option value="Husband">
                                                                        Husband
                                                                    </option>
                                                                </Field>
                                                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                                                    <ErrorMessage
                                                                        name={`familyNomineeDetail.${index}.relation`}
                                                                    />
                                                                </div>
                                                            </div>

                                                            <div>
                                                                <label
                                                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                                                                    htmlFor={`familyNomineeDetail.${index}.residing`}
                                                                >
                                                                    Residing?
                                                                </label>
                                                                <Field
                                                                    type="checkbox"
                                                                    name={`familyNomineeDetail.${index}.residing`}
                                                                    className="rounded w-4 h-4 accent-teal-600 mx-auto mt-2 block"
                                                                />
                                                            </div>

                                                            <div>
                                                                <label
                                                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm text-center block mt-1"
                                                                    htmlFor={`familyNomineeDetail.${index}.esiBenefit`}
                                                                >
                                                                    Esi
                                                                </label>
                                                                <Field
                                                                    type="checkbox"
                                                                    name={`familyNomineeDetail.${index}.esiBenefit`}
                                                                    className="rounded w-4 h-4 accent-teal-600 mx-auto mt-2 block"
                                                                    disabled={
                                                                        !singleEmployeePfEsiDetail.esiAllow
                                                                    }
                                                                />
                                                                {!singleEmployeePfEsiDetail.esiAllow && (
                                                                    <p className="mt-1 text-xs dark:text-blueAccent-600 text-blueAccent-500 font-bold">
                                                                        ESI is
                                                                        not
                                                                        allowed
                                                                    </p>
                                                                )}
                                                            </div>

                                                            <div>
                                                                <label
                                                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm text-center block mt-1"
                                                                    htmlFor={`familyNomineeDetail.${index}.pfBenefits`}
                                                                >
                                                                    Pf
                                                                </label>
                                                                <Field
                                                                    type="checkbox"
                                                                    name={`familyNomineeDetail.${index}.pfBenefits`}
                                                                    className="rounded w-4 h-4 accent-teal-600 mx-auto mt-2 block"
                                                                    disabled={
                                                                        !singleEmployeePfEsiDetail.pfAllow
                                                                    }
                                                                />
                                                                {!singleEmployeePfEsiDetail.pfAllow && (
                                                                    <p className="mt-1 text-xs dark:text-blueAccent-600 text-blueAccent-500 font-bold">
                                                                        Pf is
                                                                        not
                                                                        allowed
                                                                    </p>
                                                                )}
                                                            </div>

                                                            <div>
                                                                <label
                                                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm mx-2"
                                                                    htmlFor={`familyNomineeDetail.${index}.isEsiNominee`}
                                                                >
                                                                    Esi Nominee
                                                                </label>
                                                                <Field
                                                                    type="checkbox"
                                                                    name={`familyNomineeDetail.${index}.isEsiNominee`}
                                                                    className="rounded w-4 h-4 accent-teal-600 mx-auto mt-2 block"
                                                                    disabled={
                                                                        !singleEmployeePfEsiDetail.esiAllow
                                                                    }
                                                                />
                                                                {!singleEmployeePfEsiDetail.esiAllow && (
                                                                    <p className="mt-1 text-xs dark:text-blueAccent-600 text-blueAccent-500 font-bold">
                                                                        ESI is
                                                                        not
                                                                        allowed
                                                                    </p>
                                                                )}
                                                            </div>

                                                            <div>
                                                                <label
                                                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                                                                    htmlFor={`familyNomineeDetail.${index}.esiNomineeShare`}
                                                                >
                                                                    Esi %
                                                                </label>
                                                                <Field
                                                                    className={classNames(
                                                                        errors
                                                                            .familyNomineeDetail?.[
                                                                            index
                                                                        ]
                                                                            ?.esiNomineeShare &&
                                                                            touched
                                                                                .familyNomineeDetail?.[
                                                                                index
                                                                            ]
                                                                                ?.esiNomineeShare
                                                                            ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                                                            : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                                                        "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-20 block custom-number-input"
                                                                    )}
                                                                    type="number"
                                                                    maxLength={
                                                                        5
                                                                    }
                                                                    name={`familyNomineeDetail.${index}.esiNomineeShare`}
                                                                    disabled={
                                                                        !values
                                                                            .familyNomineeDetail[
                                                                            index
                                                                        ]
                                                                            .isEsiNominee
                                                                    }
                                                                />
                                                                {errors
                                                                    ?.familyNomineeDetail?.[
                                                                    index
                                                                ]
                                                                    ?.esiNomineeShare && (
                                                                    <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                                                        {
                                                                            errors
                                                                                ?.familyNomineeDetail?.[
                                                                                index
                                                                            ]
                                                                                ?.esiNomineeShare
                                                                        }
                                                                    </div>
                                                                )}
                                                                {errorMessage[
                                                                    index
                                                                ]
                                                                    ?.esiNomineeShare && (
                                                                    <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold w-20">
                                                                        {
                                                                            errorMessage[
                                                                                index
                                                                            ]
                                                                                .esiNomineeShare
                                                                        }
                                                                    </p>
                                                                )}
                                                            </div>

                                                            <div>
                                                                <label
                                                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm mx-2"
                                                                    htmlFor={`familyNomineeDetail.${index}.isPfNominee`}
                                                                >
                                                                    Pf Nominee
                                                                </label>
                                                                <Field
                                                                    type="checkbox"
                                                                    name={`familyNomineeDetail.${index}.isPfNominee`}
                                                                    className="rounded w-4 h-4 accent-teal-600 mx-auto mt-2 block"
                                                                    disabled={
                                                                        !singleEmployeePfEsiDetail.pfAllow ||
                                                                        !values
                                                                            .familyNomineeDetail[
                                                                            index
                                                                        ]
                                                                            .pfBenefits
                                                                    }
                                                                />
                                                                {!singleEmployeePfEsiDetail.pfAllow && (
                                                                    <p className="mt-1 text-xs dark:text-blueAccent-600 text-blueAccent-500 font-bold">
                                                                        Pf is
                                                                        not
                                                                        allowed
                                                                    </p>
                                                                )}
                                                            </div>

                                                            <div>
                                                                <label
                                                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                                                                    htmlFor={`familyNomineeDetail.${index}.pfNomineeShare`}
                                                                >
                                                                    Pf %
                                                                </label>
                                                                <Field
                                                                    className={classNames(
                                                                        errors
                                                                            .familyNomineeDetail?.[
                                                                            index
                                                                        ]
                                                                            ?.pfNomineeShare &&
                                                                            touched
                                                                                .familyNomineeDetail?.[
                                                                                index
                                                                            ]
                                                                                ?.pfNomineeShare
                                                                            ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                                                            : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                                                        "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-20 block custom-number-input"
                                                                    )}
                                                                    type="number"
                                                                    maxLength={
                                                                        5
                                                                    }
                                                                    name={`familyNomineeDetail.${index}.pfNomineeShare`}
                                                                    disabled={
                                                                        !values
                                                                            .familyNomineeDetail[
                                                                            index
                                                                        ]
                                                                            .isPfNominee
                                                                    }
                                                                />
                                                                {errors
                                                                    ?.familyNomineeDetail?.[
                                                                    index
                                                                ]
                                                                    ?.pfNomineeShare && (
                                                                    <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                                                        {
                                                                            errors
                                                                                ?.familyNomineeDetail?.[
                                                                                index
                                                                            ]
                                                                                ?.pfNomineeShare
                                                                        }
                                                                    </div>
                                                                )}
                                                                {errorMessage[
                                                                    index
                                                                ]
                                                                    ?.pfNomineeShare && (
                                                                    <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold w-20">
                                                                        {
                                                                            errorMessage[
                                                                                index
                                                                            ]
                                                                                .pfNomineeShare
                                                                        }
                                                                    </p>
                                                                )}
                                                            </div>

                                                            <div>
                                                                <label
                                                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm mx-2"
                                                                    htmlFor={`familyNomineeDetail.${index}.isFaNominee`}
                                                                >
                                                                    FA Nominee
                                                                </label>
                                                                <Field
                                                                    type="checkbox"
                                                                    name={`familyNomineeDetail.${index}.isFaNominee`}
                                                                    className="rounded w-4 h-4 accent-teal-600 mx-auto mt-2 block"
                                                                />
                                                            </div>

                                                            <div>
                                                                <label
                                                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                                                                    htmlFor={`familyNomineeDetail.${index}.faNomineeShare`}
                                                                >
                                                                    FA %
                                                                </label>
                                                                <Field
                                                                    className={classNames(
                                                                        errors
                                                                            .familyNomineeDetail?.[
                                                                            index
                                                                        ]
                                                                            ?.faNomineeShare &&
                                                                            touched
                                                                                .familyNomineeDetail?.[
                                                                                index
                                                                            ]
                                                                                ?.faNomineeShare
                                                                            ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                                                            : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                                                        "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-20 block custom-number-input"
                                                                    )}
                                                                    type="number"
                                                                    maxLength={
                                                                        5
                                                                    }
                                                                    name={`familyNomineeDetail.${index}.faNomineeShare`}
                                                                    disabled={
                                                                        !values
                                                                            .familyNomineeDetail[
                                                                            index
                                                                        ]
                                                                            .isFaNominee
                                                                    }
                                                                />
                                                                {errors
                                                                    ?.familyNomineeDetail?.[
                                                                    index
                                                                ]
                                                                    ?.faNomineeShare && (
                                                                    <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                                                        {
                                                                            errors
                                                                                ?.familyNomineeDetail?.[
                                                                                index
                                                                            ]
                                                                                ?.faNomineeShare
                                                                        }
                                                                    </div>
                                                                )}
                                                                {errorMessage[
                                                                    index
                                                                ]
                                                                    ?.faNomineeShare && (
                                                                    <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold w-20">
                                                                        {
                                                                            errorMessage[
                                                                                index
                                                                            ]
                                                                                .faNomineeShare
                                                                        }
                                                                    </p>
                                                                )}
                                                            </div>

                                                            <div>
                                                                <label
                                                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm mx-2"
                                                                    htmlFor={`familyNomineeDetail.${index}.isGratuityNominee`}
                                                                >
                                                                    Gratuity
                                                                    Nominee
                                                                </label>
                                                                <Field
                                                                    type="checkbox"
                                                                    name={`familyNomineeDetail.${index}.isGratuityNominee`}
                                                                    className="rounded w-4 h-4 accent-teal-600 mx-auto mt-2 block"
                                                                />
                                                            </div>

                                                            <div>
                                                                <label
                                                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                                                                    htmlFor={`familyNomineeDetail.${index}.gratuityNomineeShare`}
                                                                >
                                                                    Gratuity %
                                                                </label>
                                                                <Field
                                                                    className={classNames(
                                                                        errors
                                                                            .familyNomineeDetail?.[
                                                                            index
                                                                        ]
                                                                            ?.gratuityNomineeShare &&
                                                                            touched
                                                                                .familyNomineeDetail?.[
                                                                                index
                                                                            ]
                                                                                ?.gratuityNomineeShare
                                                                            ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                                                            : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                                                        "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-20 block custom-number-input"
                                                                    )}
                                                                    type="number"
                                                                    maxLength={
                                                                        5
                                                                    }
                                                                    name={`familyNomineeDetail.${index}.gratuityNomineeShare`}
                                                                    disabled={
                                                                        !values
                                                                            .familyNomineeDetail[
                                                                            index
                                                                        ]
                                                                            .isGratuityNominee
                                                                    }
                                                                />
                                                                {errors
                                                                    ?.familyNomineeDetail?.[
                                                                    index
                                                                ]
                                                                    ?.gratuityNomineeShare && (
                                                                    <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                                                        {
                                                                            errors
                                                                                ?.familyNomineeDetail?.[
                                                                                index
                                                                            ]
                                                                                ?.gratuityNomineeShare
                                                                        }
                                                                    </div>
                                                                )}
                                                                {errorMessage[
                                                                    index
                                                                ]
                                                                    ?.gratuityNomineeShare && (
                                                                    <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold w-20">
                                                                        {
                                                                            errorMessage[
                                                                                index
                                                                            ]
                                                                                .gratuityNomineeShare
                                                                        }
                                                                    </p>
                                                                )}
                                                            </div>
                                                        </div>
                                                    </div>
                                                )
                                            )}
                                            <div>
                                                <button
                                                    onClick={() =>
                                                        arrayHelpers.insert(
                                                            values
                                                                .familyNomineeDetail
                                                                .length + 1,
                                                            familyNomineeDetailInitailValues
                                                        )
                                                    }
                                                    className="dark:bg-teal-700 bg-teal-500 dark:hover:bg-teal-600 hover:bg-teal-700 rounded-md p-2 inline-flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
                                                    type="button"
                                                >
                                                    <svg
                                                        className="h-4 w-4"
                                                        xmlns="http://www.w3.org/2000/svg"
                                                        fill="none"
                                                        viewBox="0 0 24 24"
                                                        stroke="currentColor"
                                                        aria-hidden="true"
                                                    >
                                                        <path
                                                            strokeLinecap="round"
                                                            strokeLinejoin="round"
                                                            strokeWidth="2"
                                                            d="M5 12h14M12 5v14"
                                                        />
                                                    </svg>
                                                </button>
                                            </div>
                                        </div>
                                    );
                                }}
                            />
                        </div>

                        {/* <div className="w-fit">
                            <label
                                htmlFor={"salaryDetail.overtimeType"}
                                className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                            >
                                Overtime Type
                            </label>
                            <Field
                                as="select"
                                name="salaryDetail.overtimeType"
                                className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 block my-1"
                            >
                                <option value="no_overtime">No Overtime</option>
                                <option value="all_days">All Days</option>
                                <option value="holiday_weekly_off">
                                    Holiday/Weekly Off
                                </option>
                            </Field>
                            <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                <ErrorMessage
                                    name={"salaryDetail.overtimeType"}
                                />
                            </div>

                            
                        </div> */}
                    </section>
                    {errorMessage && errorMessage.error && (
                        <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                            {errorMessage.error}
                        </p>
                    )}

                    <section className="flex flex-row gap-4 mt-4 mb-2">
                        <button
                            className={classNames(
                                isValid
                                    ? "dark:hover:bg-teal-600  hover:bg-teal-600"
                                    : "opacity-40",
                                "dark:bg-teal-700 rounded w-20 p-2 text-base font-medium bg-teal-500"
                            )}
                            type="submit"
                            // disabled={!isValid}
                            onClick={handleSubmit}
                        >
                            {isEditing ? "Update" : "Add"}
                        </button>
                        <button
                            type="button"
                            className="bg-zinc-400 hover:bg-zinc-500 dark:bg-zinc-600 rounded w-20 p-2 text-base font-medium dark:hover:bg-zinc-700"
                            onClick={() => {
                                cancelButtonClicked(isEditing);
                                setErrorMessage("");
                            }}
                        >
                            Cancel
                        </button>
                    </section>
                </form>
            </div>
        );
    }
};
export default EmployeeFamilyNomineeDetail;
