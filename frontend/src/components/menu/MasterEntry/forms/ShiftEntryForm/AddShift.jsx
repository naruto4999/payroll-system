import { useRef, useEffect } from "react";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const AddShift = ({
    handleSubmit,
    handleChange,
    handleBlur,
    values,
    errors,
    setAddShiftPopover,
    isValid,
}) => {
    const inputRef = useRef(null);
    useEffect(() => {
        inputRef.current.focus();
    }, []);
    return (
        <div className="text-gray-900 dark:text-slate-100">
            <h1 className="font-medium text-2xl mb-2">Add Shift</h1>
            <form
                action=""
                className="flex flex-col gap-2 justify-center"
                onSubmit={handleSubmit}
            >
                <section className="flex flex-row justify-center gap-4">
                    <div className="w-full">
                        <label
                            htmlFor="shiftName"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Shift Name
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.shiftName
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="text"
                                id="shiftName"
                                name="shiftName"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.name}
                                ref={inputRef}
                            />
                            {errors.shiftName ? (
                                <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.shiftName}
                                </p>
                            ) : (
                                ""
                            )}
                        </div>
                        <label
                            htmlFor="shiftBeginningTime"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Beginning Time
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.shiftBeginningTime
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="time"
                                id="shiftBeginningTime"
                                name="shiftBeginningTime"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.name}
                            />
                            {errors.shiftBeginningTime ? (
                                <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.shiftBeginningTime}
                                </p>
                            ) : (
                                ""
                            )}
                        </div>

                        <label
                            htmlFor="shiftEndTime"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            End Time
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.shiftEndTime
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="time"
                                id="shiftEndTime"
                                name="shiftEndTime"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.name}
                            />
                            {errors.shiftEndTime ? (
                                <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.shiftEndTime}
                                </p>
                            ) : (
                                ""
                            )}
                        </div>

                        <label
                            htmlFor="lunchTime"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Lunch Time
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.lunchTime
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="lunchTime"
                                name="lunchTime"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.name}
                            />
                            {errors.lunchTime ? (
                                <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.lunchTime}
                                </p>
                            ) : (
                                ""
                            )}
                        </div>

                        <label
                            htmlFor="teaTime"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Tea Time
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.teaTime
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="teaTime"
                                name="teaTime"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.name}
                            />
                            {errors.teaTime ? (
                                <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.teaTime}
                                </p>
                            ) : (
                                ""
                            )}
                        </div>

                        <label
                            htmlFor="lateGrace"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Late Grace
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.lateGrace
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="lateGrace"
                                name="lateGrace"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.name}
                            />
                            {errors.lateGrace ? (
                                <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.lateGrace}
                                </p>
                            ) : (
                                ""
                            )}
                        </div>
                    </div>
                    <div className="w-full">
                        {/* second column */}
                        <label
                            htmlFor="otBeginAfter"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Over Time Begins After
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.otBeginAfter
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="otBeginAfter"
                                name="otBeginAfter"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.name}
                            />
                            {errors.otBeginAfter ? (
                                <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.otBeginAfter}
                                </p>
                            ) : (
                                ""
                            )}
                        </div>

                        <label
                            htmlFor="nextShiftDelay"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Next Shift Delay
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.nextShiftDelay
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="nextShiftDelay"
                                name="nextShiftDelay"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.name}
                            />
                            {errors.nextShiftDelay ? (
                                <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.nextShiftDelay}
                                </p>
                            ) : (
                                ""
                            )}
                        </div>

                        <label
                            htmlFor="accidentalPunchBuffer"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Accidental Punch Buffer
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.accidentalPunchBuffer
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="accidentalPunchBuffer"
                                name="accidentalPunchBuffer"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.name}
                            />
                            {errors.accidentalPunchBuffer ? (
                                <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.accidentalPunchBuffer}
                                </p>
                            ) : (
                                ""
                            )}
                        </div>

                        <label
                            htmlFor="halfDayMinimumMinutes"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Half Day Minimum Minutes
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.halfDayMinimumMinutes
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="halfDayMinimumMinutes"
                                name="halfDayMinimumMinutes"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.name}
                            />
                            {errors.halfDayMinimumMinutes ? (
                                <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.halfDayMinimumMinutes}
                                </p>
                            ) : (
                                ""
                            )}
                        </div>

                        <label
                            htmlFor="fullDayMinimumMinutes"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Full Day Minimum Minutes
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.fullDayMinimumMinutes
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="fullDayMinimumMinutes"
                                name="fullDayMinimumMinutes"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.name}
                            />
                            {errors.fullDayMinimumMinutes ? (
                                <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.fullDayMinimumMinutes}
                                </p>
                            ) : (
                                ""
                            )}
                        </div>

                        <label
                            htmlFor="shortLeaves"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Short Leaves
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.shortLeaves
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="shortLeaves"
                                name="shortLeaves"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.name}
                            />
                            {errors.shortLeaves ? (
                                <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.shortLeaves}
                                </p>
                            ) : (
                                ""
                            )}
                        </div>
                    </div>
                </section>
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
                        onClick={() => setAddShiftPopover(false)}
                    >
                        Cancel
                    </button>
                </section>
            </form>
        </div>
    );
};
export default AddShift;
