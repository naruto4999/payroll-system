import React, { useRef, useEffect, useState, useMemo, memo } from 'react';
import { FaUserPlus } from 'react-icons/fa6';
import { FaCircleNotch } from 'react-icons/fa6';
import { Field, ErrorMessage, Form } from 'formik';
import { useGetEmployeeShiftsQuery } from '../../../../authentication/api/employeeShiftsApiSlice';
import AttendanceMonthDays from './AttendanceMonthDays';
import AttendanceHeader from './AttendanceHeader';
import { useSelector } from 'react-redux';
import { useGetEmployeeAttendanceBetweenDatesQuery } from '../../../../authentication/api/timeUpdationApiSlice';
import { useGetWeeklyOffHolidayOffQuery } from '../../../../authentication/api/weeklyOffHolidayOffApiSlice';
import { useGetSingleEmployeeProfessionalDetailQuery } from '../../../../authentication/api/employeeEntryApiSlice';
import { useGetSingleEmployeeSalaryDetailQuery } from '../../../../authentication/api/employeeEntryApiSlice';

// After for the Beginnning is covered by late grace
const AUTO_SHIFT_BEGINNING_BUFFER_BEFORE = 10;
const AUTO_SHIFT_ENDING_BUFFER_BEFORE = 10;
const AUTO_SHIFT_ENDING_BUFFER_AFTER = 10;

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
		holidays,
	}) => {
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
		const weeklyOffValues = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'no_off'];

		const auth = useSelector((state) => state.auth);
		// console.log(values);
		const absent = useMemo(() => leaveGrades.find((grade) => grade.name === 'A'), [leaveGrades]);
		const missPunch = useMemo(() => leaveGrades.find((grade) => grade.name === 'MS'), [leaveGrades]);
		const present = useMemo(() => leaveGrades.find((grade) => grade.name === 'P'), [leaveGrades]);
		const weeklyOff = useMemo(() => leaveGrades.find((grade) => grade.name === 'WO'), [leaveGrades]);
		const weeklyOffSkip = useMemo(() => leaveGrades.find((grade) => grade.name === 'WO*'), [leaveGrades]);
		const holidayOff = useMemo(() => leaveGrades.find((grade) => grade.name === 'HD'), [leaveGrades]);
		const holidayOffSkip = useMemo(() => leaveGrades.find((grade) => grade.name === 'HD*'), [leaveGrades]);
		const compensationOff = useMemo(() => leaveGrades.find((grade) => grade.name === 'CO'), [leaveGrades]);
		const onDuty = useMemo(() => leaveGrades.find((grade) => grade.name === 'OD'), [leaveGrades]);

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
				skip: updateEmployeeId === null || undefined,
			}
		);

		const {
			data: employeeProfessionalDetail,
			isLoading: isLoadingEmployeeProfessionalDetail,
			isSuccess: isEmployeeProfessionalDetailSuccess,
			isFetching: isFetchingEmployeeProfessionalDetail,
		} = useGetSingleEmployeeProfessionalDetailQuery(
			{
				id: updateEmployeeId,
				company: globalCompany.id,
			},
			{
				skip: updateEmployeeId === null || undefined,
			}
		);

		const {
			data: employeeSalaryDetail,
			isLoading: isLoadingEmployeeSalaryDetail,
			isSuccess: isEmployeeSalaryDetailSuccess,
			isFetching: isFetchingEmployeeSalaryDetail,
		} = useGetSingleEmployeeSalaryDetailQuery(
			{
				id: updateEmployeeId,
				company: globalCompany.id,
			},
			{
				skip: updateEmployeeId === null || undefined,
			}
		);

		const giveWeeklyOffHolidayOff = (year, month, day, minDays, auto = false) => {
			if (employeeAttendance == undefined || employeeAttendance.length == 0) {
				return false;
			}

			const currentDate = new Date(year, month - 1, day);
			const sixDaysAgo = new Date(currentDate);
			sixDaysAgo.setDate(currentDate.getDate() - 6);

			let presentCount = 0;

			for (let i = 0; i < employeeAttendance.length; i++) {
				const attendanceDate = new Date(employeeAttendance[i].date);
				if (attendanceDate >= sixDaysAgo && attendanceDate <= currentDate) {
					// Check if employee was present in firstHalf or secondHalf
					// Fix this
					if (employeeAttendance[i].firstHalf || employeeAttendance[i].secondHalf) {
						presentCount++;
					}
				}
			}

			return presentCount >= minDays;
		};

		const {
			data: { company, ...weeklyOffHolidayOff } = {},
			isLoading,
			isSuccess,
			isError,
			error,
			isFetching,
		} = useGetWeeklyOffHolidayOffQuery(globalCompany.id);

		const datesToGet = () => {
			// Calculating fromDate
			let monthStart = new Date(Date.UTC(values.year, parseInt(values.month) - 1, 1 - 7));
			const utcFromYear = monthStart.getUTCFullYear();
			const utcFromMonth = monthStart.getUTCMonth() + 1; // Months are 0-based
			const utcFromDay = monthStart.getUTCDate();

			const utcFromDate = `${utcFromYear}-${utcFromMonth.toString().padStart(2, '0')}-${utcFromDay
				.toString()
				.padStart(2, '0')}`;

			const daysInMonth = new Date(values.year, values.month, 0).getDate();

			// Calculating toDate
			let monthEnd = new Date(Date.UTC(values.year, parseInt(values.month) - 1, daysInMonth + 7));

			const utcToYear = monthEnd.getUTCFullYear();
			const utcToMonth = monthEnd.getUTCMonth() + 1; // Months are 0-based
			const utcToDay = monthEnd.getUTCDate();

			const utcToDate = `${utcToYear}-${utcToMonth.toString().padStart(2, '0')}-${utcToDay
				.toString()
				.padStart(2, '0')}`;
			return { fromDate: utcFromDate, toDate: utcToDate };
		};

		const {
			data: employeeAttendance,
			isLoading: isLoadingEmployeeAttendance,
			isSuccess: isEmployeeAttendanceSuccess,
			isFetching: isFetchingEmployeeAttendance,
		} = useGetEmployeeAttendanceBetweenDatesQuery(
			{
				employee: updateEmployeeId,
				company: globalCompany.id,
				fromDate: datesToGet().fromDate,
				toDate: datesToGet().toDate,
			},
			{
				skip: updateEmployeeId === null,
			}
		);

		const employeeAttendanceMemoized = useMemo(
			() => (employeeAttendance ? employeeAttendance : ''),
			[employeeAttendance]
		);
		// console.log(employeeAttendanceMemoized);

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
		const sortedKeys = Object.keys(values.attendance)
			.map((key) => parseInt(key))
			.sort((a, b) => a - b);

		// Creating Year values from DOJ till now
		const currentDate = new Date();
		const options = [];
		for (let i = new Date(dateOfJoining).getFullYear(); i <= currentDate.getFullYear(); i++) {
			options.push(
				<option key={i} value={i}>
					{i}
				</option>
			);
		}

		const getTimeParts = (timeString) => {
			const timeParts = timeString.split(':');
			const hours = parseInt(timeParts[0], 10);
			const minutes = parseInt(timeParts[1], 10);
			return { hours, minutes };
		};

		const getTimeInDateObj = (time, day) => {
			const timeParts = getTimeParts(time);
			return new Date(values.year, values.month - 1, parseInt(day), timeParts.hours, timeParts.minutes);
		};

		// Calculate Overtime for a particular day

		const calculateWeeklyHolidayOvertime = (day) => {
			let overtime = 0;
			let manualIn = values.attendance[day].manualIn;
			let manualOut = values.attendance[day].manualOut;
			let manualInObj = getTimeInDateObj(manualIn, day);
			let manualOutObj = getTimeInDateObj(manualOut, manualIn < manualOut ? day : parseInt(day) + 1);
			// console.log(manualInObj);
			// console.log(manualOutObj);
			const timeDifferenceInMilliseconds = manualOutObj - manualInObj;
			const timeDifferenceInMinutes = timeDifferenceInMilliseconds / (1000 * 60);
			overtime += timeDifferenceInMinutes;
			return overtime;
		};

		const calculateOvertime = (day) => {
			let manualIn = values.attendance[day].manualIn;
			let manualOut = values.attendance[day].manualOut;
			const shift = getShift(values.year, values.month, day);
			let manualInObj;
			let manualOutObj;
			let overtime = 0;

			if (shift.beginningTime < shift.endTime) {
				const shiftBeginningTime = getTimeInDateObj(shift.beginningTime, day);
				const shiftEndTime = getTimeInDateObj(shift.endTime, day);
				// If manualIn < shift begin time (without date object one) and manualIn > "00:00":
				if (manualIn != '' && manualIn < shift.beginningTime.slice(0, 5)) {
					manualInObj = getTimeInDateObj(manualIn, day);
				}

				// else if manualIn > shift end time (withoud date object one) and manualIn < "00:00"
				else if (manualIn != '' && manualIn > shift.endTime.slice(0, 5)) {
					manualInObj = getTimeInDateObj(manualIn, parseInt(day) - 1);
					// console.log('in lower if');
				}
				// If manualOut > shift end time (without date object one) and manualOut < "00:00":
				if (manualOut != '' && manualOut > shift.endTime.slice(0, 5)) {
					manualOutObj = getTimeInDateObj(manualOut, day);
				} else if (manualOut != '' && manualOut < shift.beginningTime.slice(0, 5)) {
					manualOutObj = getTimeInDateObj(manualOut, parseInt(day) + 1);
				}
				if (manualInObj != undefined) {
					const timeDifferenceInMilliseconds = shiftBeginningTime - manualInObj;
					const timeDifferenceInMinutes = timeDifferenceInMilliseconds / (1000 * 60);
					if (timeDifferenceInMinutes > parseInt(shift.otBeginAfter)) {
						overtime += timeDifferenceInMinutes;
					}
				}
				if (manualOutObj != undefined) {
					// console.log('existsssss in else manual out');
					const timeDifferenceInMilliseconds = manualOutObj - shiftEndTime;
					const timeDifferenceInMinutes = timeDifferenceInMilliseconds / (1000 * 60);
					if (timeDifferenceInMinutes > parseInt(shift.otBeginAfter)) {
						overtime += timeDifferenceInMinutes;
					}
				}
				// setFieldValue(`attendance.${day}.otMin`, overtime);
			} else if (shift.beginningTime > shift.endTime) {
				const shiftBeginningTime = getTimeInDateObj(shift.beginningTime, day);
				const shiftEndTime = getTimeInDateObj(shift.endTime, parseInt(day) + 1);
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
					manualOutObj = getTimeInDateObj(manualOut, parseInt(day) + 1);
				}
				if (manualInObj !== undefined) {
					// console.log('existsssss in else');
					const timeDifferenceInMilliseconds = shiftBeginningTime - manualInObj;
					const timeDifferenceInMinutes = timeDifferenceInMilliseconds / (1000 * 60);
					if (timeDifferenceInMinutes > parseInt(shift.otBeginAfter)) {
						overtime += timeDifferenceInMinutes;
					}
				}
				if (manualOutObj !== undefined) {
					// console.log('existsssss in else manual out');
					const timeDifferenceInMilliseconds = manualOutObj - shiftEndTime;
					const timeDifferenceInMinutes = timeDifferenceInMilliseconds / (1000 * 60);
					if (timeDifferenceInMinutes > parseInt(shift.otBeginAfter)) {
						overtime += timeDifferenceInMinutes;
					}
				}
			}
			return overtime;
		};

		const calculateLateHrs = (day) => {
			let manualIn = values.attendance[day]?.manualIn;
			const shift = getShift(values.year, values.month, day);
			let manualInObj;
			let lateHrs = 0;

			if (shift.beginningTime < shift.endTime) {
				const shiftBeginningTime = getTimeInDateObj(shift.beginningTime, day);
				const shiftBeginningTimeWithGrace = new Date(
					shiftBeginningTime.getTime() + parseInt(shift.lateGrace) * 60 * 1000
				);
				const shiftEndTime = getTimeInDateObj(shift.endTime, day);
				// console.log(shiftBeginningTime);
				manualInObj = getTimeInDateObj(manualIn, day);
				if (manualInObj > shiftBeginningTimeWithGrace) {
					const timeDifferenceInMilliseconds = manualInObj - shiftBeginningTime;
					const timeDifferenceInMinutes = timeDifferenceInMilliseconds / (1000 * 60);
					lateHrs += timeDifferenceInMinutes;
				}
			}

			if (shift.beginningTime > shift.endTime) {
				// console.log('yessssssssssssssssssssss');
				const shiftBeginningTime = getTimeInDateObj(shift.beginningTime, day);
				const shiftBeginningTimeWithGrace = new Date(
					shiftBeginningTime.getTime() + parseInt(shift.lateGrace) * 60 * 1000
				);
				const shiftEndTime = getTimeInDateObj(shift.endTime, parseInt(day) + 1);
				if (manualIn > shift.beginningTime.slice(0, 5)) {
					manualInObj = getTimeInDateObj(manualIn, day);
					if (manualInObj > shiftBeginningTimeWithGrace) {
						const timeDifferenceInMilliseconds = manualInObj - shiftBeginningTime;
						const timeDifferenceInMinutes = timeDifferenceInMilliseconds / (1000 * 60);
						lateHrs += timeDifferenceInMinutes;
					}
				} else if (manualIn < shift.endTime.slice(0, 5)) {
					manualInObj = getTimeInDateObj(manualIn, parseInt(day) + 1);
					if (manualInObj > shiftBeginningTimeWithGrace) {
						const timeDifferenceInMilliseconds = manualInObj - shiftBeginningTime;
						const timeDifferenceInMinutes = timeDifferenceInMilliseconds / (1000 * 60);
						lateHrs += timeDifferenceInMinutes;
					}
				}
			}

			return lateHrs;
		};

		const calculateAttendance = (day, lateMinValue) => {
			const manualMode = values.attendance[day]?.manualMode;
			if (!manualMode) {
				const manualIn = values.attendance[day]?.manualIn;
				const manualOut = values.attendance[day]?.manualOut;
				const shift = getShift(values.year, values.month, day);
				const shiftBeginningTime = getTimeInDateObj(shift.beginningTime, day);
				const shiftEndTime = getTimeInDateObj(shift.endTime, day);
				const manualInObj =
					manualIn < shift.endTime.slice(0, 5)
						? getTimeInDateObj(manualIn, day)
						: getTimeInDateObj(
								manualIn,
								shift.beginningTime < shift.endTime ? parseInt(day) - 1 : parseInt(day) + 1
						  );
				const manualOutObj =
					manualOut > shift.beginningTime.slice(0, 5)
						? getTimeInDateObj(manualOut, day)
						: getTimeInDateObj(manualOut, shift.beginningTime < shift.endTime ? parseInt(day) + 1 : day);

				if (manualInObj && manualOutObj) {
					const effectiveStartTime = Math.max(manualInObj, shiftBeginningTime);
					const effectiveEndTime = Math.min(manualOutObj, shiftEndTime);
					const durationMilliseconds = Math.max(effectiveEndTime - effectiveStartTime, 0);
					const durationMinutes = Math.floor(durationMilliseconds / (1000 * 60));
					if (durationMinutes >= parseInt(shift.fullDayMinimumMinutes)) {
						if (lateMinValue <= shift.maxLateAllowedMin) {
							setFieldValue(`attendance.${day}.firstHalf`, present.id);
							setFieldValue(`attendance.${day}.secondHalf`, present.id);
						} else if (lateMinValue > shift.maxLateAllowedMin) {
							setFieldValue(`attendance.${day}.firstHalf`, absent.id);
							setFieldValue(`attendance.${day}.secondHalf`, present.id);
						}
					} else if (
						durationMinutes >= parseInt(shift.halfDayMinimumMinutes) &&
						durationMinutes < parseInt(shift.fullDayMinimumMinutes)
					) {
						if (lateMinValue <= shift.maxLateAllowedMin) {
							setFieldValue(`attendance.${day}.firstHalf`, present.id);
							setFieldValue(`attendance.${day}.secondHalf`, absent.id);
						} else if (lateMinValue > parseInt(shift.maxLateAllowedMin)) {
							// console.log('yes in correct one');
							setFieldValue(`attendance.${day}.firstHalf`, absent.id);
							setFieldValue(`attendance.${day}.secondHalf`, present.id);
						}
					} else if (durationMinutes < parseInt(shift.halfDayMinimumMinutes)) {
						setFieldValue(`attendance.${day}.firstHalf`, absent.id);
						setFieldValue(`attendance.${day}.secondHalf`, absent.id);
					}
				}
			}
		};

		const calculateFirstHalfSecondHalf = (day, type) => {
			let presentCount = 0;
			for (let i = 1; i <= 6; i++) {
				const previousDate = new Date(Date.UTC(values.year, values.month - 1, parseInt(day) - i));

				if (previousDate.getMonth() === values.month - 1) {
					const previousDay = previousDate.getDate();
					const attendance = values.attendance[previousDay];
					if (attendance.firstHalf === present.id || attendance.secondHalf === present.id) {
						presentCount += 1;
					}
				} else if (previousDate.getMonth() === values.month - 2) {
					for (const entry of employeeAttendance) {
						const entryDate = new Date(entry.date);
						if (previousDate.getTime() === entryDate.getTime()) {
							if (entry.firstHalf === present.id || entry.secondHalf === present.id) {
								presentCount += 1;
							}
						}
					}
				}

				if (
					(type === 'weeklyOff' && presentCount >= parseInt(weeklyOffHolidayOff.minDaysForWeeklyOff)) ||
					(type === 'holidayOff' && presentCount >= parseInt(weeklyOffHolidayOff.minDaysForHolidayOff))
				) {
					return true;
				}
			}

			return false;
		};

		useEffect(() => {
			let timeoutId;

			const performCalculations = () => {
				if (employeeProfessionalDetail && employeeSalaryDetail) {
					for (const day in values.attendance) {
						let weeklyOffDay = false;
						let holidayDay = false;
						// if (!values.attendance[day].manualMode) {
						const attendanceDay = new Date(Date.UTC(values.year, values.month - 1, day));

						const weeklyOffIndex = weeklyOffValues.indexOf(employeeProfessionalDetail.weeklyOff);
						const attendanceWeekday = attendanceDay.getDay();
						if (!values.attendance[day].manualMode) {
							if (attendanceWeekday === weeklyOffIndex) {
								weeklyOffDay = true;
								if (calculateFirstHalfSecondHalf(day, 'weeklyOff')) {
									setFieldValue(`attendance.${day}.firstHalf`, weeklyOff.id);
									setFieldValue(`attendance.${day}.secondHalf`, weeklyOff.id);
								} else {
									setFieldValue(`attendance.${day}.firstHalf`, weeklyOffSkip.id);
									setFieldValue(`attendance.${day}.secondHalf`, weeklyOffSkip.id);
								}
							}

							for (const holiday of holidays) {
								const holidayDate = new Date(holiday.date);

								if (holidayDate.getTime() === attendanceDay.getTime()) {
									holidayDay = true;
									if (calculateFirstHalfSecondHalf(day, 'holidayOff')) {
										setFieldValue(`attendance.${day}.firstHalf`, holidayOff.id);
										setFieldValue(`attendance.${day}.secondHalf`, holidayOff.id);
									} else {
										setFieldValue(`attendance.${day}.firstHalf`, holidayOffSkip.id);
										setFieldValue(`attendance.${day}.secondHalf`, holidayOffSkip.id);
									}
								}
							}
						}

						const attendance = values.attendance[day];
						const hasManualIn = attendance.manualIn !== '';
						const hasManualOut = attendance.manualOut !== '';
						const shift = getShift(values.year, values.month, day);

						if (hasManualIn && hasManualOut) {
							// Conditions for calculating Over Time
							if (employeeSalaryDetail.overtimeType != 'no_overtime') {
								let overtime;
								if (employeeSalaryDetail.overtimeType == 'all_days') {
									if (
										attendanceWeekday === weeklyOffIndex ||
										(values.attendance[day].manualMode &&
											(values.attendance[day].firstHalf == weeklyOff.id ||
												values.attendance[day].firstHalf == weeklyOffSkip.id ||
												values.attendance[day].firstHalf == holidayOff.id ||
												values.attendance[day].firstHalf == holidayOffSkip.id ||
												values.attendance[day].firstHalf == compensationOff.id) &&
											(values.attendance[day].secondHalf == weeklyOff.id ||
												values.attendance[day].secondHalf == weeklyOffSkip.id ||
												values.attendance[day].secondHalf == holidayOff.id ||
												values.attendance[day].secondHalf == holidayOffSkip.id ||
												values.attendance[day].secondHalf == compensationOff.id)) ||
										holidayDay
									) {
										overtime = calculateWeeklyHolidayOvertime(day);
									} else if (
										!values.attendance[day].manualMode ||
										((values.attendance[day].firstHalf == present.id ||
											values.attendance[day].firstHalf == onDuty.id) &&
											(values.attendance[day].secondHalf == present.id ||
												values.attendance[day].secondHalf == onDuty.id))
									) {
										// console.log('employee salary detail', employeeSalaryDetail);
										overtime = calculateOvertime(day);
									}
									setFieldValue(
										`attendance.${day}.otMin`,
										overtime > 0
											? Math.floor(overtime / 30) * 30 + (overtime % 30 > 15 ? 30 : 0)
											: ''
									);
								} else if (employeeSalaryDetail.overtimeType == 'holiday_weekly_off') {
									if (
										attendanceWeekday === weeklyOffIndex ||
										(values.attendance[day].manualMode &&
											(values.attendance[day].firstHalf == weeklyOff.id ||
												values.attendance[day].firstHalf == weeklyOffSkip.id ||
												values.attendance[day].firstHalf == holidayOff.id ||
												values.attendance[day].firstHalf == holidayOffSkip.id ||
												values.attendance[day].firstHalf == compensationOff.id) &&
											(values.attendance[day].secondHalf == weeklyOff.id ||
												values.attendance[day].secondHalf == weeklyOffSkip.id ||
												values.attendance[day].secondHalf == holidayOff.id ||
												values.attendance[day].secondHalf == holidayOffSkip.id ||
												values.attendance[day].secondHalf == compensationOff.id)) ||
										holidayDay
									) {
										overtime = calculateWeeklyHolidayOvertime(day);
										// console.log(overtime);
										setFieldValue(
											`attendance.${day}.otMin`,
											overtime > 0
												? Math.floor(overtime / 30) * 30 + (overtime % 30 > 15 ? 30 : 0)
												: ''
										);
									}
								}
							}

							// Conditions for calculating Late
							let lateHrs = 0;
							if (
								(!values.attendance[day].manualMode && !weeklyOffDay && !holidayDay) ||
								((values.attendance[day].firstHalf == present.id ||
									values.attendance[day].firstHalf == onDuty.id) &&
									(values.attendance[day].secondHalf == present.id ||
										values.attendance[day].secondHalf == onDuty.id))
							) {
								lateHrs = calculateLateHrs(day);
							}

							// Conditions for calculating attendance automatically
							if (!weeklyOffDay && !holidayDay && !values.attendance[day].manualMode) {
								// console.log(day, ' yes here');
								calculateAttendance(day, lateHrs);
							}

							setFieldValue(
								`attendance.${day}.lateMin`,
								lateHrs > 0 && lateHrs <= shift.maxLateAllowedMin ? lateHrs : ''
							);
						} else if (
							((hasManualIn && !hasManualOut) || (!hasManualIn && hasManualOut)) &&
							!weeklyOffDay &&
							!holidayDay &&
							!values.attendance[day].manualMode
						) {
							setFieldValue(`attendance.${day}.firstHalf`, missPunch.id);
							setFieldValue(`attendance.${day}.secondHalf`, missPunch.id);
						} else if (!hasManualIn && !hasManualOut) {
							setFieldValue(`attendance.${day}.otMin`, '');
							setFieldValue(`attendance.${day}.lateMin`, '');

							if (!holidayDay && !weeklyOffDay && !values.attendance[day].manualMode) {
								setFieldValue(`attendance.${day}.firstHalf`, absent.id);
								setFieldValue(`attendance.${day}.secondHalf`, absent.id);
							}
						}
					}
				}
			};

			if (employeeShifts && !isSubmitting) {
				clearTimeout(timeoutId);
				timeoutId = setTimeout(() => {
					performCalculations();
				}, 200);
			}

			return () => {
				clearTimeout(timeoutId);
			};
		}, [values.attendance, employeeProfessionalDetail, employeeSalaryDetail]);

		// Runs when fetch value of employeeAttendance changes
		useEffect(() => {
			if (!isSubmitting && employeeAttendance && employeeProfessionalDetail && isEmployeeAttendanceSuccess) {
				const daysInMonth = new Date(values.year, values.month, 0).getDate();
				const new_attendance = {};
				const weeklyOffIndex = weeklyOffValues.indexOf(employeeProfessionalDetail.weeklyOff);

				for (let day = 1; day <= daysInMonth; day++) {
					const attendanceDate = new Date(Date.UTC(values.year, values.month - 1, day));
					const attendanceWeekday = attendanceDate.getUTCDay();
					const matchingEmployeeAttendance = employeeAttendance.find(
						(entry) => new Date(entry.date).getTime() === attendanceDate.getTime()
					);

					new_attendance[day] = {
						machineIn: '',
						machineOut: '',
						manualIn: '',
						manualOut: '',
						firstHalf: absent.id,
						secondHalf: absent.id,
						otMin: '',
						lateMin: '',
						date: `${values.year}-${values.month}-${day}`,
						manualMode: false,
					};

					if (attendanceWeekday === weeklyOffIndex) {
						const isWeeklyOffHolidayOff = giveWeeklyOffHolidayOff(
							values.year,
							values.month,
							day,
							parseInt(weeklyOffHolidayOff.minDaysForWeeklyOff)
						);
						const weeklyOffId = isWeeklyOffHolidayOff ? weeklyOff.id : weeklyOffSkip.id;

						new_attendance[day].firstHalf = weeklyOffId;
						new_attendance[day].secondHalf = weeklyOffId;
					}

					for (const holiday of holidays) {
						const holidayDate = new Date(holiday.date);
						if (holidayDate.getTime() === attendanceDate.getTime()) {
							const isHolidayOff = giveWeeklyOffHolidayOff(
								values.year,
								values.month,
								day,
								parseInt(weeklyOffHolidayOff.minDaysForHolidayOff)
							);
							const holidayOffId = isHolidayOff ? holidayOff.id : holidayOffSkip.id;

							new_attendance[day].firstHalf = holidayOffId;
							new_attendance[day].secondHalf = holidayOffId;
						}
					}

					if (matchingEmployeeAttendance) {
						for (const key in matchingEmployeeAttendance) {
							if (matchingEmployeeAttendance.hasOwnProperty(key)) {
								new_attendance[day][key] =
									matchingEmployeeAttendance[key] === null ? '' : matchingEmployeeAttendance[key];
							}
						}
					}
				}

				setFieldValue('attendance', new_attendance);
			}
		}, [employeeAttendance, employeeProfessionalDetail, employeeSalaryDetail]);

		const getTimePart = (date) => {
			const hours = String(date.getHours()).padStart(2, '0');
			const minutes = String(date.getMinutes()).padStart(2, '0');

			return `${hours}:${minutes}`;
		};

		const AutoFillAttendance = () => {
			const manualFromDate = values.manualFromDate;
			const manualToDate = values.manualToDate;

			const daysInMonth = new Date(values.year, values.month, 0).getDate();
			const effectiveToDate = manualToDate < daysInMonth ? manualToDate : daysInMonth;

			for (let day = manualFromDate; day <= effectiveToDate; day++) {
				let skipThisDay = false;
				const autoFillDate = new Date(Date.UTC(values.year, parseInt(values.month) - 1, day));
				for (let i = 0; i < holidays.length; i++) {
					const holidayDate = new Date(holidays[i].date);
					if (autoFillDate.getTime() == holidayDate.getTime()) {
						skipThisDay = true;
						break;
					}
				}
				// console.log(skipThisDay, day);
				if (skipThisDay) {
					continue;
				}
				if (employeeProfessionalDetail) {
					const weeklyOffIndex = weeklyOffValues.indexOf(employeeProfessionalDetail?.weeklyOff);
					const autoFillDate = new Date(Date.UTC(values.year, values.month - 1, day)).getDay();
					if (autoFillDate == weeklyOffIndex) {
						continue;
					}
				}

				const shift = getShift(values.year, values.month, day);
				const shiftBeginningTime = getTimeInDateObj(shift.beginningTime, day);
				const shiftBeginningTimeMin = new Date(
					shiftBeginningTime.getTime() - AUTO_SHIFT_BEGINNING_BUFFER_BEFORE * 60 * 1000
				);
				const shiftBeginningTimeWithGrace = new Date(
					shiftBeginningTime.getTime() + parseInt(shift.lateGrace) * 60 * 1000
				);

				const randomBeginningTime =
					shiftBeginningTimeMin.getTime() +
					Math.random() * (shiftBeginningTimeWithGrace.getTime() - shiftBeginningTimeMin.getTime());

				const randomBeginningDate = new Date(randomBeginningTime);

				const shiftEndTime = getTimeInDateObj(shift.endTime, day);
				const shiftEndTimeMax = new Date(shiftEndTime.getTime() + AUTO_SHIFT_ENDING_BUFFER_AFTER * 60 * 1000);
				const shiftEndTimeMin = new Date(shiftEndTime.getTime() - AUTO_SHIFT_ENDING_BUFFER_BEFORE * 60 * 1000);

				const randomEndingTime =
					shiftEndTimeMin.getTime() + Math.random() * (shiftEndTimeMax.getTime() - shiftEndTimeMin.getTime());
				const randomEndingDate = new Date(randomEndingTime);

				setFieldValue(`attendance.${day}.manualIn`, getTimePart(randomBeginningDate));
				setFieldValue(`attendance.${day}.manualOut`, getTimePart(randomEndingDate));
			}
		};

		if (isLoadingEmployeeShifts || isLoadingEmployeeSalaryDetail || isLoadingEmployeeProfessionalDetail) {
			return <></>;
		} else {
			return (
				<>
					<div className="text-gray-900 dark:text-slate-100">
						<form action="" className="flex flex-row gap-2" onSubmit={handleSubmit}>
							<section className="w-fit">
								<AttendanceHeader />
								{sortedKeys.map((day) => {
									const shiftForCurrentDate = getShift(values.year, values.month, day);
									return (
										<AttendanceMonthDays
											day={day}
											key={day}
											year={values.year}
											month={values.month}
											shift={shiftForCurrentDate.name}
											leaveGrades={leaveGrades}
											otMin={values.attendance[day].otMin}
											lateMin={values.attendance[day].lateMin}
											holidays={holidays}
										/>
									);
								})}
							</section>
							<section className="flex w-full flex-col gap-4">
								<div>
									<label
										htmlFor="year"
										className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
									>
										Month and Year :
									</label>
									<Field
										as="select"
										name="month"
										className="my-1 mr-2 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
									>
										{months.map((month, index) => {
											const dateOfJoiningObj = new Date(dateOfJoining);
											if (
												values.year == dateOfJoiningObj.getFullYear() &&
												index < dateOfJoiningObj.getMonth()
											) {
												return null; // Skip rendering months before dateOfJoiningMonth
											}
											return (
												<option key={index} value={index + 1}>
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
								</div>
								<div className="flex flex-row justify-between">
									<section className="w-fit">
										<label
											className="mr-1 font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
											htmlFor="manualLeave"
										>
											Leave:
										</label>

										<Field
											as="select"
											id="manualLeave"
											name="manualLeave"
											className="rounded-md bg-zinc-50 bg-opacity-50 text-base dark:bg-zinc-700"
										>
											<option value="">N/A</option>
											{leaveGrades?.map((leaveGrade, index) => {
												return (
													<option key={index} value={leaveGrade.id}>
														{leaveGrade.name}
													</option>
												);
											})}
										</Field>
									</section>
									<section className="w-fit">
										<label
											className="mr-1 font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
											htmlFor="manualFromDate"
										>
											From:
										</label>

										<Field
											className={classNames(
												errors.manualFromDate && touched.manualFromDate
													? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
													: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
												'custom-number-input h-6 w-8 rounded border-2  bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
											)}
											type="number"
											name="manualFromDate"
											id="manualFromDate"
										/>
									</section>
									<section className="w-fit">
										<label
											className="mr-1 font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
											htmlFor="manualToDate"
										>
											To:
										</label>

										<Field
											className={classNames(
												errors.manualToDate && touched.manualToDate
													? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
													: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
												'custom-number-input h-6 w-8 rounded border-2  bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
											)}
											type="number"
											name="manualToDate"
											id="manualToDate"
										/>
									</section>
								</div>
								<div className="flex w-full flex-col">
									<button
										type="button"
										className="h-8 w-20 rounded bg-blueAccent-400 p-1 text-base font-medium hover:bg-blueAccent-500 dark:bg-blueAccent-700 dark:hover:bg-blueAccent-600"
										onClick={AutoFillAttendance}
									>
										Auto
									</button>
								</div>
								<div className="mt-4 mb-2 flex w-fit flex-row gap-4">
									<button
										className={classNames(
											isValid ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
											'h-10 w-fit rounded bg-teal-500 p-2 px-4 text-base font-medium dark:bg-teal-700'
										)}
										type="submit"
										disabled={!isValid}
										onClick={handleSubmit}
									>
										Update
										{isSubmitting && (
											<FaCircleNotch className="my-auto ml-2 inline animate-spin text-xl text-amber-700 dark:text-amber-600 " />
										)}
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
								</div>
							</section>
						</form>
					</div>
				</>
			);
		}
	}
);
export default EditAttendance;
