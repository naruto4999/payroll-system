import React, { useMemo, useEffect } from 'react';
import {
	useGetEmployeePersonalDetailsQuery,
	useUpdateVisibleEmployeesMutation,
} from '../../../authentication/api/employeeEntryApiSlice';
import { useDispatch, useSelector } from 'react-redux';
import { FaRegTrashAlt, FaPen, FaAngleUp, FaAngleDown, FaEye } from 'react-icons/fa';
import { FaCheck, FaWindowMinimize } from 'react-icons/fa';
import {
	createColumnHelper,
	flexRender,
	getCoreRowModel,
	useReactTable,
	getSortedRowModel,
} from '@tanstack/react-table';
import { alertActions } from '../../../authentication/store/slices/alertSlice';
import { useOutletContext } from 'react-router-dom';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

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

const VisibleEmployeesForm = () => {
	const globalCompany = useSelector((state) => state.globalCompany);
	const dispatch = useDispatch();
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();

	const {
		data: employeePersonalDetails,
		isLoading: isLoadingEmployeePersonalDetails,
		isSuccess: isSuccessEmployeePersonalDetails,
	} = useGetEmployeePersonalDetailsQuery(globalCompany);
	console.log(employeePersonalDetails);

	const [updateVisibleEmployees, { isLoading: isUpdatingVisibleEmployees }] = useUpdateVisibleEmployeesMutation();

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
			// enableHiding: true,
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

	const data = useMemo(() => (employeePersonalDetails ? employeePersonalDetails : []), [employeePersonalDetails]);

	const table = useReactTable({
		data,
		columns,
		enableRowSelection: true,
		initialState: {
			sorting: [{ id: 'name', desc: false }],
			columnVisibility: { dateOfJoining: true, resignationDate: true },
			// rowSelection: { 6: true, 9: true },
		},
		getCoreRowModel: getCoreRowModel(),
		getSortedRowModel: getSortedRowModel(),
		// getRowId: (originalRow) => originalRow.id,
		// enableSortingRemoval: false,
	});

	const saveButtonClicked = async () => {
		const employees_id = [];
		const selectedRows = table.getSelectedRowModel().flatRows;
		console.log(selectedRows);
		for (let i = 0; i < selectedRows.length; i++) {
			const original = selectedRows[i].original;
			employees_id.push(original.id);
		}
		try {
			const data = await updateVisibleEmployees({
				employees_id: employees_id,
				company: globalCompany.id,
			}).unwrap();
			dispatch(
				alertActions.createAlert({
					message: 'Saved',
					type: 'Success',
					duration: 3000,
				})
			);
		} catch (err) {
			let message = 'Error Occurred';
			if (err?.data?.error) {
				message = err?.data?.error;
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

	useEffect(() => {
		setShowLoadingBar(isLoadingEmployeePersonalDetails || isUpdatingVisibleEmployees);
	}, [isLoadingEmployeePersonalDetails, isUpdatingVisibleEmployees]);

	useEffect(() => {
		if (data?.length > 0) {
			console.log('yes length is greater');
			for (let i = 0; i < data.length; i++) {
				table.setRowSelection(data?.map((item) => item.visible));
			}
		}
	}, [data]);

	return (
		<section className="mx-5 mt-2">
			<div className="flex flex-row flex-wrap place-content-between">
				<div className="mr-4">
					<h1 className="text-3xl font-medium">Employees In Sub User Account</h1>
					<p className="my-2 text-sm">Manage the visibility of employees in sub user account here</p>
				</div>
				<button
					className="my-auto whitespace-nowrap rounded bg-teal-500 p-2 text-base font-medium hover:bg-teal-600 dark:bg-teal-700 dark:hover:bg-teal-600"
					onClick={saveButtonClicked}
				>
					Save
				</button>
			</div>
			{/* <div className="scrollbar mx-auto max-h-[80dvh] max-w-full overflow-y-auto rounded border border-black border-opacity-50 shadow-md lg:max-h-[80dvh]"> */}
			<div className="scrollbar mx-auto max-h-[80dvh] max-w-6xl overflow-y-auto rounded border border-black border-opacity-50 shadow-md lg:max-h-[84dvh]">
				<table className="w-full border-collapse text-center text-xs">
					<thead className="sticky top-0 z-20 bg-blueAccent-600 dark:bg-blueAccent-700">
						{table.getHeaderGroups().map((headerGroup) => (
							<tr key={headerGroup.id}>
								{headerGroup.headers.map((header) => (
									<th key={header.id} scope="col" className="px-4 py-2 font-medium">
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
													{flexRender(header.column.columnDef.header, header.getContext())}

													{header.column.getCanSort() ? (
														<div className="relative pl-2">
															<FaAngleUp
																className={classNames(
																	header.column.getIsSorted() == 'asc'
																		? 'text-teal-700'
																		: '',
																	'absolute -translate-y-2 text-sm'
																)}
															/>
															<FaAngleDown
																className={classNames(
																	header.column.getIsSorted() == 'desc'
																		? 'text-teal-700'
																		: '',
																	'absolute translate-y-2 text-sm'
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
					<tbody className="max-h-20 divide-y divide-black divide-opacity-50 overflow-y-auto border-t border-black border-opacity-50 ">
						{table.getRowModel().rows.map((row) => (
							<tr
								// className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50"
								className={`hover:bg-zinc-200 dark:hover:bg-zinc-800 ${
									row.original.resignationDate ? 'text-redAccent-500' : ''
								}`}
								key={row.id}
								id={row.id}
								// tabIndex={-1}
								// data-row-id={row.original.id}
								// onClick={(e) => {
								// 	onRowClick(e, row);
								// }}
							>
								{row.getVisibleCells().map((cell) => (
									<td className="relative px-4 py-2 font-normal" key={cell.id}>
										<div className="text-xs">
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
		</section>
	);
};

export default VisibleEmployeesForm;
