import React, { useEffect, useMemo, useState, useCallback } from 'react';
import {
	createColumnHelper,
	flexRender,
	getCoreRowModel,
	useReactTable,
	getSortedRowModel,
} from '@tanstack/react-table';
import {
	FaRegTrashAlt,
	FaPen,
	FaAngleUp,
	FaAngleDown,
	FaEye,
} from 'react-icons/fa';
import { useGetEmployeePersonalDetailsQuery } from '../../../../authentication/api/employeeEntryApiSlice';
import { useGetShiftsQuery } from '../../../../authentication/api/shiftEntryApiSlice';
import { useUpdateEmployeeShiftsMutation } from '../../../../authentication/api/employeeShiftsApiSlice';
import { useOutletContext } from 'react-router-dom';
import ReactModal from 'react-modal';
import { Formik } from 'formik';
import { useDispatch, useSelector } from 'react-redux';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import EditEmployeeShift from './EditEmployeeShift';
import * as yup from 'yup';
// import { generateEmployeeSalarySchema } from './EmployeeSalarySchema';
// import { useUpdateEmployeeSalaryEarningMutation } from '../../../../authentication/api/employeeEntryApiSlice';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const isDateWithinRange = (date, fromDate, toDate) => {
	return date >= fromDate && date <= toDate;
};

