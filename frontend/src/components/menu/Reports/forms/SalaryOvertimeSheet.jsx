import React, { useState, useMemo, useEffect } from 'react';
// import { useGetCompanyStatisticsQuery } from '../../../authentication/api/salaryOvertimeSheetApiSlice';
import { useSelector } from 'react-redux';
import { useGetEmployeePersonalDetailsQuery } from '../../../authentication/api/employeeEntryApiSlice';
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
import EmployeeTable from './EmployeeTable';
import { FaCheck, FaWindowMinimize } from 'react-icons/fa';

const SalaryOvertimeSheet = () => {
	const globalCompany = useSelector((state) => state.globalCompany);

	const {
		data: employeePersonalDetails,
		isLoading: isLoadingEmployeePersonalDetails,
		isSuccess: isSuccessEmployeePersonalDetails,
	} = useGetEmployeePersonalDetailsQuery(globalCompany);
	console.log(employeePersonalDetails);

	const IndeterminateCheckbox = React.forwardRef(({ indeterminate, ...rest }, ref) => {
		const defaultRef = React.useRef();
		const resolvedRef = ref || defaultRef;

		React.useEffect(() => {
			resolvedRef.current.indeterminate = indeterminate;
		}, [resolvedRef, indeterminate]);

		return (
			<label className="relative flex cursor-pointer flex-col ">
				<input
					type="checkbox"
					ref={resolvedRef}
					className="peer h-5 w-5 appearance-none rounded-md border border-slate-400"
					{...rest}
				/>
				{indeterminate ? (
					<FaWindowMinimize className="absolute left-[3px] bottom-[7px] text-teal-600 dark:text-teal-500" />
				) : (
					<FaCheck className="absolute left-[3px] bottom-[3px] text-teal-600 peer-[&:not(:checked)]:hidden dark:text-teal-500" />
				)}
				{/* {console.log(rest)} */}
				{/* {console.log(indeterminate)} */}
			</label>
		);
	});

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
		}),
		columnHelper.accessor('resignationDate', {
			header: () => 'Resign Date',
			cell: (props) => props.renderValue(),
			enableHiding: true,
		}),
		columnHelper.display({
			id: 'select',
			header: ({ table }) => (
				<IndeterminateCheckbox
					{...{
						checked: table.getIsAllRowsSelected(),
						indeterminate: table.getIsSomeRowsSelected(),
						onChange: table.getToggleAllRowsSelectedHandler(),
					}}
				/>
			),
			cell: ({ row }) => (
				<div>
					<IndeterminateCheckbox
						{...{
							checked: row.getIsSelected(),
							disabled: !row.getCanSelect(),
							indeterminate: row.getIsSomeSelected(),
							onChange: row.getToggleSelectedHandler(),
						}}
					/>
				</div>
			),
		}),
	];

	const [selectedDate, setSelectedDate] = useState({
		year: new Date().getFullYear(),
		month: new Date().getMonth() + 1,
	});
	const data = useMemo(() => {
		if (!employeePersonalDetails) return [];

		const filteredData = employeePersonalDetails.filter((employee) => {
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

	const table = useReactTable({
		data,
		columns,
		initialState: {
			sorting: [{ id: 'name', desc: false }],
			columnVisibility: { dateOfJoining: true, resignationDate: false },
			// rowSelection: { 6: true, 9: true },
		},
		getCoreRowModel: getCoreRowModel(),
		getSortedRowModel: getSortedRowModel(),
		getRowId: (originalRow) => originalRow.id,
		enableSortingRemoval: false,
	});
	useEffect(() => {
		table.toggleAllRowsSelected();
	}, [data]);

	const selectedRows = table.getSelectedRowModel().flatRows;
	console.log(selectedRows);

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
			<div className="flex w-full flex-row gap-8">
				<div className="mt-4 ml-4 w-2/5">
					<EmployeeTable table={table} flexRender={flexRender} />
				</div>
			</div>
		);
	}
};

export default SalaryOvertimeSheet;
