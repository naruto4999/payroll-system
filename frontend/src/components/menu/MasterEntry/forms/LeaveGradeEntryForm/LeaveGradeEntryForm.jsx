import React, { useEffect, useMemo, useState } from 'react';
import {
	createColumnHelper,
	flexRender,
	getCoreRowModel,
	useReactTable,
	getSortedRowModel,
} from '@tanstack/react-table';
import { FaRegTrashAlt, FaPen, FaAngleUp, FaAngleDown } from 'react-icons/fa';
import { useSelector, useDispatch } from 'react-redux';
import {
	useGetLeaveGradesQuery,
	useAddLeaveGradeMutation,
	useUpdateLeaveGradeMutation,
	useDeleteLeaveGradeMutation,
} from '../../../../authentication/api/leaveGradeEntryApiSlice';
import { useOutletContext } from 'react-router-dom';
import ReactModal from 'react-modal';
import { Formik } from 'formik';
import LeaveGradeModal from './LeaveGradeModal';
import { LeaveGradeSchema } from './LeaveGradeSchema';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';

ReactModal.setAppElement('#root');

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const replaceNullWithEmpty = (obj) => {
	const newObj = {};
	for (const key in obj) {
		newObj[key] = obj[key] === null ? '' : obj[key];
	}
	return newObj;
};

