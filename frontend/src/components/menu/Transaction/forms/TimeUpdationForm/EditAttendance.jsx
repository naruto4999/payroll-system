import React, { useRef, useEffect, useState, useMemo, memo } from 'react';
import { FaUserPlus } from 'react-icons/fa6';
import { FaCircleNotch } from 'react-icons/fa6';
import { Field, ErrorMessage, Form } from 'formik';
import { useGetEmployeeShiftsQuery } from '../../../../authentication/api/employeeShiftsApiSlice';
import AttendanceMonthDays from './AttendanceMonthDays';
import AttendanceHeader from './AttendanceHeader';

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

const EditAttendance = memo(
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
		updateEmployeeId,
		dateOfJoining,
		shifts,
		setErrorMessage,
		errorMessage,
		setEmployeeShiftsFound,
		isSubmitting,
		leaveGrades,
	}) => {
		console.log(values);
		const {
			data: employeeShifts,
			isLoading: isLoadingEmployeeShifts,
			isSuccess: isEmployeeShiftsSuccess,
			isFetching: isFetchingEmployeeShifts,
		} = useGetEmployeeShiftsQuery(
			{
				employee: updateEmployeeId,
				company: globalCompany.id,
				year: values.year,
			},
			{
				skip: updateEmployeeId === null,
			}
		);

		// Get the Value of Shift for a given date
		const getShift = (year, month, day) => {
			const targetDate = new Date(Date.UTC(year, month - 1, day));
			const foundShift = employeeShifts?.find((shiftObj) => {
				const fromDate = new Date(shiftObj.fromDate);
				const toDate = new Date(shiftObj.toDate);

				if (targetDate >= fromDate && targetDate <= toDate) {
					return true;
				}

				return false;
			});

			return foundShift ? foundShift.shift : null;
		};
		const daysInMonth = new Date(values.year, values.month, 0).getDate();
		const dayArray = Array.from(
			{ length: daysInMonth },
			(_, index) => index + 1
		);

		const getTimeParts = (timeString) => {
			const timeParts = timeString.split(':');
			const hours = parseInt(timeParts[0], 10);
			const minutes = parseInt(timeParts[1], 10);
			return { hours, minutes };
		};

		const getTimeInDateObj = (time, day) => {
			const timeParts = getTimeParts(time);
			return new Date(
				values.year,
				values.month - 1,
				parseInt(day),
				timeParts.hours,
				timeParts.minutes
			);
		};

		// Calculate Overtime for a particular day
		const calculateOvertime = (day) => {
			let manualIn = values.attendance[day].manualIn;
			let manualOut = values.attendance[day].manualOut;
			const shift = getShift(values.year, values.month, day);
			console.log(shift);
			let manualInObj;
			let manualOutObj;
			let overtime = 0;

			if (shift.beginningTime < shift.endTime) {
				const shiftBeginningTime = getTimeInDateObj(
					shift.beginningTime,
					day
				);
				const shiftEndTime = getTimeInDateObj(shift.endTime, day);
				console.log(shiftBeginningTime);

				// If manualIn < shift begin time (without date object one) and manualIn > "00:00":
				if (
					manualIn != '' &&
					manualIn < shift.beginningTime.slice(0, 5)
				) {
					manualInObj = getTimeInDateObj(manualIn, day);
					console.log('in upper if');
					console.log(manualInObj);
				}

				// else if manualIn > shift end time (withoud date object one) and manualIn < "00:00"
				else if (
					manualIn != '' &&
					manualIn > shift.endTime.slice(0, 5)
				) {
					manualInObj = getTimeInDateObj(manualIn, parseInt(day) - 1);
					console.log('in lower if');
					console.log(manualInObj);
				}
				// If manualOut > shift end time (without date object one) and manualOut < "00:00":
				if (manualOut != '' && manualOut > shift.endTime.slice(0, 5)) {
					console.log('inside manual out');
					manualOutObj = getTimeInDateObj(manualOut, day);
				} else if (
					manualOut != '' &&
					manualOut < shift.beginningTime.slice(0, 5)
				) {
					// console.log(manualOutObj);
					// console.log(shift.beginningTime.slice(0, 5));
					// console.log('inside manual out 2');
					// console.log(manualOut);

					manualOutObj = getTimeInDateObj(
						manualOut,
						parseInt(day) + 1
					);
					console.log(manualOutObj);
				}
				if (manualInObj != undefined) {
					console.log('existsssss');
					const timeDifferenceInMilliseconds =
						shiftBeginningTime - manualInObj;
					const timeDifferenceInMinutes =
						timeDifferenceInMilliseconds / (1000 * 60);
					if (
						timeDifferenceInMinutes > parseInt(shift.otBeginAfter)
					) {
						overtime += timeDifferenceInMinutes;
					}

					console.log(timeDifferenceInMinutes);
				}
				if (manualOutObj != undefined) {
					console.log('existsssss in else manual out');
					console.log(manualOutObj);
					const timeDifferenceInMilliseconds =
						manualOutObj - shiftEndTime;
					const timeDifferenceInMinutes =
						timeDifferenceInMilliseconds / (1000 * 60);
					if (
						timeDifferenceInMinutes > parseInt(shift.otBeginAfter)
					) {
						overtime += timeDifferenceInMinutes;
					}
				}
				// setFieldValue(`attendance.${day}.otMin`, overtime);
			} else if (shift.beginningTime > shift.endTime) {
				const shiftBeginningTime = getTimeInDateObj(
					shift.beginningTime,
					day
				);
				const shiftEndTime = getTimeInDateObj(
					shift.endTime,
					parseInt(day) + 1
				);
				// If manualIn < shift begin time (without date object) and manualIn > shift end time (without object):

				if (
					manualIn != '' &&
					manualIn < shift.beginningTime.slice(0, 5) &&
					manualIn > shift.endTime.slice(0, 5)
				) {
					manualInObj = getTimeInDateObj(manualIn, day);
				}

				// If manualOut > shift end time (without the date object one) and and manualOut < shift begin time (without the date object one):
				if (
					manualOut != '' &&
					manualOut > shift.endTime.slice(0, 5) &&
					manualOut < shift.beginningTime.slice(0, 5)
				) {
					manualOutObj = getTimeInDateObj(
						manualOut,
						parseInt(day) + 1
					);
				}
				if (manualInObj !== undefined) {
					console.log('existsssss in else');
					const timeDifferenceInMilliseconds =
						shiftBeginningTime - manualInObj;
					const timeDifferenceInMinutes =
						timeDifferenceInMilliseconds / (1000 * 60);
					if (
						timeDifferenceInMinutes > parseInt(shift.otBeginAfter)
					) {
						overtime += timeDifferenceInMinutes;
					}
				}
				if (manualOutObj !== undefined) {
					console.log('existsssss in else manual out');
					const timeDifferenceInMilliseconds =
						manualOutObj - shiftEndTime;
					const timeDifferenceInMinutes =
						timeDifferenceInMilliseconds / (1000 * 60);
					if (
						timeDifferenceInMinutes > parseInt(shift.otBeginAfter)
					) {
						overtime += timeDifferenceInMinutes;
					}
				}
			}
			return overtime;
		};

		// const calculateLateHrs = (day) => {
		// 	let manualIn = values.attendance[day]?.manualIn;

		// 	const shiftForCurrentDate = getShift(
		// 		values.year,
		// 		values.month,
		// 		day
		// 	);
		// 	const beginningTimeParts = getTimeParts(
		// 		shiftForCurrentDate.beginningTime
		// 	);
		// 	const shiftBeginningTime = new Date(
		// 		values.year,
		// 		values.month - 1,
		// 		parseInt(day),
		// 		beginningTimeParts.hours,
		// 		beginningTimeParts.minutes +
		// 			parseInt(shiftForCurrentDate.lateGrace)
		// 	);
		// 	console.log(beginningTimeParts.minutes);
		// 	const manualInParts = getTimeParts(manualIn);
		// 			let manualInObj = new Date(
		// 				values.year,
		// 				values.month - 1,
		// 				parseInt(day),
		// 				manualInParts.hours,
		// 				manualInParts.minutes
		// 			);
		// 	if (shiftBeginningTime)
		// };

		// useEffect(() => {
		// 	if (employeeShifts) {
		// 		for (const day in values.attendance) {
		// 			// const { manualIn, manualOut } = values.attendance[day];
		// 			const overtime = calculateOvertime(day);
		// 			if (overtime > 0) {
		// 				let otConsider = Math.floor(overtime / 30) * 30;
		// 				console.log(otConsider);
		// 				let remainingOt = overtime % 30;
		// 				if (remainingOt > 15) {
		// 					otConsider = otConsider + 30;
		// 				}
		// 				if (otConsider > 0) {
		// 					setFieldValue(
		// 						`attendance.${day}.otMin`,
		// 						otConsider
		// 					);
		// 				} else {
		// 					setFieldValue(`attendance.${day}.otMin`, '');
		// 				}
		// 			} else {
		// 				setFieldValue(`attendance.${day}.otMin`, '');
		// 			}
		// 			// calculateLateHrs(day);
		// 		}
		// 	}
		// }, [values.attendance]);

		useEffect(() => {
			let timeoutId;

			const calculateAndSetOvertime = () => {
				for (const day in values.attendance) {
					const overtime = calculateOvertime(day);
					if (overtime > 0) {
						let otConsider = Math.floor(overtime / 30) * 30;
						let remainingOt = overtime % 30;
						if (remainingOt > 15) {
							otConsider = otConsider + 30;
						}
						if (otConsider > 0) {
							setFieldValue(
								`attendance.${day}.otMin`,
								otConsider
							);
						} else {
							setFieldValue(`attendance.${day}.otMin`, '');
						}
					} else {
						setFieldValue(`attendance.${day}.otMin`, '');
					}
				}
			};

			if (employeeShifts) {
				// Clear previous timeout if any
				clearTimeout(timeoutId);

				// Set a new timeout for 1 second
				timeoutId = setTimeout(() => {
					calculateAndSetOvertime();
				}, 500);
			}

			// Clear the timeout when the component unmounts or when values.attendance changes
			return () => {
				clearTimeout(timeoutId);
			};
		}, [values.attendance]);

		if (isLoadingEmployeeShifts) {
			return <></>;
		} else {
			return (
				<>
					<div className="text-gray-900 dark:text-slate-100">
						<form
							action=""
							className="flex flex-row gap-2"
							onSubmit={handleSubmit}
						>
							<section className="w-fit">
								<AttendanceHeader />
								{dayArray.map((day) => {
									const shiftForCurrentDate = getShift(
										values.year,
										values.month,
										day
									);
									return (
										<AttendanceMonthDays
											day={day}
											key={day}
											year={values.year}
											month={values.month}
											shift={shiftForCurrentDate.name}
											leaveGrades={leaveGrades}
											otMin={values.attendance[day].otMin}
											lateMin={
												values.attendance[day].lateMin
											}
										/>
									);
								})}
							</section>
							<section className="mt-4 mb-2 flex w-fit flex-row gap-4">
								<button
									className={classNames(
										isValid
											? 'hover:bg-teal-600  dark:hover:bg-teal-600'
											: 'opacity-40',
										'h-10 w-20 rounded bg-teal-500 p-2 text-base font-medium dark:bg-teal-700'
									)}
									type="submit"
									disabled={!isValid}
									onClick={handleSubmit}
								>
									Update
								</button>
								<button
									type="button"
									className="h-10 w-20 rounded bg-zinc-400 p-2 text-base font-medium hover:bg-zinc-500 dark:bg-zinc-600 dark:hover:bg-zinc-700"
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
	}
);
export default EditAttendance;
