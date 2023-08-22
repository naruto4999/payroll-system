import React, { useRef, useEffect, useState, useMemo, memo } from 'react';
import { FaUserPlus } from 'react-icons/fa6';
import { FaCircleNotch } from 'react-icons/fa6';
import { Field, ErrorMessage, Form } from 'formik';
import { useGetEmployeeShiftsQuery } from '../../../../authentication/api/employeeShiftsApiSlice';
import MonthDays from './MonthDay';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};
const isDateWithinRange = (date, fromDate, toDate) => {
	return date >= fromDate && date <= toDate;
};
const timeFormat = (time) => {
	const timeParts = time.split(':');
	const formattedTime = `${timeParts[0]}:${timeParts[1]}`;
	return formattedTime;
};

const EditEmployeeShift = memo(
	({
		handleSubmit,
		values,
		errors,
		isValid,
		touched,
		setFieldValue,
		globalCompany,
		cancelButtonClicked,
		isEditing,
		dirty,
		initialValues,
		updateEmployeeShiftId,
		dateOfJoining,
		shifts,
		setErrorMessage,
		errorMessage,
		setEmployeeShiftsFound,
		isSubmitting,
	}) => {
		// console.log(values);
		const {
			data: employeeShifts,
			isLoading: isLoadingEmployeeShifts,
			isSuccess: isEmployeeShiftsSuccess,
			isFetching: isFetchingEmployeeShifts,
		} = useGetEmployeeShiftsQuery(
			{
				employee: updateEmployeeShiftId,
				company: globalCompany.id,
				year: values.year,
			},
			{
				skip: updateEmployeeShiftId === null,
			}
		);
		console.log(employeeShifts);
		// console.log(values);
		// values.month is not zero based index, it starts from 1
		const firstDayOfMonth = new Date(values.year, values.month - 1, 1);
		const daysInMonth = new Date(values.year, values.month, 0).getDate();
		const dayArray = Array.from(
			{ length: daysInMonth },
			(_, index) => index + 1
		);
		const dayOfWeek = firstDayOfMonth.getDay();
		// console.log(dayOfWeek);
		const weekdays = [
			'Sunday',
			'Monday',
			'Tuesday',
			'Wednesday',
			'Thursday',
			'Friday',
			'Saturday',
		];

		const months = [
			'January',
			'February',
			'March',
			'April',
			'May',
			'June',
			'July',
			'August',
			'September',
			'October',
			'November',
			'December',
		];
		const currentDate = new Date();
		const options = [];

		for (
			let i = new Date(dateOfJoining).getFullYear();
			i <= currentDate.getFullYear();
			i++
		) {
			options.push(
				<option key={i} value={i}>
					{i}
				</option>
			);
		}

		useEffect(() => {
			setEmployeeShiftsFound(employeeShifts?.length != 0);
		}, [employeeShifts]);

		useEffect(() => {
			// Using isSubmitting to prevent setting field values when the form is submitting since this component will get rerendered using submission and useEffect runs for the first render so this is to prevent that scenerio
			if (isEmployeeShiftsSuccess && !isSubmitting) {
				const dateOfJoiningObj = new Date(dateOfJoining);
				if (
					dateOfJoiningObj.getFullYear() == values.year &&
					values.month - 1 < dateOfJoiningObj.getMonth()
				) {
					// console.log('yup me here');
					setFieldValue('month', dateOfJoiningObj.getMonth() + 1);
				}

				const daysInMonth = new Date(
					values.year,
					values.month,
					0
				).getDate();

				const updatedDayWiseShifts = {}; // Create an object to hold the shifts

				for (let date = 1; date <= daysInMonth; date++) {
					let calendarDate = new Date(
						Date.UTC(
							values.year,
							values.month - 1,
							date,
							0,
							0,
							0,
							0
						)
					);

					let foundShift = null;
					for (const shift of employeeShifts) {
						let fromDate = new Date(shift.fromDate);
						let toDate = new Date(shift.toDate);

						if (isDateWithinRange(calendarDate, fromDate, toDate)) {
							foundShift = shift;
							break; // Exit the loop if a matching shift is found
						}
					}

					if (foundShift) {
						updatedDayWiseShifts[date] = foundShift.shift.id;
					} else {
						updatedDayWiseShifts[date] = ''; // Set to empty string if no shift found
					}
				}

				// Update the form state after processing all shifts
				setFieldValue('dayWiseShifts', updatedDayWiseShifts);
			}
		}, [values.month, employeeShifts]);
		if (isLoadingEmployeeShifts) {
			return <></>;
		} else if (employeeShifts?.length === 0) {
			return (
				<>
					<h3 className="mx-auto text-xl font-bold text-redAccent-500 dark:text-redAccent-600">
						No Shifts for this Employee Found
					</h3>
					<p className="mx-auto text-base text-redAccent-500 dark:text-redAccent-600">
						Make sure you have selected a valid shift under
						"Professional Details" Tab in "Employee Entry"
					</p>
				</>
			);
		} else
			return (
				<>
					<div className="text-gray-900 dark:text-slate-100">
						<form
							action=""
							className="flex flex-col justify-center gap-2"
							onSubmit={handleSubmit}
						>
							<section>
								<label
									htmlFor="year"
									className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
								>
									Shift for month and year
								</label>
								<br />
								<Field
									as="select"
									name="month"
									className="my-1 mr-2 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
								>
									{months.map((month, index) => {
										const dateOfJoiningObj = new Date(
											dateOfJoining
										);
										if (
											values.year ==
												dateOfJoiningObj.getFullYear() &&
											index < dateOfJoiningObj.getMonth()
										) {
											return null; // Skip rendering months before dateOfJoiningMonth
										}
										return (
											<option
												key={index}
												value={index + 1}
											>
												{month}
											</option>
										);
									})}
								</Field>
								<Field
									as="select"
									name="year"
									className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
								>
									{options}
								</Field>
							</section>
							<section className="container grid max-w-full grid-cols-7 gap-1">
								{weekdays.map((weekday, index) => {
									return (
										<div
											key={index}
											className="w-full rounded-sm border border-slate-400 border-opacity-30"
										>
											<h2 className="mx-auto hidden w-fit font-bold sm:block">
												{weekday}
											</h2>
											<h2 className="mx-auto w-fit font-bold sm:hidden">
												{weekday.slice(0, 3)}
											</h2>
										</div>
									);
								})}
								{Array.from({ length: dayOfWeek }).map(
									(_, index) => (
										<div
											className="h-fit w-full"
											key={index}
										>
											{/* <MonthDays /> */}
										</div>
									)
								)}
								{dayArray.map((day) => (
									<div className="h-fit w-full" key={day}>
										<MonthDays
											day={day}
											shifts={shifts}
											shiftValue={
												values?.dayWiseShifts[day]
											}
											fieldName={`dayWiseShifts.${day}`}
										/>
										{/* {console.log(day)} */}
										{/* {values.dayWiseShifts[day]} */}
									</div>
								))}
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
									Update
								</button>
								<button
									type="button"
									className="w-20 rounded bg-zinc-400 p-2 text-base font-medium hover:bg-zinc-500 dark:bg-zinc-600 dark:hover:bg-zinc-700"
									onClick={() => {
										cancelButtonClicked(isEditing);
										setErrorMessage('');
									}}
								>
									Cancel
								</button>
							</section>
						</form>
					</div>
				</>
			);
	}
);
export default EditEmployeeShift;
