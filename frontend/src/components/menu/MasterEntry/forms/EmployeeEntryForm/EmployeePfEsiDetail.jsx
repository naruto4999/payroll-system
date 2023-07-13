import { useRef, useEffect, useState } from "react";
import { FaUserPlus } from "react-icons/fa6";
import { FaPlus } from "react-icons/fa6";
import { Field, ErrorMessage, FieldArray } from "formik";

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
    familyNomineeDetailInitailValues,
}) => {
    console.log(values);
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
                                                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm mx-2"
                                                                    htmlFor={`familyNomineeDetail.${index}.esiBenefit`}
                                                                >
                                                                    Esi
                                                                </label>
                                                                <Field
                                                                    type="checkbox"
                                                                    name={`familyNomineeDetail.${index}.esiBenefit`}
                                                                    className="rounded w-4 h-4 accent-teal-600 mx-auto mt-2 block"
                                                                />
                                                            </div>

                                                            <div>
                                                                <label
                                                                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm mx-2"
                                                                    htmlFor={`familyNomineeDetail.${index}.pfBenefits`}
                                                                >
                                                                    Pf
                                                                </label>
                                                                <Field
                                                                    type="checkbox"
                                                                    name={`familyNomineeDetail.${index}.pfBenefits`}
                                                                    className="rounded w-4 h-4 accent-teal-600 mx-auto mt-2 block"
                                                                />
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
                                                                />
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
                                                                />
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
                                                                />
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
                                                                />
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
                                                                />
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
                                                                />
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
    }
};
export default EmployeePfEsiDetail;
