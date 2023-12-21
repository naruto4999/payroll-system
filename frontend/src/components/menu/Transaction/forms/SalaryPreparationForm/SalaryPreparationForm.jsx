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

import { rankItem } from '@tanstack/match-sorter-utils';
import { FaRegTrashAlt, FaPen, FaAngleUp, FaAngleDown, FaEye } from 'react-icons/fa';
import { useGetEmployeePersonalDetailsQuery } from '../../../../authentication/api/employeeEntryApiSlice';
import { useAddEmployeeSalaryPreparedMutation } from '../../../../authentication/api/salaryPreparationApiSlice';
import { useOutletContext } from 'react-router-dom';
import ReactModal from 'react-modal';
import { Formik } from 'formik';
import { useDispatch, useSelector } from 'react-redux';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import * as yup from 'yup';
import EmployeeTable from './EmployeeTable';
import EditSalary from './EditSalary';
// import TableFilterInput from '../TimeUpdationForm/TableFilterInput';
import TableFilterInput from './TableFilterInput';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

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

	const [selectedDate, setSelectedDate] = useState({
		year: new Date().getFullYear(),
		month: new Date().getMonth() + 1,
	});
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

	const generateInitialValues = () => {
		const currentDate = new Date();
		const currentYear = currentDate.getFullYear();
		// get method returns a zero-based index for the month
		const currentMonthIndex = currentDate.getMonth();
		// const daysInMonth = new Date(currentYear, currentMonthIndex + 1, 0).getDate();

		const initialValues = {
			year: currentYear,
			month: currentMonthIndex + 1,
			employeeSalaryPrepared: {
				incentiveAmount: 0,
				pfDeducted: 0,
				esiDeducted: 0,
				vpfDeducted: 0,
				advanceDeducted: 0,
				tdsDeducted: 0,
				labourWelfareFundDeducted: 0,
				othersDeducted: 0,
				netOtMinutesMonthly: 0,
				netOtAmountMonthly: 0,
				paymentMode: '',
			},
			earnedAmount: [],
		};
		return initialValues;
	};
	const initialValues = useMemo(() => generateInitialValues(), []);

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
		console.log('here bish', values);
		let toSend = { employeeSalaryPrepared: {}, allEarnedAmounts: [] };
		toSend.employeeSalaryPrepared = { ...values.employeeSalaryPrepared };
		toSend.employeeSalaryPrepared.date = `${values.year}-${values.month}-1`;
		toSend.employeeSalaryPrepared.employee = parseInt(updateEmployeeId);
		toSend.employeeSalaryPrepared.company = globalCompany.id;
		toSend.allEarnedAmounts = [...values.earnedAmount];
		console.log(toSend);

		try {
			const data = await addEmployeeSalaryPrepared(toSend).unwrap();
			dispatch(
				alertActions.createAlert({
					message: 'Saved',
					type: 'Success',
					duration: 3000,
				})
			);
		} catch (err) {
			console.log(err);
			let message = 'Error Occurred';
			if (err.data?.detail == 'Too Much Advance Emi Repayment') {
				message = 'Too Much Advance Emi Repayment';
			}
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
				<div className="flex flex-row flex-wrap place-content-between">
					<div className="mr-4">
						<h1 className="text-3xl font-medium">Salary Preperation</h1>
						<p className="my-2 text-sm">Prepare employees salaries here</p>
					</div>
				</div>
				<div className="flex w-full flex-row gap-8">
					<div className="mt-4 ml-4 w-2/5">
						<TableFilterInput
							globalFilter={globalFilter}
							setGlobalFilter={setGlobalFilter}
							// isTableFilterInputFocused={isTableFilterInputFocused}
							// setIsTableFilterInputFocused={setIsTableFilterInputFocused}
						/>
						<EmployeeTable
							table={table}
							flexRender={flexRender}
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
						<div className="mt-4">
							<Formik
								initialValues={initialValues}
								validationSchema={''}
								onSubmit={updateButtonClicked}
								component={(props) => (
									<EditSalary
										{...props}
										updateEmployeeId={updateEmployeeId}
										globalCompany={globalCompany}
										earliestMonthAndYear={earliestMonthAndYear}
										setSelectedDate={setSelectedDate}
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
