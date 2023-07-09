import { useRef, useEffect, useState } from "react";
import { FaUserPlus } from "react-icons/fa6";
import { useGetEarningsHeadsQuery } from "../../../../authentication/api/earningsHeadEntryApiSlice";
import { FaCircleNotch } from "react-icons/fa6";
import { Field, getIn } from "formik";

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
}) => {
    const {
        data: fetchedEarningsHeads,
        isLoading,
        isSuccess,
        isError,
        error,
        isFetching,
        refetch,
    } = useGetEarningsHeadsQuery(globalCompany);
    console.log(errors);
    console.log(touched);
    console.log(values);

    // const ErrorMessage = ({ name }) => (
    //     <Field
    //         className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold"
    //         name={name}
    //     >
    //         {({}) => {
    //             const error = getIn(errors, name);
    //             const touch = getIn(touched, name);
    //             return touch && error ? error : null;
    //         }}
    //     </Field>
    // );
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
                        {Object.keys(initialValues.earningsHead).map((key) => (
                            <div key={key}>
                                <label
                                    htmlFor={key}
                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                                >
                                    {key}
                                </label>
                                <div className="relative">
                                    {/* <input
                                        className={classNames(
                                            getIn(errors, key) &&
                                                getIn(touched, key)
                                                ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                                : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                            "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                        )}
                                        type="number"
                                        id={key}
                                        name={key}
                                        onChange={handleChange}
                                        onBlur={handleBlur}
                                        value={values[key]}
                                    /> */}
                                    <Field
                                        className={classNames(
                                            errors.earningsHead?.[key]
                                                ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                                : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                            "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full custom-number-input"
                                        )}
                                        type="number"
                                        name={`earningsHead.${key}`}
                                    />

                                    {/* {getIn(errors, `key`) && (
                                        <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                            hahahahah
                                        </div>
                                    )} */}
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="w-fit"></div>
                </section>
                {errorMessage && errorMessage.error && (
                    <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                        {errorMessage.error}
                    </p>
                )}

                <section className="flex flex-row gap-4 mt-4 mb-2">
                    <button
                        className={classNames(
                            isValid && dirty
                                ? "dark:hover:bg-teal-600  hover:bg-teal-600"
                                : "opacity-40",
                            "dark:bg-teal-700 rounded w-20 p-2 text-base font-medium bg-teal-500"
                        )}
                        type="submit"
                        disabled={!isValid || !dirty}
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
};
export default EmployeeSalaryDetail;
