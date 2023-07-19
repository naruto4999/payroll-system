import { useRef, useEffect, useState } from "react";
import { FaUserPlus } from "react-icons/fa6";
import { FaCircleNotch } from "react-icons/fa6";
import { Field, ErrorMessage } from "formik";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};
const timeFormat = (time) => {
    const timeParts = time.split(":");
    const formattedTime = `${timeParts[0]}:${timeParts[1]}`;
    return formattedTime;
};
const EmployeeSalaryDetail = ({
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
    addedEmployeeId
}) => {
    console.log(values);
    useEffect(() => {
        if (
            values.salaryDetail.overtimeType !== "no_overtime" &&
            values.salaryDetail.overtimeRate === ""
        ) {
            setFieldValue("salaryDetail.overtimeRate", "S");
        } else if (values.salaryDetail.overtimeType === "no_overtime") {
            setFieldValue("salaryDetail.overtimeRate", "");
        }
    }, [values.salaryDetail.overtimeType]);
    if (!addedEmployeeId && !isEditing) {
        return (
            <div className="mt-1 text-xl dark:text-redAccent-600 text-redAccent-500 font-bold mx-auto">
                Please add Personal Details First
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
                        <label
                                htmlFor="year"
                                className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                            >
                                Salary for year
                            </label>
                            <Field
                                className={classNames(
                                    errors.year &&
                                        touched.year
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full custom-number-input"
                                )}
                                type="number"
                                name="year"
                            />
                            <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                <ErrorMessage name="year" />
                            </div>
                            {Object.keys(initialValues.earningsHead).map(
                                (key) => (
                                    <div key={key}>
                                        <label
                                            htmlFor={key}
                                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                                        >
                                            {key}
                                        </label>
                                        <div className="relative">
                                            <Field
                                                className={classNames(
                                                    errors.earningsHead?.[
                                                        key
                                                    ] &&
                                                        touched.earningsHead?.[
                                                            key
                                                        ]
                                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full custom-number-input"
                                                )}
                                                type="number"
                                                name={`earningsHead.${key}`}
                                            />
                                            <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                                <ErrorMessage
                                                    name={`earningsHead.${key}`}
                                                />
                                            </div>
                                        </div>
                                    </div>
                                )
                            )}
                        </div>

                        <div className="w-fit">
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

                            <label
                                htmlFor={"salaryDetail.overtimeRate"}
                                className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                            >
                                Overtime Rate
                            </label>
                            {values.salaryDetail.overtimeType !==
                            "no_overtime" ? (
                                <Field
                                    as="select"
                                    name="salaryDetail.overtimeRate"
                                    className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 block my-1"
                                >
                                    <option value="S">Single</option>
                                    <option value="D">Double</option>
                                </Field>
                            ) : (
                                <div className="mt-1 text-xs dark:text-blueAccent-700 text-blueAccent-500 font-bold">
                                    No overtime is allowed
                                </div>
                            )}
                            {errorMessage && errorMessage.overtimeRate && (
                                <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errorMessage.overtimeRate}
                                </p>
                            )}
                            {console.log(errorMessage)}
                            <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                <ErrorMessage
                                    name={"salaryDetail.overtimeRate"}
                                />
                            </div>

                            <label
                                htmlFor={"salaryDetail.salaryMode"}
                                className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                            >
                                Salary Mode
                            </label>
                            <Field
                                as="select"
                                name="salaryDetail.salaryMode"
                                className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 block my-1"
                            >
                                <option value="monthly">Monthly</option>
                                <option value="daily">Daily</option>
                                <option value="piece_rate">Piece Rate</option>
                            </Field>
                            <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                <ErrorMessage
                                    name={"salaryDetail.salaryMode"}
                                />
                            </div>

                            <label
                                htmlFor={"salaryDetail.paymentMode"}
                                className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                            >
                                Payment Mode
                            </label>
                            <Field
                                as="select"
                                name="salaryDetail.paymentMode"
                                className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 block my-1"
                            >
                                <option value="bank_transfer">
                                    Bank Transfer
                                </option>
                                <option value="cheque">Cheque</option>
                                <option value="cash">Cash</option>
                                <option value="rtgs">RTGS</option>
                                <option value="neft">NEFT</option>
                            </Field>
                            <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                <ErrorMessage
                                    name={"salaryDetail.paymentMode"}
                                />
                            </div>

                            <label
                                htmlFor="salaryDetail.bankName"
                                className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                            >
                                Bank Name
                            </label>
                            <Field
                                className={classNames(
                                    errors.salaryDetail?.bankName &&
                                        touched.salaryDetail?.bankName
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full custom-number-input"
                                )}
                                type="text"
                                name="salaryDetail.bankName"
                            />
                            <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                <ErrorMessage name="salaryDetail.bankName" />
                            </div>

                            <label
                                htmlFor="salaryDetail.accountNumber"
                                className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                            >
                                Account Number
                            </label>
                            <Field
                                className={classNames(
                                    errors.salaryDetail?.accountNumber &&
                                        touched.salaryDetail?.accountNumber
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full custom-number-input"
                                )}
                                type="text"
                                name="salaryDetail.accountNumber"
                                maxLength={30}
                            />
                            <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                <ErrorMessage name="salaryDetail.accountNumber" />
                            </div>

                            <label
                                htmlFor="salaryDetail.ifcs"
                                className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                            >
                                IFSC
                            </label>
                            <Field
                                className={classNames(
                                    errors.salaryDetail?.ifcs &&
                                        touched.salaryDetail?.ifcs
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full custom-number-input"
                                )}
                                type="text"
                                name="salaryDetail.ifcs"
                                maxLength={25}
                            />
                            <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                <ErrorMessage name="salaryDetail.ifcs" />
                            </div>
                        </div>

                        <div className="w-fit">
                            <label className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block my-2">
                                Labour Welfare Fund:
                                <Field
                                    type="checkbox"
                                    name="salaryDetail.labourWellfareFund"
                                    className="rounded w-4 h-4 accent-teal-600 mx-4 translate-y-0.5"
                                />
                            </label>

                            <label className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block my-2">
                                Late Deduction:
                                <Field
                                    type="checkbox"
                                    name="salaryDetail.lateDeduction"
                                    className="rounded w-4 h-4 accent-teal-600 mx-4 translate-y-0.5"
                                />
                            </label>

                            <label className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block my-2">
                                Bonus Allow:
                                <Field
                                    type="checkbox"
                                    name="salaryDetail.bonusAllow"
                                    className="rounded w-4 h-4 accent-teal-600 mx-4 translate-y-0.5"
                                />
                            </label>

                            <label className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block my-2">
                                Bonus Exg.:
                                <Field
                                    type="checkbox"
                                    name="salaryDetail.bonusExg"
                                    className="rounded w-4 h-4 accent-teal-600 mx-4 translate-y-0.5"
                                />
                            </label>
                        </div>
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
                            disabled={!isValid}
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
export default EmployeeSalaryDetail;
