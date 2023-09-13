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
import { useOutletContext } from 'react-router-dom';
import ReactModal from 'react-modal';
import { Formik } from 'formik';
import { useDispatch, useSelector } from 'react-redux';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
// import EditSalary from './EditSalary';
import * as yup from 'yup';
// import { generateEmployeeSalarySchema } from './EmployeeSalarySchema';
import EditAdvance from './EditAdvance';
import {
	useAddEmployeeAdvancePaymentsMutation,
	useUpdateEmployeeAdvancePaymentsMutation,
	useDeleteEmployeeAdvancePaymentsMutation,
} from '../../../../authentication/api/advanceUpdationApiSlice';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const AdvanceUpdationForm = () => {
	const dispatch = useDispatch();
	const globalCompany = useSelector((state) => state.globalCompany);

	const [editEmployeeAdvanceModal, setEditEmployeeAdvanceModal] = useState(false);
	const [updateEmployeeId, setUpdateEmployeeId] = useState(null);

	const {
		data: fetchedData,
		isLoading,
		isSuccess,
		isError,
		error,
		isFetching,
		refetch,
	} = useGetEmployeePersonalDetailsQuery(globalCompany);

	const cancelButtonClicked = () => {
		setEditEmployeeAdvanceModal(false);
		setUpdateEmployeeId(null);
	};

	const [
		addEmployeeAdvancePayments,
		{
			isLoading: isAddingEmployeeAdvancePayments,
			// isError: errorRegisteringRegular,
			isSuccess: isAddEmployeeAdvancePaymentsSuccess,
		},
	] = useAddEmployeeAdvancePaymentsMutation();

	const [
		deleteEmployeeAdvancePayments,
		{
			isLoading: isDeletingEmployeeAdvancePayments,
			// isError: errorRegisteringRegular,
			isSuccess: isDeleteEmployeeAdvancePaymentsSuccess,
		},
	] = useDeleteEmployeeAdvancePaymentsMutation();

	const [
		updateEmployeeAdvancePayments,
		{
			isLoading: isUpdatingEmployeeAdvancePayments,
			// isError: errorRegisteringRegular,
			isSuccess: isUpdateAddEmployeeAdvancePaymentsSuccess,
		},
	] = useUpdateEmployeeAdvancePaymentsMutation();

	const editEmployeeAdvancePopoverHandler = async (personalDetail) => {
		console.log(personalDetail);
		// const year = new Date(personalDetail.dateOfJoining).getFullYear();
		// const month = new Date(personalDetail.dateOfJoining).getMonth() + 1; // Adding 1 because getMonth() returns values from 0 to 11.
		// console.log(month);

		// setYearOfJoining(year);
		// setMonthOfJoining(month);
		setUpdateEmployeeId(personalDetail.id);
		// setFirstRender(true);
		setEditEmployeeAdvanceModal(true);
	};

	const updateButtonClicked = useCallback(async (values, formikBag) => {
		console.log(values);
		const objectsWithId = [];
		const objectsWithoutId = [];

		values.employeeAdvanceDetails.forEach((item) => {
			if ('id' in item) {
				objectsWithId.push(item);
			} else {
				objectsWithoutId.push({ ...item, company: globalCompany.id, employee: updateEmployeeId });
			}
		});

		console.log("Objects with 'id' key:", objectsWithId);
		console.log("Objects without 'id' key:", objectsWithoutId);
		let toCreate = {
			employeeAdvanceDetails: objectsWithoutId,
			company: globalCompany.id,
			employee: updateEmployeeId,
		};
		let toUpdate = {
			employeeAdvanceDetails: objectsWithId,
			company: globalCompany.id,
			employee: updateEmployeeId,
		};

		try {
			const data = await addEmployeeAdvancePayments(toCreate).unwrap();
			const updateddData = await updateEmployeeAdvancePayments(toUpdate).unwrap();
			if (values.detailsToDelete.length != 0) {
				const deletedData = await deleteEmployeeAdvancePayments({
					company: globalCompany.id,
					employee: updateEmployeeId,
					detailsToDelete: [...values.detailsToDelete],
				}).unwrap();
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
	});

	// const advanceInitialValues = {
	// 	principal: 0,
	// 	date: '',
	// 	emi: 0,
	// 	tenureMonths: 'Father',
	// 	repaidAmount: false,
	// };

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
		columnHelper.accessor('resignationDate', {
			header: () => 'Resign Date',
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
							editEmployeeAdvancePopoverHandler(props.row.original);
						}}
					>
						<FaPen className="h-4 text-white" />
					</div>
				</div>
			),
		}),
	];

	const data = useMemo(() => (fetchedData ? [...fetchedData] : []), [fetchedData]);

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
	} else if (isLoading) {
		return <div></div>;
	} else {
		return (
			<section className="mx-5 mt-2">
				<div className="flex flex-row flex-wrap place-content-between">
					<div className="mr-4">
						<h1 className="text-3xl font-medium">Advance Updation</h1>
						<p className="my-2 text-sm">Add and manage advance payments made to employees here</p>
					</div>
					{/* <button
							className="my-auto whitespace-nowrap rounded bg-teal-500 p-2 text-base font-medium hover:bg-teal-600 dark:bg-teal-700 dark:hover:bg-teal-600"
							onClick={() => addEmployeePopoverHandler('addEmployeePersonalDetail')}
						>
							Add Employee
						</button> */}
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
								<tr
									className={`hover:bg-zinc-200 dark:hover:bg-zinc-800 ${
										row.original.resignationDate ? 'text-redAccent-500' : ''
									}`}
									key={row.id}
								>
									{console.log(row.original.resignationDate)}
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
					className="items-left scrollbar fixed inset-0 mx-2 my-auto flex h-fit max-h-[100dvh] w-fit flex-col gap-4 overflow-y-scroll rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-[1100px]"
					isOpen={editEmployeeAdvanceModal}
					onRequestClose={cancelButtonClicked}
					style={{
						overlay: {
							backgroundColor: 'rgba(0, 0, 0, 0.75)',
						},
					}}
				>
					<Formik
						initialValues={{ employeeAdvanceDetails: [], detailsToDelete: [] }}
						validationSchema={''}
						onSubmit={updateButtonClicked}
						component={(props) => (
							<EditAdvance
								{...props}
								globalCompany={globalCompany}
								updateEmployeeId={updateEmployeeId}
								cancelButtonClicked={cancelButtonClicked}
								// yearOfJoining={yearOfJoining}
								// updateEmployeeSalaryId={updateEmployeeSalaryId}
								// fetchedEarningsHeads={fetchedEarningsHeads}
								// firstRender={firstRender}
								// setFirstRender={setFirstRender}
								// monthOfJoining={monthOfJoining}
								// cancelButtonClicked={cancelButtonClicked}
							/>
						)}
					/>
				</ReactModal>
			</section>
		);
	}
};
export default AdvanceUpdationForm;
