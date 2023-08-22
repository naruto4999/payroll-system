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
import { useGetEarningsHeadsQuery } from '../../../../authentication/api/earningsHeadEntryApiSlice';
import { useOutletContext } from 'react-router-dom';
import ReactModal from 'react-modal';
import { Formik } from 'formik';
import { useDispatch, useSelector } from 'react-redux';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import EditSalary from './EditSalary';
import * as yup from 'yup';
import { generateEmployeeSalarySchema } from './EmployeeSalarySchema';
import { useUpdateEmployeeSalaryEarningMutation } from '../../../../authentication/api/employeeEntryApiSlice';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const isDateWithinRange = (date, fromDate, toDate) => {
	return date >= fromDate && date <= toDate;
};

const EmployeeSalaryForm = () => {
	const dispatch = useDispatch();
	const globalCompany = useSelector((state) => state.globalCompany);
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();
	const [firstRender, setFirstRender] = useState(false);

	const {
		data: employeePersonalDetails,
		isLoading: isLoadingEmployeePersonalDetails,
		isSuccess: isSuccessEmployeePersonalDetails,
		// isError,
		// error,
		// isFetching,
		// refetch,
	} = useGetEmployeePersonalDetailsQuery(globalCompany);

	const {
		data: fetchedEarningsHeads,
		isLoading: isLoadingEarningsHeads,
		isSuccess: EarningsHeadsSuccess,
	} = useGetEarningsHeadsQuery(globalCompany);

	const [
		updateEmployeeSalaryEarning,
		{ isLoading: isUpdatingEmployeeSalaryEarning },
	] = useUpdateEmployeeSalaryEarningMutation();

	console.log(fetchedEarningsHeads);

	const [editSalaryPopover, setEditSalaryPopover] = useState(false);
	const [updateEmployeeSalaryId, setUpdateEmployeeSalaryId] = useState('');
	const [errorMessage, setErrorMessage] = useState('');
	const [yearOfJoining, setYearOfJoining] = useState(null);
	const [monthOfJoining, setMonthOfJoining] = useState(null);

	const editEmployeeSalaryPopoverHandler = async (personalDetail) => {
		console.log(personalDetail);
		const year = new Date(personalDetail.dateOfJoining).getFullYear();
		const month = new Date(personalDetail.dateOfJoining).getMonth() + 1; // Adding 1 because getMonth() returns values from 0 to 11.
		console.log(month);

		setYearOfJoining(year);
		setMonthOfJoining(month);
		setUpdateEmployeeSalaryId(personalDetail.id);
		setFirstRender(true);
		setEditSalaryPopover(!editSalaryPopover);
	};

	const updateButtonClicked = useCallback(
		async (values, formikBag) => {
			console.log(values);
			const employeeEarnings = [];
			for (const earningHead in values.earnings) {
				let earningHeadId = null;
				fetchedEarningsHeads.forEach((item) => {
					if (item.name === earningHead) {
						earningHeadId = item.id;
					}
				});
				const months = [
					'01',
					'02',
					'03',
					'04',
					'05',
					'06',
					'07',
					'08',
					'09',
					'10',
					'11',
					'12',
				];

				let fromDate = `01`;
				let toDate = null;
				let prevValue = values.earnings[earningHead]['01'];

				for (const month of months) {
					if (
						values.year == yearOfJoining &&
						parseInt(fromDate) < monthOfJoining
					) {
						fromDate = month;
						prevValue = values.earnings[earningHead][month];
						toDate = month;
						continue;
					}
					// console.log(parseInt(fromDate));
					const currentValue = values.earnings[earningHead][month];

					if (currentValue !== prevValue) {
						console.log(
							'current value',
							currentValue,
							' prevValue',
							prevValue
						);
						console.log(fromDate);
						console.log(toDate);
						if (fromDate !== null && toDate !== null) {
							// A segment is complete, push it to the employeeEarnings array

							employeeEarnings.push({
								earningsHead: earningHeadId,
								fromDate: `${values.year}-${fromDate}-01`,
								toDate: `${values.year}-${toDate}-01`,
								value: values.earnings[earningHead][fromDate],
								employee: updateEmployeeSalaryId,
								company: globalCompany.id,
							});

							fromDate = month;
							prevValue = currentValue;
						}
					}

					toDate = month;
				}

				if (fromDate !== null && toDate !== null) {
					// Store the last segment for the earning head
					employeeEarnings.push({
						earningsHead: earningHeadId,
						fromDate: `${values.year}-${fromDate}-01`,
						toDate: `${values.year}-${toDate}-01`,
						value: values.earnings[earningHead][fromDate],
						employee: updateEmployeeSalaryId,
						company: globalCompany.id,
					});
				}
			}
			console.log(employeeEarnings);
			// console.log(yearOfJoining);
			console.log(monthOfJoining);
			try {
				const data = await updateEmployeeSalaryEarning({
					employeeEarnings,
					globalCompany: globalCompany.id,
					employee: updateEmployeeSalaryId,
				}).unwrap();
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
		},
		[
			fetchedEarningsHeads,
			updateEmployeeSalaryId,
			yearOfJoining,
			monthOfJoining,
		]
	);
	console.log(monthOfJoining);

	const cancelButtonClicked = useCallback(() => {
		setEditSalaryPopover(false);
		setUpdateEmployeeSalaryId(null);
		setFirstRender(false);
		setYearOfJoining(null);
		setMonthOfJoining(null);
	}, []);

	const generateInitialValues = () => {
		const currentDate = new Date();
		const currentYear = currentDate.getFullYear();
		const initialValues = {
			year: currentYear,
			earnings: {},
			sameValue: {
				'01': false,
				'02': false,
				'03': false,
				'04': false,
				'05': false,
				'06': false,
				'07': false,
				'08': false,
				'09': false,
				10: false,
				11: false,
				12: false,
			},
		};

		// Iterate through each object in fetchedEarningsHeads
		fetchedEarningsHeads.forEach((item) => {
			const monthInitialValues = {};
			const months = [
				'01',
				'02',
				'03',
				'04',
				'05',
				'06',
				'07',
				'08',
				'09',
				'10',
				'11',
				'12',
			];

			// Set initial value for each month ('01' to '12')
			months.forEach((month) => {
				monthInitialValues[month] = '';
			});

			// Assign the monthInitialValues object to the 'name' key
			initialValues.earnings[item.name] = monthInitialValues;
		});

		return initialValues;
	};
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
							editEmployeeSalaryPopoverHandler(
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
	const schema = useMemo(() => {
		fetchedEarningsHeads
			? generateEmployeeSalarySchema(fetchedEarningsHeads)
			: '';
	}, [fetchedEarningsHeads]);

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

	const initialValues = useMemo(
		() => (fetchedEarningsHeads ? generateInitialValues() : ''),
		[fetchedEarningsHeads]
	);
	console.log(initialValues);

	if (globalCompany.id == null) {
		return (
			<section className="flex flex-col items-center">
				<h4 className="text-x mt-10 font-bold text-redAccent-500 dark:text-redAccent-600">
					Please Select a Company First
				</h4>
			</section>
		);
	}
	if (isLoadingEmployeePersonalDetails) {
		return <div></div>;
	} else {
		return (
			<>
				<section className="mx-5 mt-2">
					<div className="flex flex-row flex-wrap place-content-between">
						<div className="mr-4">
							<h1 className="text-3xl font-medium">
								Employee Salary
							</h1>
							<p className="my-2 text-sm">
								Edit and manage salaries here
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
						className="items-left scrollbar fixed inset-0 mx-2 my-auto flex h-fit max-h-[100dvh] w-fit flex-col gap-4 overflow-y-scroll rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-[1100px]"
						isOpen={editSalaryPopover}
						onRequestClose={cancelButtonClicked}
						style={{
							overlay: {
								backgroundColor: 'rgba(0, 0, 0, 0.75)',
							},
						}}
					>
						<Formik
							initialValues={initialValues}
							validationSchema={schema}
							onSubmit={updateButtonClicked}
							component={(props) => (
								<EditSalary
									{...props}
									// errorMessage={errorMessage}
									// setErrorMessage={setErrorMessage}
									// editEmployeeSalaryPopoverHandler={
									//     editEmployeeSalaryPopoverHandler
									// }
									globalCompany={globalCompany}
									yearOfJoining={yearOfJoining}
									updateEmployeeSalaryId={
										updateEmployeeSalaryId
									}
									fetchedEarningsHeads={fetchedEarningsHeads}
									firstRender={firstRender}
									setFirstRender={setFirstRender}
									monthOfJoining={monthOfJoining}
									cancelButtonClicked={cancelButtonClicked}
								/>
							)}
						/>
					</ReactModal>
				</section>
			</>
		);
	}
};

export default EmployeeSalaryForm;
