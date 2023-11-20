import { useRef, useEffect } from 'react';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};
import { FaCircleNotch } from 'react-icons/fa6';

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
}) => {
	// if (isSubmitting == undefined) {
	// 	let isSubmitting = false;
	// }
	console.log(errors);
	const inputRef = useRef(null);
	useEffect(() => {
		inputRef.current.focus();
	}, []);
	return (
		<div className="text-gray-900 dark:text-slate-100">
			<h1 className="mb-2 text-2xl font-medium">Bulk Update Attendance</h1>

			<form action="" className="flex flex-col justify-center gap-2">
				<label
					htmlFor="userInput"
					className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
				>
					Please type "confirm" to Bulk Update Attendances
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
						// onClick={() => {
						// 	setConfirmDelete({ id: '', phrase: '' });
						// 	setDeleteCompanyPopover(false);
						// }}
					>
						Cancel
					</button>
				</section>
			</form>
		</div>
	);
};

export default ConfirmationModal;
