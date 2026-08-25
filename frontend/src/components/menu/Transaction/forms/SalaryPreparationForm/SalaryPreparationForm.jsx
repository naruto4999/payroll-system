import React, { useMemo, useState, useRef } from 'react';
import {
	// column,
	createColumnHelper,
	getCoreRowModel,
	useReactTable,
	getSortedRowModel,
	// columnFiltersState,
	getFilteredRowModel,
	// filterFn,
	// filterFns,
} from '@tanstack/react-table';

import { useGetEmployeePersonalDetailsQuery } from '../../../../authentication/api/employeeEntryApiSlice';
import { useAddEmployeeSalaryPreparedMutation } from '../../../../authentication/api/salaryPreparationApiSlice';
import { useOutletContext } from 'react-router-dom';
import ReactModal from 'react-modal';
import { Formik } from 'formik';
import { useDispatch, useSelector } from 'react-redux';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import { apiSlice } from '../../../../authentication/api/apiSlice';
import { getApiErrorMessage } from '../../../../authentication/api/errorUtils';
import EmployeeTable from './EmployeeTable';
import EditSalary from './EditSalary';
import { SalaryPreparationSchema } from './SalaryPreperationSchema';
// import TableFilterInput from '../TimeUpdationForm/TableFilterInput';
import TableFilterInput from './TableFilterInput';

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

