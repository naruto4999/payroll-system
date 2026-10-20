import { useRef, useEffect } from 'react';
import { FaCircleNotch } from 'react-icons/fa6';
import Button from './Button';

const ConfirmationModal = ({
    // deleteCompanyChangeHandler,
    // deleteButtonClicked,
    // setConfirmDelete,
    // setDeleteCompanyPopover,
    handleSubmit,
    handleChange,
    values,
    isValid,
    errors,
    isSubmitting,
    displayHeading,
    setShowConfirmModal,
}) => {
    console.log(errors);
    const inputRef = useRef(null);
    useEffect(() => {
        inputRef.current.focus();
    }, []);
    return (
        <div className="text-gray-900 dark:text-slate-100">
            <h1 className="mb-2 text-2xl font-medium">{`${displayHeading}`}</h1>

            <form onSubmit={handleSubmit} className="flex flex-col justify-center gap-2">
                <label
                    htmlFor="userInput"
                    className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
                >
                    {`Please type "Confirm" to ${displayHeading}`}
                </label>
                <div className="relative">
                    <input
                        className="w-full rounded border-2 border-gray-800  border-opacity-25 bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-700 dark:focus:border-opacity-75"
                        type="text"
                        id="userInput"
                        name="userInput"
                        placeholder=""
                        onChange={handleChange}
                        ref={inputRef}
                    />
                </div>
                {isValid ? (
                    ''
                ) : (
                    <p className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">{errors.userInput}</p>
                )}
                <section className="mt-4 mb-2 flex flex-row gap-4">
                    <Button size="sm" className="min-w-24" type="submit" disabled={isSubmitting}>
                        Confirm
                        {isSubmitting && <FaCircleNotch className="animate-spin" />}
                    </Button>
                    <Button size="sm" variant="secondary" disabled={isSubmitting} onClick={() => setShowConfirmModal(false)}>
                        Cancel
                    </Button>
                </section>
            </form>
        </div>
    );
};

export default ConfirmationModal;
