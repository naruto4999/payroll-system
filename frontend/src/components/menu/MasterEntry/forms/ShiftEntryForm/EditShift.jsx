import { useRef, useEffect } from "react";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const EditShift = ({
    handleSubmit,
    handleChange,
    handleBlur,
    values,
    errors,
    editShiftPopoverHandler,
    isValid,
    touched,
    errorMessage,
    setErrorMessage,
}) => {
    const inputRef = useRef(null);
    useEffect(() => {
        inputRef.current.focus();
    }, []);
    return (
        <div className="text-gray-900 dark:text-slate-100">
            <h1 className="font-medium text-2xl mb-2">Edit Shift</h1>
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
                                    errors.shiftName && touched.shiftName
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="text"
                                id="shiftName"
                                name="shiftName"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.shiftName}
                                ref={inputRef}
                            />
                            {errors.shiftName && touched.shiftName && (
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.shiftName}
                                </div>
                            )}
                            {errorMessage && (
                                <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errorMessage}
                                </p>
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
                                    errors.shiftBeginningTime &&
                                        touched.shiftBeginningTime
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="time"
                                id="shiftBeginningTime"
                                name="shiftBeginningTime"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.shiftBeginningTime}
                            />
                            {errors.shiftBeginningTime &&
                                touched.shiftBeginningTime && (
                                    <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                        {errors.shiftBeginningTime}
                                    </div>
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
                                    errors.shiftEndTime && touched.shiftEndTime
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="time"
                                id="shiftEndTime"
                                name="shiftEndTime"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.shiftEndTime}
                            />
                            {errors.shiftEndTime && touched.shiftEndTime && (
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.shiftEndTime}
                                </div>
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
                                    errors.lunchTime && touched.lunchTime
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="lunchTime"
                                name="lunchTime"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.lunchTime}
                            />
                            {errors.lunchTime && touched.lunchTime && (
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.lunchTime}
                                </div>
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
                                    errors.teaTime && touched.teaTime
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="teaTime"
                                name="teaTime"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.teaTime}
                            />
                            {errors.teaTime && touched.teaTime && (
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.teaTime}
                                </div>
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
                                    errors.lateGrace && touched.lateGrace
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="lateGrace"
                                name="lateGrace"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.lateGrace}
                            />
                            {errors.lateGrace && touched.lateGrace && (
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.lateGrace}
                                </div>
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
                                    errors.otBeginAfter && touched.otBeginAfter
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="otBeginAfter"
                                name="otBeginAfter"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.otBeginAfter}
                            />
                            {errors.otBeginAfter && touched.otBeginAfter && (
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.otBeginAfter}
                                </div>
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
                                    errors.nextShiftDelay &&
                                        touched.nextShiftDelay
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="nextShiftDelay"
                                name="nextShiftDelay"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.nextShiftDelay}
                            />
                            {errors.nextShiftDelay &&
                                touched.nextShiftDelay && (
                                    <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                        {errors.nextShiftDelay}
                                    </div>
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
                                    errors.accidentalPunchBuffer &&
                                        touched.accidentalPunchBuffer
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="accidentalPunchBuffer"
                                name="accidentalPunchBuffer"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.accidentalPunchBuffer}
                            />
                            {errors.accidentalPunchBuffer &&
                                touched.accidentalPunchBuffer && (
                                    <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                        {errors.accidentalPunchBuffer}
                                    </div>
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
                                    errors.halfDayMinimumMinutes &&
                                        touched.halfDayMinimumMinutes
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="halfDayMinimumMinutes"
                                name="halfDayMinimumMinutes"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.halfDayMinimumMinutes}
                            />
                            {errors.halfDayMinimumMinutes &&
                                touched.halfDayMinimumMinutes && (
                                    <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                        {errors.halfDayMinimumMinutes}
                                    </div>
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
                                    errors.fullDayMinimumMinutes &&
                                        touched.fullDayMinimumMinutes
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="fullDayMinimumMinutes"
                                name="fullDayMinimumMinutes"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.fullDayMinimumMinutes}
                            />
                            {errors.fullDayMinimumMinutes &&
                                touched.fullDayMinimumMinutes && (
                                    <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                        {errors.fullDayMinimumMinutes}
                                    </div>
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
                                    errors.shortLeaves && touched.shortLeaves
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="number"
                                id="shortLeaves"
                                name="shortLeaves"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.shortLeaves}
                            />
                            {errors.shortLeaves && touched.shortLeaves && (
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.shortLeaves}
                                </div>
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
                        Update
                    </button>
                    <button
                        type="button"
                        className="bg-zinc-400 hover:bg-zinc-500 dark:bg-zinc-600 rounded w-20 p-2 text-base font-medium dark:hover:bg-zinc-700"
                        onClick={() => {
                            editShiftPopoverHandler({ id: "" });
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
export default EditShift;
