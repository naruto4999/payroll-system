import React from 'react';
import { useRef, useEffect } from 'react';
import { FaCircleNotch } from 'react-icons/fa6';

const classNames = (...classes) => {
    return classes.filter(Boolean).join(' ');
};

const InsertTotalEarnedModal = ({
    handleSubmit,
    handleChange,
    values,
    isValid,
    errors,
    isSubmitting,
    displayHeading,
    setShowInsertTotalEarnedModal,
}) => {
    console.log(errors);
    const inputRef = useRef(null);
    useEffect(() => {
        inputRef.current.focus();
    }, []);

    return (
        <div className="text-gray-900 dark:text-slate-100">
            <h1 className="mb-2 text-2xl font-medium">{`Total Earned Amount`}</h1>

            <form action="" className="flex flex-col justify-center gap-2">
                <label
                    htmlFor="manuallyInsertedTotalEarned"
                    className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
                >
                    {`Please Enter the Total Earned Amount`}
                    <div className="flex flex-row gap-2">
                        <div>
                            <p>Note: </p>
                        </div>
                        <div className="flex flex-col text-amber-500">
                            <p>1. Deductions are deducted from the entered amount.</p>
                            <p>2. Overtime is not marked on Weekly Off and Holiday Off.</p>
                            <p>
                                3. Max. Overtime for each day is{' '}
                                <span className="italic text-blueAccent-600"> 2 hrs </span>.
                            </p>
                            <p>
                                4. Total Earned Computed will be max.{' '}
                                <span className="italic text-blueAccent-600">entered_amount + 100 </span>or below that.
                            </p>
                        </div>
                    </div>
                </label>
                <div className="relative">
                    <input
                        className="custom-number-input w-full rounded border-2 border-gray-800  border-opacity-25 bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-700 dark:focus:border-opacity-75"
                        type="number"
                        id="manuallyInsertedTotalEarned"
                        name="manuallyInsertedTotalEarned"
                        placeholder=""
                        onChange={handleChange}
                        ref={inputRef}
                        disabled={isSubmitting}
                    />
                </div>
                {isValid ? (
                    ''
                ) : (
                    <p className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
                        {errors.manuallyInsertedTotalEarned}
                    </p>
                )}
                <section className="mt-4 mb-2 flex flex-row gap-4">
                    <button
                        className={classNames(
                            isValid && !isSubmitting ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
                            'w-24 rounded bg-teal-500 p-2 text-base font-medium dark:bg-teal-700'
                        )}
                        onClick={handleSubmit}
                        type="submit"
                        disabled={isSubmitting}
                    >
                        Confirm
                        <FaCircleNotch
                            className={classNames(isSubmitting ? '' : 'hidden', 'mx-2 inline animate-spin text-white')}
                        />
                    </button>
                    <button
                        className="w-20 rounded bg-zinc-400 p-2 text-base font-medium hover:bg-zinc-500 dark:bg-zinc-600 dark:hover:bg-zinc-700"
                        type="button"
                        onClick={() => {
                            setShowInsertTotalEarnedModal(false || isSubmitting);
                        }}
                    >
                        Cancel
                    </button>
                </section>
            </form>
        </div>
    );
};

export default InsertTotalEarnedModal;
