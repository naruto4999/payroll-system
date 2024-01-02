import React, { useEffect, useMemo, useState, useCallback, useRef } from 'react';
import {
	// column,
	createColumnHelper,
	flexRender,
	getCoreRowModel,
	useReactTable,
	getSortedRowModel,
	// columnFiltersState,
	getFilteredRowModel,
	// filterFn,
	// filterFns,
} from '@tanstack/react-table';
// import EmployeeTable from './EmployeeTable';

import { rankItem } from '@tanstack/match-sorter-utils';
import { FaRegTrashAlt, FaPen, FaAngleUp, FaAngleDown, FaEye } from 'react-icons/fa';
import { useGetEmployeePersonalDetailsQuery } from '../../../../authentication/api/employeeEntryApiSlice';
import {
	useAddEmployeeAttendanceMutation,
	useUpdateEmployeeAttendanceMutation,
} from '../../../../authentication/api/timeUpdationApiSlice';

import { useOutletContext } from 'react-router-dom';
import ReactModal from 'react-modal';
import { Formik } from 'formik';
import { useDispatch, useSelector } from 'react-redux';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import EditAttendance from './EditAttendance';
import { useGetLeaveGradesQuery } from '../../../../authentication/api/leaveGradeEntryApiSlice';
import * as yup from 'yup';
import { useGetWeeklyOffHolidayOffQuery } from '../../../../authentication/api/weeklyOffHolidayOffApiSlice';
import { useGetHolidaysQuery } from '../../../../authentication/api/holidayEntryApiSlice';
import { TimeUpdationSchema } from './TimeUpdationSchema';
// import createValidationSchema from './EmployeeShiftsSchema';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const isDateWithinRange = (date, fromDate, toDate) => {
	return date >= fromDate && date <= toDate;
};

