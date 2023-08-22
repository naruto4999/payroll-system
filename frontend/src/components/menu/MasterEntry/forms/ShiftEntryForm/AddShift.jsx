import { useRef, useEffect } from 'react';
import { Field, ErrorMessage } from 'formik';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const AddShift = ({
	handleSubmit,
	handleChange,
	handleBlur,
	values,
	errors,
	setAddShiftPopover,
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
			<h1 className="mb-2 text-2xl font-medium">Add Shift</h1>
			<form
				action=""
				className="flex flex-col justify-center gap-2"
				onSubmit={handleSubmit}
			>
				<section className="flex flex-row justify-center gap-4">
					<div className="w-full">
						<label
							htmlFor="shiftName"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Shift Name
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.shiftName && touched.shiftName
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
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
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.shiftName}
								</div>
							)}
							{errorMessage && (
								<p className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errorMessage}
								</p>
							)}
						</div>
						<label
							htmlFor="shiftBeginningTime"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Beginning Time
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.shiftBeginningTime &&
										touched.shiftBeginningTime
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
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
									<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
										{errors.shiftBeginningTime}
									</div>
								)}
						</div>

						<label
							htmlFor="shiftEndTime"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							End Time
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.shiftEndTime && touched.shiftEndTime
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="time"
								id="shiftEndTime"
								name="shiftEndTime"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.shiftEndTime}
							/>
							{errors.shiftEndTime && touched.shiftEndTime && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.shiftEndTime}
								</div>
							)}
						</div>

						<label
							htmlFor="lunchTime"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Lunch Time
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.lunchTime && touched.lunchTime
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="number"
								id="lunchTime"
								name="lunchTime"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.lunchTime}
							/>
							{errors.lunchTime && touched.lunchTime && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.lunchTime}
								</div>
							)}
						</div>

						<label
							htmlFor="teaTime"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Tea Time
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.teaTime && touched.teaTime
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="number"
								id="teaTime"
								name="teaTime"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.teaTime}
							/>
							{errors.teaTime && touched.teaTime && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.teaTime}
								</div>
							)}
						</div>

						<label
							htmlFor="lateGrace"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Late Grace
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.lateGrace && touched.lateGrace
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="number"
								id="lateGrace"
								name="lateGrace"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.lateGrace}
							/>
							{errors.lateGrace && touched.lateGrace && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.lateGrace}
								</div>
							)}
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
							<input
								className={classNames(
									errors.otBeginAfter && touched.otBeginAfter
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="number"
								id="otBeginAfter"
								name="otBeginAfter"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.otBeginAfter}
							/>
							{errors.otBeginAfter && touched.otBeginAfter && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.otBeginAfter}
								</div>
							)}
						</div>

						<label
							htmlFor="nextShiftDelay"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Next Shift Delay
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.nextShiftDelay &&
										touched.nextShiftDelay
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
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
									<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
										{errors.nextShiftDelay}
									</div>
								)}
						</div>

						<label
							htmlFor="accidentalPunchBuffer"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Accidental Punch Buffer
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.accidentalPunchBuffer &&
										touched.accidentalPunchBuffer
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
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
									<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
										{errors.accidentalPunchBuffer}
									</div>
								)}
						</div>

						<label
							htmlFor="halfDayMinimumMinutes"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Half Day Minimum Minutes
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.halfDayMinimumMinutes &&
										touched.halfDayMinimumMinutes
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
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
									<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
										{errors.halfDayMinimumMinutes}
									</div>
								)}
						</div>

						<label
							htmlFor="fullDayMinimumMinutes"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Full Day Minimum Minutes
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.fullDayMinimumMinutes &&
										touched.fullDayMinimumMinutes
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
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
									<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
										{errors.fullDayMinimumMinutes}
									</div>
								)}
						</div>

						<label
							htmlFor="shortLeaves"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Short Leaves
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.shortLeaves && touched.shortLeaves
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="number"
								id="shortLeaves"
								name="shortLeaves"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.shortLeaves}
							/>
							{errors.shortLeaves && touched.shortLeaves && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.shortLeaves}
								</div>
							)}
						</div>
					</div>
				</section>
				<section className="mt-4 mb-2 flex flex-row gap-4">
					<button
						className={classNames(
							isValid
								? 'hover:bg-teal-600  dark:hover:bg-teal-600'
								: 'opacity-40',
							'w-20 rounded bg-teal-500 p-2 text-base font-medium dark:bg-teal-700'
						)}
						type="submit"
						disabled={!isValid}
						onClick={handleSubmit}
					>
						Add
					</button>
					<button
						type="button"
						className="w-20 rounded bg-zinc-400 p-2 text-base font-medium hover:bg-zinc-500 dark:bg-zinc-600 dark:hover:bg-zinc-700"
						onClick={() => {
							setAddShiftPopover(false);
							setErrorMessage('');
						}}
					>
						Cancel
					</button>
				</section>
			</form>
		</div>
	);
};
export default AddShift;
