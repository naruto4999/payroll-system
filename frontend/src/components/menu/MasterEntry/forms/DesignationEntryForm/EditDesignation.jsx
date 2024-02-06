import { useRef, useEffect } from 'react';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const EditDesignation = ({
	handleSubmit,
	handleChange,
	handleBlur,
	values,
	errors,
	editDesignationPopoverHandler,
	isValid,
}) => {
	const inputRef = useRef(null);
	useEffect(() => {
		inputRef.current.focus();
	}, []);
	return (
		<div className="text-gray-900 dark:text-slate-100">
			<h1 className="mb-2 text-2xl font-medium">Edit Designation</h1>

			<form action="" className="flex flex-col justify-center gap-2" onSubmit={handleSubmit}>
				<label
					htmlFor="comapny-name"
					className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
				>
					Deparment Name
				</label>
				<div className="relative">
					<input
						className={classNames(
							isValid
								? 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25'
								: 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75',
							'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
						)}
						type="text"
						id="updatedDesignation"
						name="updatedDesignation"
						onChange={handleChange}
						onBlur={handleBlur}
						ref={inputRef}
					/>
					{isValid ? (
						''
					) : (
						<p className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
							{errors.updatedDesignation}
						</p>
					)}
				</div>
			</form>
			<section className="mt-4 mb-2 flex flex-row gap-4">
				<button
					className={classNames(
						isValid ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
						'w-20 rounded bg-teal-500 p-2 text-base font-medium dark:bg-teal-700'
					)}
					type="submit"
					disabled={!isValid}
					onClick={handleSubmit}
				>
					Update
				</button>
				<button
					className="w-20 rounded bg-zinc-400 p-2 text-base font-medium hover:bg-zinc-500 dark:bg-zinc-600 dark:hover:bg-zinc-700"
					onClick={() => editDesignationPopoverHandler({ id: '' })}
				>
					Cancel
				</button>
			</section>
		</div>
	);
};
export default EditDesignation;