const TimeUpdationForm = () => {
	const dispatch = useDispatch();
	const globalCompany = useSelector((state) => state.globalCompany);

	const {
		data: leaveGrades,
		isLoading: isLoadingLeaveGrades,
		isSuccess: isLeaveGradesSuccess,
		// isError,
		// error,
		// isFetching,
		// refetch,
	} = useGetLeaveGradesQuery(globalCompany);

	const {
		data: { company, ...weeklyOffHolidayOff } = {},
		isLoading,
		isSuccess,
		isError,
		error,
		isFetching,
	} = useGetWeeklyOffHolidayOffQuery(globalCompany.id);

	const {
		data: holidays,
		isLoading: isLoadingHolidays,
		isSuccess: isLoadingHolidaysSuccess,
	} = useGetHolidaysQuery(globalCompany);

	const [showLoadingBar, setShowLoadingBar] = useOutletContext();
	const {
		data: employeePersonalDetails,
		isLoading: isLoadingEmployeePersonalDetails,
		isSuccess: isSuccessEmployeePersonalDetails,
	} = useGetEmployeePersonalDetailsQuery(globalCompany);

	const [dateOfJoining, setDateOfJoining] = useState(null);
	const [errorMessage, setErrorMessage] = useState('');
	const [updateEmployeeId, setUpdateEmployeeId] = useState(null);
	const [
		addEmployeeAttendance,
		{
			isLoading: isAddingEmployeeAttendance,
			// isError: errorRegisteringRegular,
			isSuccess: isAddEmployeeAttendanceSuccess,
		},
	] = useAddEmployeeAttendanceMutation();
	const [
		updateEmployeeAttendance,
		{
			isLoading: isUpdatingEmployeeAttendance,
			// isError: errorRegisteringRegular,
			isSuccess: isUpdateEmployeeAttendanceSuccess,
		},
	] = useUpdateEmployeeAttendanceMutation();

	const [isTableFilterInputFocused, setIsTableFilterInputFocused] = useState(false);
	const [firstRender, setFirstRender] = useState(true);

	// const [columnFilters, setColumnFilters] = useState([{ id: 'paycode', value: { month: 8, year: 2023 } }]);

	// const columnFilters = useMemo(() => [{ id: 'paycode', value: { month: 8, year: 2023 } }]);

	const [globalFilter, setGlobalFilter] = useState('');

	const updateButtonClicked = async (values, formikBag) => {
		const employee_attendance = [];
		for (const day in values.attendance) {
			if (values.attendance.hasOwnProperty(day)) {
				employee_attendance.push({ ...values.attendance[day] });
			}
		}
		employee_attendance.map((each_attendance) => {
			each_attendance.company = globalCompany.id;
			each_attendance.employee = updateEmployeeId;
			if (each_attendance.machineIn == '') {
				each_attendance.machineIn = null;
			}
			if (each_attendance.otMin == '') {
				each_attendance.otMin = null;
			}
			if (each_attendance.lateMin == '') {
				each_attendance.lateMin = null;
			}
			if (each_attendance.machineOut == '') {
				each_attendance.machineOut = null;
			}
			if (each_attendance.manualIn == '') {
				each_attendance.manualIn = null;
			}
			if (each_attendance.manualOut == '') {
				each_attendance.manualOut = null;
			}
		});
		let toSend = {};
		toSend.employee_attendance = employee_attendance;
		toSend.employee = updateEmployeeId;
		toSend.company = globalCompany.id;

		try {
			if (employee_attendance[0].hasOwnProperty('id')) {
				const data = await updateEmployeeAttendance(toSend).unwrap();
			} else {
				const data = await addEmployeeAttendance(toSend).unwrap();
			}

			dispatch(
				alertActions.createAlert({
					message: 'Saved',
					type: 'Success',
					duration: 3000,
				})
			);
		} catch (err) {
			console.log(err);
			dispatch(
				alertActions.createAlert({
					message: 'Error Occurred',
					type: 'Error',
					duration: 5000,
				})
			);
		}
	};

	const [editTimeUpdationPopover, setEditTimeUpdationPopover] = useState(false);

	const generateInitialValues = () => {
		const currentDate = new Date();
		const currentYear = currentDate.getFullYear();
		// get method returns a zero-based index for the month
		const currentMonthIndex = currentDate.getMonth();
		const daysInMonth = new Date(currentYear, currentMonthIndex + 1, 0).getDate();
		// console.log(daysInMonth);

		const initialValues = {
			year: currentYear,
			month: currentMonthIndex + 1,
			manualLeave: '',
			manualFromDate: '',
			manualToDate: '',
			attendance: {},
			machineAttendanceUpload: '',
			allEmployeesMachineAttendance: false,
		};

		for (let day = 1; day <= daysInMonth; day++) {
			initialValues.attendance[day] = {
				machineIn: '',
				machineOut: '',
				manualIn: '',
				manualOut: '',
				firstHalf: '',
				secondHalf: '',
				otMin: '',
				lateMin: '',
				date: `${initialValues.year}-${initialValues.month}-${day}`,
				manualMode: false,
			};
		}
		return initialValues;
	};
	const initialValues = useMemo(() => generateInitialValues(), []);
	const columnHelper = createColumnHelper();

	const columns = [
		columnHelper.accessor('paycode', {
			header: () => 'PC',
			cell: (props) => props.renderValue(),
			//   footer: props => props.column.id,
			// filterFn: 'fuzzy',
		}),
		columnHelper.accessor('attendanceCardNo', {
			header: () => 'ACN',
			cell: (props) => props.renderValue(),
			//   footer: props => props.column.id,
		}),

		columnHelper.accessor('name', {
			header: () => 'Employee Name',
			cell: (props) => props.renderValue(),
			//   footer: info => info.column.id,
		}),
		columnHelper.accessor('designation', {
			header: () => 'Designation',
			cell: (props) => props.renderValue(),
			//   footer: info => info.column.id,
		}),
		columnHelper.accessor('dateOfJoining', {
			header: () => 'DOJ',
			cell: (props) => props.renderValue(),
			// enableHiding: true,
			enableGlobalFilter: false,
		}),
		columnHelper.accessor('resignationDate', {
			header: () => 'Resign Date',
			cell: (props) => props.renderValue(),
			enableHiding: true,
			enableGlobalFilter: false,
		}),
	];

	const tbodyRef = useRef(null);

	const [selectedDate, setSelectedDate] = useState({
		year: new Date().getFullYear(),
		month: new Date().getMonth() + 1,
	});
	const data = useMemo(() => {
		if (!employeePersonalDetails) return [];

		const filteredData = employeePersonalDetails.filter((employee) => {
			const comparisonDate = new Date(Date.UTC(selectedDate.year, parseInt(selectedDate.month) - 1, 1));
			// Extract the year and month from the original dateOfJoining
			// console.log(employee);
			if (employee.dateOfJoining) {
				const [year, month] = employee.dateOfJoining.split('-').map(Number);
				if (employee.resignationDate) {
					const [resignYear, resignMonth] = employee.resignationDate.split('-').map(Number);
					const resignDate = new Date(Date.UTC(resignYear, resignMonth, 0));
					if (resignDate < comparisonDate) {
						return false;
					}
				}

				// Create a new date with the same year and month but set day to 1
				const newDateOfJoining = new Date(Date.UTC(year, month - 1, 1));

				// Compare the new date with "2023-08-01"

				// Include the object if the new date is less than the comparison date
				return newDateOfJoining <= comparisonDate;
			} else {
				return false;
			}
		});

		return filteredData;
	}, [employeePersonalDetails, selectedDate]);

	const table = useReactTable({
		data,
		columns,
		filterFns: {
			// fuzzy: dojResignFilter,
		},
		initialState: {
			sorting: [{ id: 'name', desc: false }],
			columnVisibility: { dateOfJoining: true, resignationDate: false },
		},
		state: {
			globalFilter,
			// columnFilters,
		},
		// filterFns: {
		// 	fuzzy: dojResignFilter,
		// },
		onGlobalFilterChange: setGlobalFilter,
		// onColumnFiltersChange: setColumnFilters,

		getCoreRowModel: getCoreRowModel(),
		getSortedRowModel: getSortedRowModel(),
		getFilteredRowModel: getFilteredRowModel(),
		enableSortingRemoval: false,
		// globalFilterFn: globalFuzzyFilter,
	});
	const focusedRowRef = useRef(null);
	let debouncedSetUpdateEmployeeId;

	const onRowClick = (event, row) => {
		const currentRow = tbodyRef.current?.children.namedItem(row.id);
		clearTimeout(debouncedSetUpdateEmployeeId); // Clear the debounce timer
		debouncedSetUpdateEmployeeId = setTimeout(() => {
			focusedRowRef.current = currentRow.getAttribute('id');
			setUpdateEmployeeId(row.original.id);
		}, 300);
	};

	const handleKeyDown = (event, row) => {
		event.stopPropagation();
		event.preventDefault();
		const currentRow = tbodyRef.current?.children.namedItem(row.id);

		switch (event.key) {
			case 'ArrowUp':
				const previousRow = currentRow?.previousElementSibling;
				if (previousRow) {
					previousRow.focus();

					// setUpdateEmployeeId(previousRow?.getAttribute('data-row-id'));
					clearTimeout(debouncedSetUpdateEmployeeId); // Clear the debounce timer
					debouncedSetUpdateEmployeeId = setTimeout(() => {
						focusedRowRef.current = previousRow?.getAttribute('id');
						setUpdateEmployeeId(previousRow?.getAttribute('data-row-id'));
					}, 300);
				}
				break;
			case 'ArrowDown':
				// currentRow?.nextElementSibling?.focus();

				const nextRow = currentRow?.nextElementSibling;
				if (nextRow) {
					nextRow.focus();

					// setUpdateEmployeeId(nextRow?.getAttribute('data-row-id'));
					clearTimeout(debouncedSetUpdateEmployeeId); // Clear the debounce timer
					debouncedSetUpdateEmployeeId = setTimeout(() => {
						focusedRowRef.current = nextRow?.getAttribute('id');
						setUpdateEmployeeId(nextRow?.getAttribute('data-row-id'));
					}, 300);
				}

				break;
			default:
				break;
		}
	};

	if (globalCompany.id == null) {
		return (
			<section className="flex flex-col items-center">
				<h4 className="text-x mt-10 font-bold text-redAccent-500 dark:text-redAccent-600">
					Please Select a Company First
				</h4>
			</section>
		);
	} else if (isLoadingEmployeePersonalDetails || isLoadingLeaveGrades) {
		return <div></div>;
	} else {
		return (
			<>
				<section className="mx-2 mt-2">
					<div className="flex flex-row flex-wrap place-content-between">
						<div className="mr-4">
							<h1 className="text-3xl font-medium">Time Updation</h1>
							<p className="my-2 text-sm">Manage Employees attendances here</p>
						</div>
					</div>
					<div className="ml-14 max-w-full">
						<Formik
							initialValues={initialValues}
							validationSchema={TimeUpdationSchema}
							onSubmit={updateButtonClicked}
							component={(props) => (
								<EditAttendance
									{...props}
									errorMessage={errorMessage}
									setErrorMessage={setErrorMessage}
									globalCompany={globalCompany}
									updateEmployeeId={updateEmployeeId}
									// shifts={shifts}
									leaveGrades={leaveGrades}
									holidays={holidays}
									table={table}
									globalFilter={globalFilter}
									setGlobalFilter={setGlobalFilter}
									tbodyRef={tbodyRef}
									handleKeyDown={handleKeyDown}
									onRowClick={onRowClick}
									focusedRowRef={focusedRowRef}
									isTableFilterInputFocused={isTableFilterInputFocused}
									setIsTableFilterInputFocused={setIsTableFilterInputFocused}
									setSelectedDate={setSelectedDate}
								/>
							)}
						/>
					</div>
				</section>
			</>
		);
	}
};
export default TimeUpdationForm;
