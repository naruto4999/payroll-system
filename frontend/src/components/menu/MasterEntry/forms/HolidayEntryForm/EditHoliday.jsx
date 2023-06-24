import { useRef, useEffect } from "react";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const EditHoliday = ({
    handleSubmit,
    handleChange,
    handleBlur,
    values,
    errors,
    editHolidayPopoverHandler,
    isValid,
    disableEdit,
    errorMessage,
    setErrorMessage,
    touched,
}) => {
    const inputRef = useRef(null);
    console.log(disableEdit);
    useEffect(() => {
        inputRef.current.focus();
    }, []);
    return (
        <div className="text-gray-900 dark:text-slate-100">
            <h1 className="font-medium text-2xl mb-2">Edit Holiday</h1>

            <form
                action=""
                className="flex flex-col gap-2 justify-center"
                onSubmit={handleSubmit}
            >
                <label
                    htmlFor="holiday-name"
                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                >
                    Holiday Name
                </label>
                <div className="relative">
                    <input
                        className={
                            disableEdit
                                ? classNames(
                                      "dark:text-slate-100 text-gray-900 text-opacity-50 dark:text-opacity-50  border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25 rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2 p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                  )
                                : classNames(
                                      errors.holidayName &&
                                          touched.holidayName
                                          ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                          : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                      "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                  )
                        }
                        type="text"
                        id="holidayName"
                        name="holidayName"
                        onChange={handleChange}
                        onBlur={handleBlur}
                        value={values.holidayName}
                        disabled={disableEdit}
                        ref={inputRef}
                    />
                    {errors.holidayName && touched.holidayName && (
                        <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                            {errors.holidayName}
                        </div>
                    )}
                    {errorMessage && (
                        <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                            {errorMessage}
                        </p>
                    )}
                </div>
                <label
                    htmlFor="holidayDate"
                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                >
                    Date
                </label>
                <div className="relative">
                    <input
                        className={classNames(
                            errors.holidayDate && touched.holidayDate
                                ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                            "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full custom-number-input"
                        )}
                        type="date"
                        id="holidayDate"
                        name="holidayDate"
                        onChange={handleChange}
                        onBlur={handleBlur}
                        value={values.holidayDate}
                    />
                    {errors.holidayDate && touched.holidayDate && (
                        <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                            {errors.holidayDate}
                        </div>
                    )}
                </div>

                <section className="flex flex-row gap-4 mt-4 mb-2">
                    <button
                        className="dark:bg-teal-700 rounded w-20 p-2 text-base font-medium bg-teal-500 dark:hover:bg-teal-600  hover:bg-teal-600"
                        type="submit"
                    >
                        Update
                    </button>
                    <button
                        type="button"
                        className="bg-zinc-400 hover:bg-zinc-500 dark:bg-zinc-600 rounded w-20 p-2 text-base font-medium dark:hover:bg-zinc-700"
                        onClick={() => {
                            editHolidayPopoverHandler({
                                id: "",
                                mandatory_holiday: false,
                            });
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
export default EditHoliday;
