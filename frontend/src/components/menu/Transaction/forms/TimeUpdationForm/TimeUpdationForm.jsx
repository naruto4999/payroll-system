import React, { useEffect, useMemo, useState, useCallback } from 'react';
import {
	createColumnHelper,
	flexRender,
	getCoreRowModel,
	useReactTable,
	getSortedRowModel,
} from '@tanstack/react-table';
import { FaRegTrashAlt, FaPen, FaAngleUp, FaAngleDown, FaEye } from 'react-icons/fa';
import { useGetEmployeePersonalDetailsQuery } from '../../../../authentication/api/employeeEntryApiSlice';
import { useAddEmployeeAttendanceMutation } from '../../../../authentication/api/timeUpdationApiSlice';

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

	const updateButtonClicked = async (values, formikBag) => {
		console.log(values);
		const employee_attendance = [];
		for (const day in values.attendance) {
			if (values.attendance.hasOwnProperty(day)) {
				employee_attendance.push({ ...values.attendance[day] });
			}
		}
		employee_attendance.map((each_attendance) => {
			each_attendance.company = globalCompany.id;
			each_attendance.employee = updateEmployeeId;
			each_attendance.otMin = null;
			each_attendance.lateMin = null;
			if (each_attendance.machineIn == '') {
				each_attendance.machineIn = null;
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

		console.log(toSend);

		// try {
		// 	const data = await addEmployeeAttendance(toSend).unwrap();
		// 	console.log(data);
		// 	dispatch(
		// 		alertActions.createAlert({
		// 			message: 'Saved',
		// 			type: 'Success',
		// 			duration: 3000,
		// 		})
		// 	);
		// } catch (err) {
		// 	console.log(err);
		// 	dispatch(
		// 		alertActions.createAlert({
		// 			message: 'Error Occurred',
		// 			type: 'Error',
		// 			duration: 5000,
		// 		})
		// 	);
		// }
	};

	const [editTimeUpdationPopover, setEditTimeUpdationPopover] = useState(false);

	const editTimeUpdationDetail = (personalDetail) => {
		setDateOfJoining(personalDetail.dateOfJoining);
		setUpdateEmployeeId(personalDetail.id);
		setEditTimeUpdationPopover(true);
	};

	const cancelButtonClicked = () => {
		setEditTimeUpdationPopover(false);
		setDateOfJoining(null);
		setUpdateEmployeeId(null);
		setErrorMessage('');
	};

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
			header: () => 'Paycode',
			cell: (props) => props.renderValue(),
			//   footer: props => props.column.id,
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
		columnHelper.accessor('dateOfJoining', {
			header: () => 'DOJ',
			cell: (props) => props.renderValue(),
			//   footer: info => info.column.id,
		}),
		columnHelper.accessor('designation', {
			header: () => 'Designation',
			cell: (props) => props.renderValue(),
			//   footer: info => info.column.id,
		}),
		columnHelper.display({
			id: 'actions',
			header: () => 'Actions',
			cell: (props) => (
				<div className="flex justify-center gap-4">
					<div
						className="rounded bg-teal-600 p-1.5 hover:bg-teal-700 dark:bg-teal-700 dark:hover:bg-teal-600"
						onClick={() => {
							editTimeUpdationDetail(props.row.original);
						}}
					>
						<FaPen className="h-4" />
					</div>
				</div>
			),
		}),
	];

	const data = useMemo(
		() => (employeePersonalDetails ? [...employeePersonalDetails] : []),
		[employeePersonalDetails]
	);

	const table = useReactTable({
		data,
		columns,
		initialState: {
			sorting: [{ id: 'name', desc: false }],
		},
		getCoreRowModel: getCoreRowModel(),
		getSortedRowModel: getSortedRowModel(),
		enableSortingRemoval: false,
	});

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
				<section className="mx-5 mt-2">
					<div className="flex flex-row flex-wrap place-content-between">
						<div className="mr-4">
							<h1 className="text-3xl font-medium">Employee Shifts</h1>
							<p className="my-2 text-sm">Edit and manage employees shifts here</p>
						</div>
					</div>
					<div className="scrollbar mx-auto max-h-[80dvh] max-w-6xl overflow-y-auto rounded border border-black border-opacity-50 shadow-md lg:max-h-[84dvh]">
						<table className="w-full border-collapse text-center text-sm">
							<thead className="sticky top-0 bg-blueAccent-600 dark:bg-blueAccent-700">
								{table.getHeaderGroups().map((headerGroup) => (
									<tr key={headerGroup.id}>
										{headerGroup.headers.map((header) => (
											<th key={header.id} scope="col" className="px-4 py-4 font-medium">
												{header.isPlaceholder ? null : (
													<div className="">
														<div
															{...{
																className: header.column.getCanSort()
																	? 'cursor-pointer select-none flex flex-row justify-center'
																	: '',
																onClick: header.column.getToggleSortingHandler(),
															}}
														>
															{flexRender(
																header.column.columnDef.header,
																header.getContext()
															)}

															{header.column.getCanSort() ? (
																<div className="relative pl-2">
																	<FaAngleUp
																		className={classNames(
																			header.column.getIsSorted() == 'asc'
																				? 'text-teal-700'
																				: '',
																			'absolute -translate-y-2 text-lg'
																		)}
																	/>
																	<FaAngleDown
																		className={classNames(
																			header.column.getIsSorted() == 'desc'
																				? 'text-teal-700'
																				: '',
																			'absolute translate-y-2 text-lg'
																		)}
																	/>
																</div>
															) : (
																''
															)}
														</div>
													</div>
												)}
											</th>
										))}
									</tr>
								))}
							</thead>
							<tbody className="max-h-20 divide-y divide-black divide-opacity-50 overflow-y-auto border-t border-black border-opacity-50">
								{table.getRowModel().rows.map((row) => (
									<tr className="hover:bg-zinc-200 dark:hover:bg-zinc-800" key={row.id}>
										{row.getVisibleCells().map((cell) => (
											<td className="px-4 py-4 font-normal" key={cell.id}>
												<div className="text-sm">
													<div className="font-medium">
														{flexRender(cell.column.columnDef.cell, cell.getContext())}
													</div>
												</div>
											</td>
										))}
									</tr>
								))}
							</tbody>
						</table>
					</div>

					<ReactModal
						className="items-left scrollbar container fixed inset-0 my-auto flex h-fit max-h-[100dvh] flex-col gap-4 overflow-y-scroll rounded bg-zinc-300 p-4 pl-16 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-7xl"
						isOpen={editTimeUpdationPopover}
						onRequestClose={cancelButtonClicked}
						style={{
							overlay: {
								backgroundColor: 'rgba(0, 0, 0, 0.75)',
							},
						}}
					>
						<Formik
							initialValues={initialValues}
							validationSchema={''}
							onSubmit={updateButtonClicked}
							component={(props) => (
								<EditAttendance
									{...props}
									errorMessage={errorMessage}
									setErrorMessage={setErrorMessage}
									globalCompany={globalCompany}
									updateEmployeeId={updateEmployeeId}
									// shifts={shifts}
									dateOfJoining={dateOfJoining}
									cancelButtonClicked={cancelButtonClicked}
									leaveGrades={leaveGrades}
									holidays={holidays}
								/>
							)}
						/>
					</ReactModal>
				</section>
			</>
		);
	}
};
export default TimeUpdationForm;
