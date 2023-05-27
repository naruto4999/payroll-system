import { useRef, useEffect } from "react";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const AddDesignation = ({
    handleSubmit,
    handleChange,
    handleBlur,
    values,
    errors,
    setAddDesignationPopover,
    isValid,
}) => {
    console.log(isValid);
    const inputRef = useRef(null);
    useEffect(() => {
        inputRef.current.focus();
    }, []);
    return (
        <div className="text-gray-900 dark:text-slate-100">
            <h1 className="font-medium text-2xl mb-2">Add Designation</h1>

            <form
                action=""
                className="flex flex-col gap-2 justify-center"
                onSubmit={handleSubmit}
            >
                <label
                    htmlFor="comapny-name"
                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                >
                    Designation Name
                </label>
                <div className="relative">
                    <input
                        className={classNames(
                            isValid
                                ? "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25"
                                : "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75",
                            "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                        )}
                        type="text"
                        id="newDesignation"
                        name="newDesignation"
                        onChange={handleChange}
                        onBlur={handleBlur}
                        value={values.name}
                        ref={inputRef}
                    />
                    {isValid ? (
                        ""
                    ) : (
                        <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                            {errors.newDesignation}
                        </p>
                    )}
                </div>
            </form>
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
                    className="bg-zinc-400 hover:bg-zinc-500 dark:bg-zinc-600 rounded w-20 p-2 text-base font-medium dark:hover:bg-zinc-700"
                    onClick={() => setAddDesignationPopover(false)}
                >
                    Cancel
                </button>
            </section>
        </div>
    );
};
export default AddDesignation;
