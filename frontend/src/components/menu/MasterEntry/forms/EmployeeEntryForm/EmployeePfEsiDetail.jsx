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
const EmployeePfEsiDetail = ({
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
}) => {
    console.log(values);
    console.log(errors)
    useEffect(() => {
        if (values.pfLimitIgnoreEmployee === false) {
            setFieldValue("pfLimitIgnoreEmployeeValue", "");
        }
        if (values.pfPercentIgnoreEmployee === false) {
            setFieldValue("pfPercentIgnoreEmployeeValue", "")
        }
        if (values.pfLimitIgnoreEmployer === false) {
            setFieldValue("pfLimitIgnoreEmployerValue", "")
        }
        if (values.pfPercentIgnoreEmployer === false) {
            setFieldValue("pfPercentIgnoreEmployerValue", "")
        }
    }, [values.pfLimitIgnoreEmployee, values.pfPercentIgnoreEmployee, values.pfLimitIgnoreEmployer, values.pfPercentIgnoreEmployer]);

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
                            <label className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block my-2">
                                PF Allow:
                                <Field
                                    type="checkbox"
                                    name="pfAllow"
                                    className="rounded w-4 h-4 accent-teal-600 mx-4 translate-y-0.5"
                                />
                            </label>
                            <div>
                                <label
                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                                    htmlFor={"pfNumber"}
                                >
                                    PF Number
                                </label>
                                <Field
                                    className={classNames(
                                        errors.pfNumber && touched.pfNumber
                                            ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                            : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                        "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full block"
                                    )}
                                    type="text"
                                    maxLength={50}
                                    name={"pfNumber"}
                                />
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    <ErrorMessage name="pfNumber" />
                                </div>
                            </div>

                            <div>
                                <label className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block mt-2">
                                    PF Limit Ignore Employee:
                                    <Field
                                        type="checkbox"
                                        name="pfLimitIgnoreEmployee"
                                        className="rounded w-4 h-4 accent-teal-600 mx-4 translate-y-0.5"
                                    />
                                </label>
                                <Field
                                    className={classNames(
                                        errors.pfLimitIgnoreEmployeeValue &&
                                            touched.pfLimitIgnoreEmployeeValue
                                            ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                            : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                        "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full block custom-number-input"
                                    )}
                                    type="number"
                                    name={"pfLimitIgnoreEmployeeValue"}
                                    disabled={!values.pfLimitIgnoreEmployee}
                                />
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    <ErrorMessage name="pfLimitIgnoreEmployeeValue" />
                                </div>
                            </div>

                            <div>
                                <label className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block mt-2">
                                    PF % Ignore Employee:
                                    <Field
                                        type="checkbox"
                                        name="pfPercentIgnoreEmployee"
                                        className="rounded w-4 h-4 accent-teal-600 mx-4 translate-y-0.5"
                                    />
                                </label>
                                <Field
                                    className={classNames(
                                        errors.pfPercentIgnoreEmployeeValue &&
                                            touched.pfPercentIgnoreEmployeeValue
                                            ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                            : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                        "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full block custom-number-input"
                                    )}
                                    type="number"
                                    maxLength={5}
                                    name={"pfPercentIgnoreEmployeeValue"}
                                    disabled={!values.pfPercentIgnoreEmployee}
                                />
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    <ErrorMessage name="pfPercentIgnoreEmployeeValue" />
                                </div>
                            </div>

                            <div>
                                <label className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block mt-2">
                                    PF Limit Ignore Employer:
                                    <Field
                                        type="checkbox"
                                        name="pfLimitIgnoreEmployer"
                                        className="rounded w-4 h-4 accent-teal-600 mx-4 translate-y-0.5"
                                    />
                                </label>
                                <Field
                                    className={classNames(
                                        errors.pfLimitIgnoreEmployerValue &&
                                            touched.pfLimitIgnoreEmployerValue
                                            ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                            : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                        "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full block custom-number-input"
                                    )}
                                    type="number"
                                    name={"pfLimitIgnoreEmployerValue"}
                                    disabled={!values.pfLimitIgnoreEmployer}

                                />
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    <ErrorMessage name="pfLimitIgnoreEmployerValue" />
                                </div>
                            </div>

                            <div>
                                <label className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block mt-2">
                                    PF % Ignore Employer:
                                    <Field
                                        type="checkbox"
                                        name="pfPercentIgnoreEmployer"
                                        className="rounded w-4 h-4 accent-teal-600 mx-4 translate-y-0.5"
                                    />
                                </label>
                                <Field
                                    className={classNames(
                                        errors.pfPercentIgnoreEmployerValue &&
                                            touched.pfPercentIgnoreEmployerValue
                                            ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                            : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                        "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full block custom-number-input"
                                    )}
                                    type="number"
                                    maxLength={5}
                                    name={"pfPercentIgnoreEmployerValue"}
                                    disabled={!values.pfPercentIgnoreEmployer}

                                />
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    <ErrorMessage name="pfPercentIgnoreEmployerValue" />
                                </div>
                            </div>
                        </div>

                        <div className="w-fit">
                            {/* <label className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block my-2">
                                Bonus Exg.:
                                <Field
                                    type="checkbox"
                                    name="salaryDetail.bonusExg"
                                    className="rounded w-4 h-4 accent-teal-600 mx-4 translate-y-0.5"
                                />
                            </label> */}

                            <div>
                                <label className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block my-2">
                                    ESI Allow:
                                    <Field
                                        type="checkbox"
                                        name="esiAllow"
                                        className="rounded w-4 h-4 accent-teal-600 mx-4 translate-y-0.5"
                                    />
                                </label>
                            </div>
                            <div>
                                <label
                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                                    htmlFor={"esiNumber"}
                                >
                                    ESI Number
                                </label>
                                <Field
                                    className={classNames(
                                        errors.esiNumber && touched.esiNumber
                                            ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                            : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                        "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full block"
                                    )}
                                    type="text"
                                    maxLength={30}
                                    name={"esiNumber"}
                                />
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    <ErrorMessage name="esiNumber" />
                                </div>
                            </div>

                            <div>
                                <label
                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                                    htmlFor={"esiDispensary"}
                                >
                                    ESI Dispensary
                                </label>
                                <Field
                                    className={classNames(
                                        errors.esiDispensary &&
                                            touched.esiDispensary
                                            ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                            : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                        "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full block"
                                    )}
                                    type="text"
                                    maxLength={100}
                                    name={"esiDispensary"}
                                />
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    <ErrorMessage name="esiDispensary" />
                                </div>
                            </div>

                            <div>
                                <label className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block my-2">
                                    ESI on Overtime:
                                    <Field
                                        type="checkbox"
                                        name="esiOnOt"
                                        className="rounded w-4 h-4 accent-teal-600 mx-4 translate-y-0.5"
                                    />
                                </label>
                            </div>

                            <div>
                                <label
                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                                    htmlFor={"uanNumber"}
                                >
                                    UAN Number
                                </label>
                                <Field
                                    className={classNames(
                                        errors.uanNumber && touched.uanNumber
                                            ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                            : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                        "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full block"
                                    )}
                                    type="text"
                                    maxLength={50}
                                    name={"uanNumber"}
                                />
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    <ErrorMessage name="uanNumber" />
                                </div>
                            </div>
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
export default EmployeePfEsiDetail;
