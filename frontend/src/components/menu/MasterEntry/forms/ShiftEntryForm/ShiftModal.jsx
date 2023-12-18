import { useRef, useEffect } from 'react';
import { Field, ErrorMessage } from 'formik';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const ShiftModal = ({
	handleSubmit,
	values,
	errors,
	setAddShiftPopover,
	isValid,
	touched,
	errorMessage,
	setErrorMessage,
	isEditing,
	cancelButtonClicked,
}) => {
	console.log(values);
	const inputRef = useRef(null);
	useEffect(() => {
		inputRef.current.focus();
	}, []);
	return (
		<div className="text-gray-900 dark:text-slate-100">
			<h1 className="mb-2 text-2xl font-medium">{isEditing ? 'Edit Shift' : 'Add Shift'}</h1>
			<form action="" className="flex flex-col justify-center gap-2" onSubmit={handleSubmit}>
				<section className="flex flex-row justify-center gap-4">
					<div className="w-full">
						<label
							htmlFor="name"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Shift Name
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
								<p className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">{errorMessage}</p>
							)}
						</div>

						<label
							htmlFor="beginningTime"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Beginning Time
						</label>
						<div className="relative">
							<Field
								className={classNames(
									errors.beginningTime && touched.beginningTime
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="time"
								id="beginningTime"
								name="beginningTime"
							/>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="beginningTime" />
							</div>
						</div>

						<label
							htmlFor="endTime"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							End Time
						</label>
						<div className="relative">
							<Field
								className={classNames(
									errors.endTime && touched.endTime
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="time"
								id="endTime"
								name="endTime"
							/>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="endTime" />
							</div>
						</div>

						<label
							htmlFor="lunchBeginningTime"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Lunch Beginning Time
						</label>
						<div className="relative">
							<Field
								className={classNames(
									errors.lunchBeginningTime && touched.lunchBeginningTime
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="time"
								id="lunchBeginningTime"
								name="lunchBeginningTime"
							/>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="lunchBeginningTime" />
							</div>
						</div>

						<label
							htmlFor="lunchDuration"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Lunch Duration
						</label>
						<div className="relative">
							<Field
								className={classNames(
									errors.lunchDuration && touched.lunchDuration
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="number"
								id="lunchDuration"
								name="lunchDuration"
							/>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="lunchDuration" />
							</div>
						</div>

						<label
							htmlFor="teaTime"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Tea Time
						</label>
						<div className="relative">
							<Field
								className={classNames(
									errors.teaTime && touched.teaTime
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="number"
								id="teaTime"
								name="teaTime"
							/>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="teaTime" />
							</div>
						</div>

						<label
							htmlFor="lateGrace"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Late Grace
						</label>
						<div className="relative">
							<Field
								className={classNames(
									errors.lateGrace && touched.lateGrace
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="number"
								id="lateGrace"
								name="lateGrace"
							/>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="lateGrace" />
							</div>
						</div>
					</div>
					<div className="w-full">
						{/* second column */}
						<label
							htmlFor="otBeginAfter"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Over Time Begins After
						</label>
						<div className="relative">
							<Field
								className={classNames(
									errors.otBeginAfter && touched.otBeginAfter
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="number"
								id="otBeginAfter"
								name="otBeginAfter"
							/>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="otBeginAfter" />
							</div>
						</div>

						<label
							htmlFor="nextShiftDelay"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Next Shift Delay
						</label>
						<div className="relative">
							<Field
								className={classNames(
									errors.nextShiftDelay && touched.nextShiftDelay
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="number"
								id="nextShiftDelay"
								name="nextShiftDelay"
							/>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="nextShiftDelay" />
							</div>
						</div>

						<label
							htmlFor="accidentalPunchBuffer"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Accidental Punch Buffer
						</label>
						<div className="relative">
							<Field
								className={classNames(
									errors.accidentalPunchBuffer && touched.accidentalPunchBuffer
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="number"
								id="accidentalPunchBuffer"
								name="accidentalPunchBuffer"
							/>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="accidentalPunchBuffer" />
							</div>
						</div>

						<label
							htmlFor="halfDayMinimumMinutes"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Half Day Minimum Minutes
						</label>
						<div className="relative">
							<Field
								className={classNames(
									errors.halfDayMinimumMinutes && touched.halfDayMinimumMinutes
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="number"
								id="halfDayMinimumMinutes"
								name="halfDayMinimumMinutes"
							/>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="halfDayMinimumMinutes" />
							</div>
						</div>

						<label
							htmlFor="fullDayMinimumMinutes"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Full Day Minimum Minutes
						</label>
						<div className="relative">
							<Field
								className={classNames(
									errors.fullDayMinimumMinutes && touched.fullDayMinimumMinutes
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="number"
								id="fullDayMinimumMinutes"
								name="fullDayMinimumMinutes"
							/>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="fullDayMinimumMinutes" />
							</div>
						</div>

						<label
							htmlFor="maxLateAllowedMin"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							{'Max late allowed Minutes'}
						</label>
						<div className="relative">
							<Field
								className={classNames(
									errors.maxLateAllowedMin && touched.maxLateAllowedMin
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="number"
								id="maxLateAllowedMin"
								name="maxLateAllowedMin"
							/>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="maxLateAllowedMin" />
							</div>
						</div>

						<label
							htmlFor="shortLeaves"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Short Leaves
						</label>
						<div className="relative">
							<Field
								className={classNames(
									errors.shortLeaves && touched.shortLeaves
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="number"
								id="shortLeaves"
								name="shortLeaves"
							/>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="shortLeaves" />
							</div>
						</div>
					</div>
				</section>
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
export default ShiftModal;
