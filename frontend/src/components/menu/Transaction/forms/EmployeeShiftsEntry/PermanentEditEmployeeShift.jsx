import React, { useRef, useEffect, useState, useMemo } from 'react';
import { FaUserPlus } from 'react-icons/fa6';
import { FaCircleNotch } from 'react-icons/fa6';
import { Field, ErrorMessage, Form } from 'formik';
import { useGetEmployeeShiftsQuery } from '../../../../authentication/api/employeeShiftsApiSlice';
import MonthDays from './MonthDay';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const timeFormat = (time) => {
	const timeParts = time.split(':');
	const formattedTime = `${timeParts[0]}:${timeParts[1]}`;
	return formattedTime;
};

const PermanentEditEmployeeShift = ({
	errorMessage,
	setErrorMessage,
	globalCompany,
	updateEmployeeShiftId,
	shifts,
	dateOfJoining,
	handleSubmit,
	errors,
	cancelButtonClicked,
	isValid,
}) => {
	console.log(errors);
	return (
		<>
			<div className="text-gray-900 dark:text-slate-100">
				<form
					action=""
					className="flex flex-col justify-center gap-2"
					onSubmit={handleSubmit}
				>
					<section className="flex flex-row justify-evenly gap-2">
						<div>
							<label
								htmlFor="fromDate"
								className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							>
								From Date
							</label>
							<Field
								className={classNames(
									errors?.employeeProfessionalDetail
										?.dateOfJoining &&
										touched?.employeeProfessionalDetail
											?.dateOfJoining
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'block w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="date"
								name="fromDate"
							/>
							<div className="mt-1 w-40 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="fromDate" />
							</div>
						</div>
						<div>
							<label
								className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
								htmlFor="shift"
							>
								Shift
							</label>
							<Field
								className=" block rounded-md bg-zinc-50 bg-opacity-50 p-1.5 dark:bg-zinc-700"
								name="shift"
								as="select"
							>
								<option value="">-- Select an option --</option>

								{shifts?.map((shift) => (
									<option key={shift.id} value={shift.id}>
										{shift.name}
										{` [${timeFormat(
											shift.beginningTime
										)} - ${timeFormat(shift.endTime)}]`}
									</option>
								))}
							</Field>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="shift" />
							</div>
						</div>
					</section>
					<section className="mx-auto mt-4 mb-2 flex flex-row gap-10">
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
							onClick={cancelButtonClicked}
						>
							Cancel
						</button>
					</section>
				</form>
			</div>
		</>
	);
};
export default PermanentEditEmployeeShift;