const EmployeeShiiftsEntryForm = () => {
	const dispatch = useDispatch();
	const globalCompany = useSelector((state) => state.globalCompany);
	const {
		data: shifts,
		isLoading: isLoadingShifts,
		isSuccess,
		isFetching,
		refetch,
	} = useGetShiftsQuery(globalCompany);
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();
	const {
		data: employeePersonalDetails,
		isLoading: isLoadingEmployeePersonalDetails,
		isSuccess: isSuccessEmployeePersonalDetails,
	} = useGetEmployeePersonalDetailsQuery(globalCompany);
	console.log(shifts);
	const [updateEmployeeShifts, { isLoading: isUpdatingEmployeeShifts }] =
		useUpdateEmployeeShiftsMutation();

	const [editShiftPopover, setEditShiftPopover] = useState(false);
	const [updateEmployeeShiftId, setUpdateEmployeeShiftId] = useState(null);
	const [dateOfJoining, setDateOfJoining] = useState(null);
	const [errorMessage, setErrorMessage] = useState('');

	const editEmployeeShiftsPopoverHandler = async (personalDetail) => {
		console.log(personalDetail);
		console.log(personalDetail.dateOfJoining);
		setDateOfJoining(personalDetail.dateOfJoining);
		setUpdateEmployeeShiftId(personalDetail.id);
		// setFirstRender(true);
		setEditShiftPopover(!editShiftPopover);
	};

	const cancelButtonClicked = useCallback(() => {
		setEditShiftPopover(false);
		setUpdateEmployeeShiftId(null);
		// setFirstRender(false);
		setDateOfJoining(null);
	}, []);

	const updateButtonClicked = async (values, formikBag) => {
		const employeeShifts = [];
		let fromDate = null;
		let toDate = null;
		let prevValue = parseInt(values.dayWiseShifts[1]);
		const daysInMonth = new Date(values.year, values.month, 0).getDate();
		const dateOfJoiningObj = new Date(dateOfJoining);

		for (let day = 1; day <= daysInMonth; day++) {
			const calendarDate = new Date(
				Date.UTC(values.year, values.month - 1, day, 0, 0, 0, 0)
			);

			if (calendarDate < dateOfJoiningObj) {
				fromDate = day + 1;
				prevValue = parseInt(values.dayWiseShifts[day + 1]);
				toDate = day + 1;
				continue;
			}

			const currentValue = parseInt(values.dayWiseShifts[day]);
			if (currentValue !== prevValue) {
				if (fromDate !== null && toDate !== null) {
					// Push the segment to the employeeShifts array
					employeeShifts.push({
						fromDate: `${values.year}-${values.month}-${fromDate}`,
						toDate: `${values.year}-${values.month}-${toDate}`,
						shift: prevValue, // Use prevValue, since currentValue could have changed
						employee: updateEmployeeShiftId,
						company: globalCompany.id,
					});

					fromDate = day;
					prevValue = currentValue;
				}
			}

			toDate = day;
		}

		if (fromDate !== null && toDate !== null) {
			// Store the last segment for the earning head
			employeeShifts.push({
				fromDate: `${values.year}-${values.month}-${fromDate}`,
				toDate: `${values.year}-${values.month}-${toDate}`,
				shift: prevValue, // Use prevValue
				employee: updateEmployeeShiftId,
				company: globalCompany.id,
			});
		}

		const toSend = {
			company: globalCompany.id,
			employee: updateEmployeeShiftId,
			employeeShifts: employeeShifts,
		};

		// Wrap your API call with try-catch for error handling
		try {
			const data = await updateEmployeeShifts(toSend).unwrap();
			console.log(data);
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

	console.log(shifts);

	const columnHelper = createColumnHelper();

	const generateInitialValues = () => {
		const currentDate = new Date();
		const currentYear = currentDate.getFullYear();
		// get method returns a zero-based index for the month
		const currentMonthIndex = currentDate.getMonth();
		const daysInMonth = new Date(
			currentYear,
			currentMonthIndex + 1,
			0
		).getDate();
		console.log(daysInMonth);

		const initialValues = {
			year: currentYear,
			month: currentMonthIndex + 1,
			dayWiseShifts: {},
		};

		for (let day = 1; day <= daysInMonth; day++) {
			initialValues.dayWiseShifts[day] = '';
		}
		return initialValues;
	};
	console.log(generateInitialValues());
	const initialValues = useMemo(() => generateInitialValues(), []);

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
							editEmployeeShiftsPopoverHandler(
								props.row.original
							);
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
	}
	if (isLoadingEmployeePersonalDetails || isLoadingShifts) {
		return <div></div>;
	} else {
		return (
			<>
				<section className="mx-5 mt-2">
					<div className="flex flex-row flex-wrap place-content-between">
						<div className="mr-4">
							<h1 className="text-3xl font-medium">
								Employee Shifts
							</h1>
							<p className="my-2 text-sm">
								Edit and manage employees shifts here
							</p>
						</div>
					</div>
					<div className="scrollbar mx-auto max-h-[80dvh] max-w-6xl overflow-y-auto rounded border border-black border-opacity-50 shadow-md lg:max-h-[84dvh]">
						<table className="w-full border-collapse text-center text-sm">
							<thead className="sticky top-0 bg-blueAccent-600 dark:bg-blueAccent-700">
								{table.getHeaderGroups().map((headerGroup) => (
									<tr key={headerGroup.id}>
										{headerGroup.headers.map((header) => (
											<th
												key={header.id}
												scope="col"
												className="px-4 py-4 font-medium"
											>
												{header.isPlaceholder ? null : (
													<div className="">
														<div
															{...{
																className:
																	header.column.getCanSort()
																		? 'cursor-pointer select-none flex flex-row justify-center'
																		: '',
																onClick:
																	header.column.getToggleSortingHandler(),
															}}
														>
															{flexRender(
																header.column
																	.columnDef
																	.header,
																header.getContext()
															)}

															{header.column.getCanSort() ? (
																<div className="relative pl-2">
																	<FaAngleUp
																		className={classNames(
																			header.column.getIsSorted() ==
																				'asc'
																				? 'text-teal-700'
																				: '',
																			'absolute -translate-y-2 text-lg'
																		)}
																	/>
																	<FaAngleDown
																		className={classNames(
																			header.column.getIsSorted() ==
																				'desc'
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
									<tr
										className="hover:bg-zinc-200 dark:hover:bg-zinc-800"
										key={row.id}
									>
										{row.getVisibleCells().map((cell) => (
											<td
												className="px-4 py-4 font-normal"
												key={cell.id}
											>
												<div className="text-sm">
													<div className="font-medium">
														{flexRender(
															cell.column
																.columnDef.cell,
															cell.getContext()
														)}
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
						className="items-left scrollbar container fixed inset-0 mx-2 my-auto flex h-fit max-h-[100dvh] flex-col gap-4 overflow-y-scroll rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-[1100px]"
						isOpen={editShiftPopover}
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
								<EditEmployeeShift
									{...props}
									errorMessage={errorMessage}
									setErrorMessage={setErrorMessage}
									globalCompany={globalCompany}
									updateEmployeeShiftId={
										updateEmployeeShiftId
									}
									shifts={shifts}
									// firstRender={firstRender}
									// setFirstRender={setFirstRender}
									dateOfJoining={dateOfJoining}
								/>
							)}
						/>
					</ReactModal>
				</section>
			</>
		);
	}
};

export default EmployeeShiiftsEntryForm;
