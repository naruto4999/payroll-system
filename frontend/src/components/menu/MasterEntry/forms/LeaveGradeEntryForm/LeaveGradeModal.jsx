import { useRef, useEffect } from 'react';
import { Field, ErrorMessage } from 'formik';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const LeaveGradeModal = ({
	handleSubmit,
	values,
	errors,
	isValid,
	errorMessage,
	setErrorMessage,
	touched,
	setFieldValue,
	cancelButtonClicked,
	isEditing,
}) => {
	console.log(values);
	const inputRef = useRef(null);
	console.log(errorMessage);
	console.log(errors);
	useEffect(() => {
		inputRef.current.focus();
	}, []);

	useEffect(() => {
		if (values.paid == false) {
			setFieldValue('generateFrequency', '');
			setFieldValue('limit', '');
		}
	}, [values.paid]);

	return (
		<div className="text-gray-900 dark:text-slate-100">
			<h1 className="mb-2 text-2xl font-medium">Add Leave Grade</h1>

			<form
				action=""
				className="flex flex-col justify-center gap-2"
				onSubmit={handleSubmit}
			>
				<div>
					<label
						htmlFor="name"
						className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
					>
						Leave Grade Name
					</label>
					<div className="relative">
						<Field
							className={classNames(
								errors.name && touched.name
									? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
									: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
								'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
							)}
							type="text"
							id="name"
							name="name"
							innerRef={inputRef}
						/>
						<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
							<ErrorMessage name={'name'} />
						</div>
						{errorMessage && (
							<p className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								{errorMessage}
							</p>
						)}
					</div>
				</div>

				{/* <label>
					<Field type="checkbox" name="paid" />
					Paid
				</label> */}

				<label className="block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70">
					Paid:
					<Field
						type="checkbox"
						name="paid"
						className="mx-4 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
					/>
				</label>

				<div>
					<label
						htmlFor="limit"
						className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
					>
						Limit
					</label>
					<div className="relative">
						<Field
							className={classNames(
								errors.limit && touched.limit
									? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
									: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
								'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
							)}
							type="number"
							id="limit"
							name="limit"
							disabled={!values.paid}
						/>
						<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
							<ErrorMessage name={'limit'} />
						</div>
					</div>
				</div>

				<div>
					<label
						htmlFor="generateFrequency"
						className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
					>
						Generate Frequency
					</label>
					<div className="relative">
						<Field
							className={classNames(
								errors.generateFrequency &&
									touched.generateFrequency
									? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
									: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
								'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
							)}
							type="number"
							id="generateFrequency"
							name="generateFrequency"
							disabled={!values.paid}
						/>
						<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
							<ErrorMessage name={'generateFrequency'} />
						</div>
					</div>
				</div>

				<section className="mt-4 mb-2 flex flex-row gap-4">
					<button
						className={classNames(
							isValid
								? 'hover:bg-teal-600  dark:hover:bg-teal-600'
								: 'opacity-40',
							'w-20 rounded bg-teal-500 p-2 text-base font-medium dark:bg-teal-700'
						)}
						type="submit"
						onClick={handleSubmit}
						disabled={!isValid}
					>
						{isEditing ? 'Update' : 'Add'}
					</button>
					<button
						type="button"
						className="w-20 rounded bg-zinc-400 p-2 text-base font-medium hover:bg-zinc-500 dark:bg-zinc-600 dark:hover:bg-zinc-700"
						onClick={cancelButtonClicked}
					>
						Cancel
					</button>
				</section>
			</form>
		</div>
	);
};
export default LeaveGradeModal;
