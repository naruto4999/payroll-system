import { useRef, useEffect } from "react";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const AddLeaveGrade = ({
    handleSubmit,
    handleChange,
    handleBlur,
    values,
    errors,
    setAddLeaveGradePopover,
    isValid,
}) => {
    const inputRef = useRef(null);
    console.log(errors);
    useEffect(() => {
        inputRef.current.focus();
    }, []);
    return (
        <div className="text-gray-900 dark:text-slate-100">
            <h1 className="font-medium text-2xl mb-2">Add Leave Grade</h1>

            <form
                action=""
                className="flex flex-col gap-2 justify-center"
                onSubmit={handleSubmit}
            >
                <label
                    htmlFor="leaveGradeName"
                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                >
                    Leave Grade Name
                </label>
                <div className="relative">
                    <input
                        className={classNames(
                            errors.leaveGradeName
                                ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                            "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                        )}
                        type="text"
                        id="leaveGradeName"
                        name="leaveGradeName"
                        onChange={handleChange}
                        onBlur={handleBlur}
                        value={values.name}
                        ref={inputRef}
                    />
                    {errors.leaveGradeName ? (
                        <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                            {errors.leaveGradeName}
                        </p>
                    ) : (
                        ""
                    )}
                </div>
                <label
                    htmlFor="leaveGradeLimit"
                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                >
                    Limit
                </label>
                <div className="relative">
                    <input
                        className={classNames(
                            errors.leaveGradeLimit
                                ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                            "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                        )}
                        type="text"
                        id="leaveGradeLimit"
                        name="leaveGradeLimit"
                        onChange={handleChange}
                        onBlur={handleBlur}
                        value={values.name}
                    />
                    {errors.leaveGradeLimit ? (
                        <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                            {errors.leaveGradeLimit}
                        </p>
                    ) : (
                        ""
                    )}
                </div>

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
                        Add
                    </button>
                    <button
                        type="button"
                        className="bg-zinc-400 hover:bg-zinc-500 dark:bg-zinc-600 rounded w-20 p-2 text-base font-medium dark:hover:bg-zinc-700"
                        onClick={() => setAddLeaveGradePopover(false)}
                    >
                        Cancel
                    </button>
                </section>
            </form>
        </div>
    );
};
export default AddLeaveGrade;