const LeaveGradeEntryForm = () => {
	const dispatch = useDispatch();
	const globalCompany = useSelector((state) => state.globalCompany);

	const {
		data: fetchedData,
		isLoading,
		isSuccess,
		isError,
		error,
		isFetching,
		refetch,
	} = useGetLeaveGradesQuery(globalCompany);
	console.log(fetchedData);
	const [addLeaveGrade, { isLoading: isAddingLeaveGrade }] =
		useAddLeaveGradeMutation();
	const [updateLeaveGrade, { isLoading: isUpdatingLeaveGrade }] =
		useUpdateLeaveGradeMutation();
	const [deleteLeaveGrade, { isLoading: isDeletingLeaveGrade }] =
		useDeleteLeaveGradeMutation();
	const [addLeaveGradePopover, setAddLeaveGradePopover] = useState(false);
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();
	const [editLeaveGradePopover, setEditLeaveGradePopover] = useState(false);
	const [updateLeaveGradeId, setUpdateLeaveGradeId] = useState(null);
	const [disabledEdit, setDisableEdit] = useState(false);
	// const [msg, setMsg] = useState("");
	const [errorMessage, setErrorMessage] = useState('');

	const editLeaveGradePopoverHandler = (LeaveGrade) => {
		console.log(LeaveGrade);
		console.log(LeaveGrade.mandatoryLeave);
		setUpdateLeaveGradeId(LeaveGrade.id);
		setDisableEdit(LeaveGrade.mandatoryLeave);
		setEditLeaveGradePopover(!editLeaveGradePopover);
	};

	const cancelButtonClicked = () => {
		setAddLeaveGradePopover(false);
		setErrorMessage('');
		setUpdateLeaveGradeId(null);
		setEditLeaveGradePopover(false);
	};

	const addButtonClicked = async (values, formikBag) => {
		console.log(values);
		let toSend = { ...values };
		if (toSend.limit == '') {
			toSend.limit = null;
		}
		if (toSend.generateFrequency == '') {
			toSend.generateFrequency = null;
		}
		toSend.company = globalCompany.id;

		try {
			const data = await addLeaveGrade(toSend).unwrap();
			console.log(data);
			setErrorMessage('');
			dispatch(
				alertActions.createAlert({
					message: 'Saved',
					type: 'Success',
					duration: 3000,
				})
			);
			cancelButtonClicked();
			formikBag.resetForm();
		} catch (err) {
			console.log(err);
			dispatch(
				alertActions.createAlert({
					message: 'Error Occurred',
					type: 'Error',
					duration: 5000,
				})
			);
			if (err.status === 400) {
				setErrorMessage('Leave grade with this name already exists');
			}
		}
	};

	const updateButtonClicked = async (values, formikBag) => {
		console.log(values);
		let toSend = { ...values };
		if (toSend.limit == '') {
			toSend.limit = null;
		}
		if (toSend.generateFrequency == '') {
			toSend.generateFrequency = null;
		}
		toSend.company = globalCompany.id;
		toSend.id = updateLeaveGradeId;
		try {
			const data = await updateLeaveGrade(toSend).unwrap();
			console.log(data);
			setErrorMessage('');
			dispatch(
				alertActions.createAlert({
					message: 'Saved',
					type: 'Success',
					duration: 3000,
				})
			);
			cancelButtonClicked();
			formikBag.resetForm();
		} catch (err) {
			console.log(err);
			dispatch(
				alertActions.createAlert({
					message: 'Error Occurred',
					type: 'Error',
					duration: 5000,
				})
			);
			if (err.status === 400) {
				setErrorMessage('Leave grade with this name already exists');
			}
		}
	};

	const deleteButtonClicked = async (id) => {
		console.log(id);
		deleteLeaveGrade({ id: id, company: globalCompany.id });
	};

	const columnHelper = createColumnHelper();

	const columns = [
		columnHelper.accessor('id', {
			header: () => 'ID',
			cell: (props) => props.renderValue(),
			//   footer: props => props.column.id,
		}),
		columnHelper.accessor('name', {
			header: () => 'Leave Grade Name',
			cell: (props) => props.renderValue(),
			//   footer: info => info.column.id,
		}),
		columnHelper.accessor('limit', {
			header: () => 'Limit',
			cell: (props) => props.renderValue(),
			//   footer: info => info.column.id,
		}),
		columnHelper.accessor('generateFrequency', {
			header: () => 'Generate Frequency',
			cell: (props) => props.renderValue(),
			//   footer: info => info.column.id,
		}),
		columnHelper.accessor('mandatoryLeave', {
			header: () => 'Mandatory',
			cell: (props) => props.renderValue(),
			enableHiding: true,
			//   footer: info => info.column.id,
		}),
		columnHelper.display({
			id: 'actions',
			header: () => 'Actions',
			cell: (props) => (
				<div className="flex justify-center gap-4">
					{props.row.original.mandatoryLeave ? (
						''
					) : (
						<div
							className="rounded bg-redAccent-500 p-1.5 hover:bg-redAccent-700 dark:bg-redAccent-700 dark:hover:bg-redAccent-500"
							onClick={() =>
								deleteButtonClicked(props.row.original.id)
							}
						>
							<FaRegTrashAlt className="h-4" />
						</div>
					)}
					{props.row.original.mandatoryLeave ? (
						''
					) : (
						<div
							className="rounded bg-teal-600 p-1.5 hover:bg-teal-700 dark:bg-teal-700 dark:hover:bg-teal-600"
							onClick={() =>
								editLeaveGradePopoverHandler(props.row.original)
							}
						>
							<FaPen className="h-4" />
						</div>
					)}
				</div>
			),
		}),
	];

	const data = useMemo(
		() => (fetchedData ? [...fetchedData] : []),
		[fetchedData]
	);
	const table = useReactTable({
		data,
		columns,
		initialState: {
			sorting: [{ id: 'name', desc: false }],
			columnVisibility: { mandatoryLeave: false },
		},
		getCoreRowModel: getCoreRowModel(),
		getSortedRowModel: getSortedRowModel(),
		enableSortingRemoval: false,
	});
	// console.log(tableInstance)
	useEffect(() => {
		setShowLoadingBar(
			isLoading ||
				isAddingLeaveGrade ||
				isDeletingLeaveGrade ||
				isUpdatingLeaveGrade
		);
	}, [
		isLoading,
		isAddingLeaveGrade,
		isDeletingLeaveGrade,
		isUpdatingLeaveGrade,
	]);

	if (globalCompany.id == null) {
		return (
			<section className="flex flex-col items-center">
				<h4 className="text-x mt-10 font-bold text-redAccent-500 dark:text-redAccent-600">
					Please Select a Company First
				</h4>
			</section>
		);
	}
	if (isLoading) {
		return <div></div>;
	} else {
		return (
			<section className="mx-5 mt-2">
				<div className="flex flex-row flex-wrap place-content-between">
					<div className="mr-4">
						<h1 className="text-3xl font-medium">Leave Grades</h1>
						<p className="my-2 text-sm">
							Add more leave grades here
						</p>
					</div>
					<button
						className="my-auto whitespace-nowrap rounded bg-teal-500 p-2 text-base font-medium hover:bg-teal-600 dark:bg-teal-700 dark:hover:bg-teal-600"
						onClick={() => setAddLeaveGradePopover(true)}
					>
						Add Leave Grade
					</button>
				</div>
				<div className="m-5 mx-auto max-w-5xl overflow-hidden rounded border border-black border-opacity-50 shadow-md">
					<table className="w-full border-collapse text-center text-sm">
						<thead className="bg-blueAccent-600 dark:bg-blueAccent-700">
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
						<tbody className="divide-y divide-black divide-opacity-50 border-t border-black border-opacity-50">
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
														cell.column.columnDef
															.cell,
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
					className="items-left fixed inset-0 mx-2 my-auto flex h-fit flex-col gap-4 rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-lg"
					isOpen={addLeaveGradePopover || editLeaveGradePopover}
					onRequestClose={cancelButtonClicked}
					style={{
						overlay: {
							backgroundColor: 'rgba(0, 0, 0, 0.75)',
						},
					}}
				>
					{addLeaveGradePopover && (
						<Formik
							// Remember to divide generateFrequency by two in submission function
							initialValues={{
								name: '',
								limit: '',
								paid: false,
								generateFrequency: '',
							}}
							validationSchema={LeaveGradeSchema}
							onSubmit={addButtonClicked}
							component={(props) => (
								<LeaveGradeModal
									{...props}
									errorMessage={errorMessage}
									setErrorMessage={setErrorMessage}
									setAddLeaveGradePopover={
										setAddLeaveGradePopover
									}
									isEditing={false}
									cancelButtonClicked={cancelButtonClicked}
								/>
							)}
						/>
					)}

					{editLeaveGradePopover && (
						<Formik
							// Remember to divide generateFrequency by two in submission function
							initialValues={replaceNullWithEmpty(
								fetchedData.find(
									(grade) => grade.id === updateLeaveGradeId
								)
							)}
							validationSchema={LeaveGradeSchema}
							onSubmit={updateButtonClicked}
							component={(props) => (
								<LeaveGradeModal
									{...props}
									errorMessage={errorMessage}
									setErrorMessage={setErrorMessage}
									setAddLeaveGradePopover={
										setAddLeaveGradePopover
									}
									disabledEdit={disabledEdit}
									isEditing={true}
									disableEdit={disabledEdit}
									cancelButtonClicked={cancelButtonClicked}
								/>
							)}
						/>
					)}
				</ReactModal>
			</section>
		);
	}
};

export default LeaveGradeEntryForm;