const SalaryPreparationForm = () => {
	const dispatch = useDispatch();
	const globalCompany = useSelector((state) => state.globalCompany);

	const [showLoadingBar, setShowLoadingBar] = useOutletContext();
	const {
		data: employeePersonalDetails,
		isLoading: isLoadingEmployeePersonalDetails,
		isSuccess: isSuccessEmployeePersonalDetails,
	} = useGetEmployeePersonalDetailsQuery(globalCompany);
	const [
		addEmployeeSalaryPrepared,
		{
			isLoading: isAddingEmployeeSalaryPrepared,
			// isError: errorRegisteringRegular,
			isSuccess: isAddEmployeeSalaryPreparedSuccess,
		},
	] = useAddEmployeeSalaryPreparedMutation();

	const [updateEmployeeId, setUpdateEmployeeId] = useState(null);
	const [globalFilter, setGlobalFilter] = useState('');
	// const [isTableFilterInputFocused, setIsTableFilterInputFocused] = useState(false);

	// const initialValues = useMemo(() => generateInitialValues(), []);
	const columnHelper = createColumnHelper();

	const columns = [
		columnHelper.accessor('paycode', {
			header: () => 'PC',
			cell: (props) => props.renderValue(),
			meta: {
				columnClassName: 'w-[64px]',
				headerClassName: 'whitespace-nowrap',
				cellClassName: 'whitespace-nowrap',
			},
			//   footer: props => props.column.id,
			// filterFn: 'fuzzy',
		}),
		columnHelper.accessor('attendanceCardNo', {
			header: () => 'ACN',
			cell: (props) => props.renderValue(),
			meta: {
				columnClassName: 'w-[64px]',
				headerClassName: 'whitespace-nowrap',
				cellClassName: 'whitespace-nowrap',
			},
			//   footer: props => props.column.id,
		}),

		columnHelper.accessor('name', {
			header: () => 'Employee Name',
			cell: (props) => props.renderValue(),
			meta: {
				columnClassName: 'w-[220px]',
				headerClassName: 'whitespace-nowrap text-left',
				headerContentClassName: 'justify-start',
				cellClassName: 'text-left',
				cellContentClassName: 'truncate whitespace-nowrap',
			},
			//   footer: info => info.column.id,
		}),
		columnHelper.accessor('designation', {
			header: () => 'Designation',
			cell: (props) => props.renderValue(),
			meta: {
				columnClassName: 'w-[180px]',
				headerClassName: 'whitespace-nowrap text-left',
				headerContentClassName: 'justify-start',
				cellClassName: 'text-left',
				cellContentClassName: 'truncate whitespace-nowrap',
			},
			//   footer: info => info.column.id,
		}),
		columnHelper.accessor('dateOfJoining', {
			header: () => 'DOJ',
			cell: (props) => props.renderValue(),
			meta: {
				columnClassName: 'w-[118px]',
				headerClassName: 'whitespace-nowrap',
				cellClassName: 'whitespace-nowrap tabular-nums',
			},
			// enableHiding: true,
			enableGlobalFilter: false,
		}),
		columnHelper.accessor('resignationDate', {
			header: () => 'Resign Date',
			cell: (props) => props.renderValue(),
			meta: {
				columnClassName: 'w-[118px]',
				headerClassName: 'whitespace-nowrap',
				cellClassName: 'whitespace-nowrap tabular-nums',
			},
			enableHiding: true,
			enableGlobalFilter: false,
		}),
	];

	const [selectedDate, setSelectedDate] = useState({
		year: new Date().getFullYear(),
		month: new Date().getMonth() + 1,
	});
	const selectionKey = `${globalCompany?.id}-${updateEmployeeId}-${selectedDate.year}-${selectedDate.month}`;
	const latestSelectionKeyRef = useRef(selectionKey);
	latestSelectionKeyRef.current = selectionKey;

	const data = useMemo(() => {
		if (!employeePersonalDetails) return [];

		const filteredData = employeePersonalDetails.filter((employee) => {
			if (employee.dateOfJoining) {
				const comparisonDate = new Date(Date.UTC(selectedDate.year, parseInt(selectedDate.month) - 1, 1));
				// Extract the year and month from the original dateOfJoining
				const [year, month] = employee.dateOfJoining.split('-').map(Number);
				if (employee.resignationDate) {
					const [resignYear, resignMonth] = employee.resignationDate.split('-').map(Number);
					const resignDate = new Date(Date.UTC(resignYear, resignMonth, 0));
					if (resignDate < comparisonDate) {
						return false;
					}
				}
				const newDateOfJoining = new Date(Date.UTC(year, month - 1, 1));
				return newDateOfJoining <= comparisonDate;
			} else {
				return false;
			}
		});

		return filteredData;
	}, [employeePersonalDetails, selectedDate]);

	const earliestMonthAndYear = useMemo(() => {
		let earliestDate = Infinity; // Initialize earliestDate to a very large value
		let earliestMonth = '';
		let earliestYear = '';
		if (employeePersonalDetails) {
			for (const employee of employeePersonalDetails) {
				const dateOfJoining = new Date(employee.dateOfJoining);

				if (dateOfJoining < earliestDate) {
					earliestDate = dateOfJoining;
					earliestMonth = dateOfJoining.getMonth() + 1;
					earliestYear = dateOfJoining.getFullYear();
				}
			}
		}
		return {
			earliestMonth: earliestMonth,
			earliestYear: earliestYear,
		};
	}, [employeePersonalDetails]);

	const optionsForYear = useMemo(() => {
		if (!earliestMonthAndYear?.earliestYear) return [];

		return Array.from(
			{ length: new Date().getFullYear() - earliestMonthAndYear.earliestYear + 1 },
			(_, index) => earliestMonthAndYear.earliestYear + index
		);
	}, [earliestMonthAndYear]);

	const generateInitialValues = () => {
		const initialValues = {
			year: selectedDate.year,
			month: selectedDate.month,
			employeeSalaryPrepared: {
				incentiveAmount: 0,
				advanceDeducted: null,
				vpfDeducted: null,
				tdsDeducted: null,
				othersDeducted: 0,
			},
			earnedAmount: [],
		};
		return initialValues;
	};
	const initialValues = useMemo(() => generateInitialValues(), [selectedDate]);

	const table = useReactTable({
		data,
		columns,
		initialState: {
			sorting: [{ id: 'name', desc: false }],
			columnVisibility: { dateOfJoining: true, resignationDate: false },
		},
		state: {
			globalFilter,
		},
		onGlobalFilterChange: setGlobalFilter,
		getCoreRowModel: getCoreRowModel(),
		getSortedRowModel: getSortedRowModel(),
		getFilteredRowModel: getFilteredRowModel(),
		enableSortingRemoval: false,
	});

	const tbodyRef = useRef(null);
	const focusedRowRef = useRef(null);
	let debouncedSetUpdateEmployeeId;

	const onRowClick = (event, row) => {
		const currentRow = tbodyRef.current?.children.namedItem(row.original.id);
		clearTimeout(debouncedSetUpdateEmployeeId); // Clear the debounce timer
		debouncedSetUpdateEmployeeId = setTimeout(() => {
			focusedRowRef.current = currentRow.getAttribute('id');
			setUpdateEmployeeId(row.original.id);
		}, 300);
	};
	const handleKeyDown = (event, row) => {
		event.stopPropagation();
		event.preventDefault();
		const currentRow = tbodyRef.current?.children.namedItem(row.original.id);

		switch (event.key) {
			case 'ArrowUp':
				const previousRow = currentRow?.previousElementSibling;
				if (previousRow) {
					previousRow.focus();

					// setUpdateEmployeeId(previousRow?.getAttribute('data-row-id'));
					clearTimeout(debouncedSetUpdateEmployeeId); // Clear the debounce timer
					debouncedSetUpdateEmployeeId = setTimeout(() => {
						focusedRowRef.current = previousRow?.getAttribute('id');
						setUpdateEmployeeId(parseInt(previousRow?.getAttribute('data-row-id')));
					}, 300);
				}
				// focusedRowRef.current = currentRow.previousElementSibling;
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
						setUpdateEmployeeId(parseInt(nextRow?.getAttribute('data-row-id')));
					}, 300);
				}

				// focusedRowRef.current = currentRow.nextElementSibling;
				break;
			default:
				break;
		}
	};
	const updateButtonClicked = async (values, formikBag) => {
		const requestKey = `${globalCompany.id}-${updateEmployeeId}-${values.year}-${values.month}`;
		const toSend = { employeeSalaryPrepared: {}, allEarnedAmounts: [] };
		toSend.employeeSalaryPrepared = {
			date: `${values.year}-${values.month}-1`,
			employee: parseInt(updateEmployeeId),
			company: globalCompany.id,
			incentiveAmount: values.employeeSalaryPrepared.incentiveAmount,
			advanceDeducted: values.employeeSalaryPrepared.advanceDeducted,
			vpfDeducted: values.employeeSalaryPrepared.vpfDeducted,
			tdsDeducted: values.employeeSalaryPrepared.tdsDeducted,
			othersDeducted: values.employeeSalaryPrepared.othersDeducted,
		};
		toSend.allEarnedAmounts = values.earnedAmount.map((row) => ({
			earningsHead: { id: row.earningsHead.id },
			rate: row.rate,
			earnedAmount: row.earnedAmount,
			arearAmount: row.arearAmount,
		}));

		try {
			await addEmployeeSalaryPrepared(toSend).unwrap();
			if (latestSelectionKeyRef.current !== requestKey) {
				dispatch(
					alertActions.createAlert({
						message: 'Salary saved, but the selection changed before the response returned.',
						type: 'Success',
						duration: 5000,
					})
				);
				return;
			}
			dispatch(
				apiSlice.util.invalidateTags([
					{ type: 'SalaryOvertimePreview', id: requestKey },
				])
			);
			dispatch(
				alertActions.createAlert({
					message: 'Saved',
					type: 'Success',
					duration: 3000,
				})
			);
		} catch (err) {
			const requiresReview = [
				'stale_salary_rate',
				'missing_earned_heads',
				'duplicate_earned_head',
				'invalid_earned_head',
			].includes(err?.data?.code);
			if (requiresReview) {
				dispatch(apiSlice.util.invalidateTags(['AllEmployeeSalaryEarnings', 'SalaryOvertimePreview']));
			}
			const message = `${getApiErrorMessage(err)}${
				requiresReview ? ' Salary earnings were refreshed; review the rows before saving again.' : ''
			}`;
			dispatch(
				alertActions.createAlert({
					message: message,
					type: 'Error',
					duration: 5000,
				})
			);
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
	} else if (isLoadingEmployeePersonalDetails) {
		return <div></div>;
	} else {
		return (
			<section className="mx-5 mt-2">
				<div className="flex flex-row flex-wrap items-start justify-between gap-4">
					<div className="mr-4">
						<h1 className="text-3xl font-medium">Salary Preperation</h1>
						<p className="my-2 text-sm">Prepare employees salaries here</p>
					</div>
					<section className="flex flex-wrap items-center gap-2 text-sm">
						<label
							htmlFor="salary-preparation-year"
							className="font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Month and Year:
						</label>
						<select
							id="salary-preparation-month"
							value={selectedDate.month}
							onChange={(event) => setSelectedDate((previous) => ({ ...previous, month: event.target.value }))}
							className="rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
						>
							{months.map((month, index) => (
								<option key={month} value={index + 1}>
									{month}
								</option>
							))}
						</select>
						<select
							id="salary-preparation-year"
							value={selectedDate.year}
							onChange={(event) => setSelectedDate((previous) => ({ ...previous, year: event.target.value }))}
							className="rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
						>
							{optionsForYear.map((year) => (
								<option key={year} value={year}>
									{year}
								</option>
							))}
						</select>
					</section>
				</div>
				<div className="grid w-full gap-6 lg:grid-cols-[minmax(0,0.95fr)_minmax(0,1.05fr)] lg:items-start lg:gap-8 xl:grid-cols-[minmax(640px,0.95fr)_minmax(0,1.05fr)]">
					<div className="mt-4 min-w-0 lg:ml-4">
						<TableFilterInput
							globalFilter={globalFilter}
							setGlobalFilter={setGlobalFilter}
							// isTableFilterInputFocused={isTableFilterInputFocused}
							// setIsTableFilterInputFocused={setIsTableFilterInputFocused}
						/>
						<EmployeeTable
							table={table}
							tbodyRef={tbodyRef}
							handleKeyDown={handleKeyDown}
							onRowClick={onRowClick}
							focusedRowRef={focusedRowRef}
						/>
					</div>
					{updateEmployeeId == null ? (
						<div className="mx-auto mt-10 text-xl font-bold dark:text-red-700">
							Please Select an Employee to prepare the Salary
						</div>
					) : (
						<div className="mt-4 min-w-0">
							<Formik
								key={`${updateEmployeeId}-${selectedDate.year}-${selectedDate.month}`}
								enableReinitialize
								initialValues={initialValues}
								validationSchema={SalaryPreparationSchema}
								onSubmit={updateButtonClicked}
								component={(props) => (
									<EditSalary
										{...props}
										updateEmployeeId={updateEmployeeId}
										globalCompany={globalCompany}
										isAddingEmployeeSalaryPrepared={isAddingEmployeeSalaryPrepared}
										employeePersonalDetails={employeePersonalDetails}
									/>
								)}
							/>
						</div>
					)}
				</div>
			</section>
		);
	}
};
export default SalaryPreparationForm;
