import React, { useMemo, useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
	createColumnHelper,
	flexRender,
	getCoreRowModel,
	useReactTable,
	getSortedRowModel,
} from '@tanstack/react-table';
import { FaRegTrashAlt, FaPen, FaCircleNotch, FaCheck, FaWindowMinimize, FaAngleUp, FaAngleDown } from 'react-icons/fa';
import { useOutletContext } from 'react-router-dom';
import { alertActions } from '../../../authentication/store/slices/alertSlice';

//imports after using RTK query
import { useGetCompaniesQuery, useVisibleCompanyMutation } from '../../../authentication/api/newCompanyEntryApiSlice';
import ReactModal from 'react-modal';
import { Formik } from 'formik';

ReactModal.setAppElement('#root');

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

const VisibleCompaniesForm = () => {
	//using RTK query
	const { data: fetchedData, isLoading, isSuccess, isError, error, isFetching } = useGetCompaniesQuery();
	console.log(fetchedData);
	const [visibleCompany, { isLoading: isUpdatingVisibleCompanies }] = useVisibleCompanyMutation();
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();
	const [confirmDelete, setConfirmDelete] = useState({ id: '', phrase: '' });
	const dispatch = useDispatch();

	const [updatedCompanyId, setUpdatedCompanyId] = useState();

	const editCompanyPopoverHandler = (company) => {
		setUpdatedCompanyId(company.id);
		setEditCompanyPopover(!editCompanyPopover);
	};

	const saveButtonClicked = async () => {
		const body = [];
		const selectedRows = table.getSelectedRowModel().flatRows;
		console.log(selectedRows);
		for (let i = 0; i < selectedRows.length; i++) {
			const original = selectedRows[i].original;
			body.push({
				company_id: original.id,
				visible: true,
			});
		}
		try {
			const data = await visibleCompany(body).unwrap();
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
	const columnHelper = createColumnHelper();

	const columns = [
		columnHelper.accessor('id', {
			header: () => 'ID',
			cell: (props) => props.renderValue(),
			//   footer: props => props.column.id,
		}),
		columnHelper.accessor('name', {
			header: () => 'Company Head Name',
			cell: (props) => props.renderValue(),
			//   footer: info => info.column.id,
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

	const data = useMemo(() => (fetchedData ? [...fetchedData] : []), [fetchedData]);

	const table = useReactTable({
		data,
		columns,
		enableRowSelection: true,
		initialState: {
			sorting: [{ id: 'name', desc: true }],
		},
		getCoreRowModel: getCoreRowModel(),
		getSortedRowModel: getSortedRowModel(),
	});
	console.log(table);
	useEffect(() => {
		setShowLoadingBar(isLoading || isUpdatingVisibleCompanies);
	}, [isLoading, isUpdatingVisibleCompanies]);

	useEffect(() => {
		if (fetchedData?.length > 0) {
			for (let i = 0; i < fetchedData.length; i++) {
				table.setRowSelection(fetchedData?.map((item) => item.visible));
			}
		}
	}, [fetchedData]);

	if (isLoading) {
		return (
			<div className="fixed inset-0 z-50 mx-auto my-auto flex h-fit w-fit items-center rounded bg-indigo-600 p-2 font-medium">
				<FaCircleNotch className="mr-2 animate-spin text-white" />
				Processing...
			</div>
		);
	} else {
		return (
			<section className="mx-5 mt-2">
				<div className="flex flex-row place-content-between">
					<div className="">
						<h1 className="text-3xl font-medium">Companies in Sub User Account</h1>
						<p className="my-2 text-sm">Manage the visibility of companies in sub user account here</p>
					</div>
					<button
						className="my-4 rounded bg-teal-500 p-2 text-base font-medium hover:bg-teal-600 dark:bg-teal-700 dark:hover:bg-teal-600"
						onClick={saveButtonClicked}
					>
						Save
					</button>
				</div>
				<div className="m-5 mx-auto max-w-5xl overflow-hidden rounded border border-black border-opacity-50 shadow-md">
					<table className="w-full border-collapse text-center text-sm">
						<thead className="bg-blueAccent-600 dark:bg-blueAccent-700">
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

														{/* {console.log(
                                                            header.column.getIsSorted()
                                                        )} */}
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
						<tbody className="divide-y divide-black divide-opacity-50 border-t border-black border-opacity-50">
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
			</section>
		);
	}
};

export default VisibleCompaniesForm;
