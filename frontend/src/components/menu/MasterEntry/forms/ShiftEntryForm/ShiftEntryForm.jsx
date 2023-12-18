import React, { useEffect, useMemo, useState } from 'react';
import {
	createColumnHelper,
	flexRender,
	getCoreRowModel,
	useReactTable,
	getSortedRowModel,
} from '@tanstack/react-table';
import { FaRegTrashAlt, FaPen, FaAngleUp, FaAngleDown, FaEye } from 'react-icons/fa';
import { useSelector, useDispatch } from 'react-redux';
import {
	useGetShiftsQuery,
	useAddShiftMutation,
	useUpdateShiftMutation,
	useDeleteShiftMutation,
} from '../../../../authentication/api/shiftEntryApiSlice';
import ViewShift from './ViewShift';
import { useOutletContext } from 'react-router-dom';
import ReactModal from 'react-modal';
import { Formik } from 'formik';
import ShiftModal from './ShiftModal';
import { ShiftSchema } from './ShiftEntrySchema';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';

ReactModal.setAppElement('#root');

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const replaceNullWithEmpty = (obj) => {
	const newObj = {};
	console.log(obj);
	for (const key in obj) {
		newObj[key] = obj[key] === null ? '' : obj[key];
	}
	return newObj;
};

const ShiftEntryForm = () => {
	const dispatch = useDispatch();
	const globalCompany = useSelector((state) => state.globalCompany);

	console.log(globalCompany);
	const {
		data: fetchedData,
		isLoading,
		isSuccess,
		isError,
		error,
		isFetching,
		refetch,
	} = useGetShiftsQuery(globalCompany);
	// console.log(fetchedData)
	const [addShift, { isLoading: isAddingShift }] = useAddShiftMutation();
	const [updateShift, { isLoading: isUpdatingShift }] = useUpdateShiftMutation();
	const [deleteShift, { isLoading: isDeletingShift }] = useDeleteShiftMutation();
	const [addShiftPopover, setAddShiftPopover] = useState(false);
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();
	const [editShiftPopover, setEditShiftPopover] = useState(false);
	const [viewShiftPopover, setViewShiftPopover] = useState(false);
	const [updateShiftId, setUpdateShiftId] = useState('');
	// const [msg, setMsg] = useState("");
	const [errorMessage, setErrorMessage] = useState('');

	const [viewShiftId, setViewShiftId] = useState('');

	const editShiftPopoverHandler = (shift) => {
		console.log(shift);
		setUpdateShiftId(shift.id);
		setEditShiftPopover(!editShiftPopover);
	};

	const viewShiftPopoverHandler = (shift) => {
		console.log(shift);
		setViewShiftPopover(!viewShiftPopover);
		setViewShiftId(shift.id);
	};

	const cancelButtonClicked = () => {
		setAddShiftPopover(false);
		setErrorMessage('');
		setUpdateShiftId(null);
		setEditShiftPopover(false);
	};

	const addButtonClicked = async (values, formikBag) => {
		console.log(values);
		try {
			const data = await addShift({
				...values,
				company: globalCompany.id,
			}).unwrap();
			formikBag.resetForm();
			dispatch(
				alertActions.createAlert({
					message: 'Saved',
					type: 'Success',
					duration: 3000,
				})
			);
			cancelButtonClicked();
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
				setErrorMessage('Shift with this name already exists');
			} else {
				console.log(err);
			}
		}
	};

	const updateButtonClicked = async (values, formikBag) => {
		console.log(values);
		try {
			const data = await updateShift({
				...values,
				id: updateShiftId,
				company: globalCompany.id,
			}).unwrap();
			formikBag.resetForm();
			dispatch(
				alertActions.createAlert({
					message: 'Saved',
					type: 'Success',
					duration: 3000,
				})
			);
			cancelButtonClicked();
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
				setErrorMessage('Shift with this name already exists');
			} else {
				console.log(err);
			}
		}
	};

	const deleteButtonClicked = async (id) => {
		console.log(id);
		deleteShift({ id: id, company: globalCompany.id });
	};

	const columnHelper = createColumnHelper();

	const columns = [
		columnHelper.accessor('id', {
			header: () => 'ID',
			cell: (props) => props.renderValue(),
			//   footer: props => props.column.id,
		}),
		columnHelper.accessor('name', {
			header: () => 'Shift Name',
			cell: (props) => props.renderValue(),
			//   footer: info => info.column.id,
		}),
		columnHelper.display({
			id: 'actions',
			header: () => 'Actions',
			cell: (props) => (
				<div className="flex justify-center gap-4">
					<div
						className="rounded bg-redAccent-500 p-1.5 hover:bg-redAccent-700 dark:bg-redAccent-700 dark:hover:bg-redAccent-500"
						onClick={() => deleteButtonClicked(props.row.original.id)}
					>
						<FaRegTrashAlt className="h-4" />
					</div>
					<div
						className="rounded bg-teal-600 p-1.5 hover:bg-teal-700 dark:bg-teal-700 dark:hover:bg-teal-600"
						onClick={() => editShiftPopoverHandler(props.row.original)}
					>
						<FaPen className="h-4" />
					</div>
					<div
						className="rounded bg-blueAccent-600 p-1.5 hover:bg-blueAccent-700 dark:bg-blueAccent-600 dark:hover:bg-blueAccent-500"
						onClick={() => viewShiftPopoverHandler(props.row.original)}
					>
						<FaEye className="h-4" />
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

	useEffect(() => {
		// Add more for adding, editing and deleting later on
		setShowLoadingBar(isLoading || isAddingShift || isUpdatingShift || isDeletingShift);
	}, [isLoading, isAddingShift, isUpdatingShift, isDeletingShift]);

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
						<h1 className="text-3xl font-medium">Shifts</h1>
						<p className="my-2 text-sm">Add more shifts here</p>
					</div>
					<button
						className="my-auto whitespace-nowrap rounded bg-teal-500 p-2 text-base font-medium hover:bg-teal-600 dark:bg-teal-700 dark:hover:bg-teal-600"
						onClick={() => setAddShiftPopover(true)}
					>
						Add Shift
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

														{console.log(header.column.getIsSorted())}
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

				<ReactModal
					className="items-left fixed inset-0 mx-2 my-auto flex h-fit flex-col gap-4 rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-2xl"
					isOpen={addShiftPopover || editShiftPopover}
					onRequestClose={cancelButtonClicked}
					style={{
						overlay: {
							backgroundColor: 'rgba(0, 0, 0, 0.75)',
						},
					}}
				>
					<Formik
						initialValues={
							addShiftPopover
								? {
										name: '',
										beginningTime: '',
										endTime: '',
										lunchDuration: '',
										lunchBeginningTime: '',
										teaTime: '',
										lateGrace: '',
										otBeginAfter: '',
										nextShiftDelay: '',
										accidentalPunchBuffer: '',
										halfDayMinimumMinutes: '',
										fullDayMinimumMinutes: '',
										shortLeaves: '',
										maxLateAllowedMin: '',
								  }
								: replaceNullWithEmpty(fetchedData.find((shift) => shift.id === updateShiftId))
						}
						validationSchema={ShiftSchema}
						onSubmit={addShiftPopover ? addButtonClicked : updateButtonClicked}
						component={(props) => (
							<ShiftModal
								{...props}
								errorMessage={errorMessage}
								setErrorMessage={setErrorMessage}
								cancelButtonClicked={cancelButtonClicked}
								isEditing={editShiftPopover}
							/>
						)}
					/>
				</ReactModal>

				<ReactModal
					className="items-left fixed inset-0 mx-2 my-auto flex h-fit flex-col gap-4 rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-2xl"
					isOpen={viewShiftPopover}
					onRequestClose={() =>
						viewShiftPopoverHandler({
							id: null,
						})
					}
					style={{
						overlay: {
							backgroundColor: 'rgba(0, 0, 0, 0.75)',
						},
					}}
				>
					<ViewShift
						shift={viewShiftId ? fetchedData.find((shift) => shift.id === viewShiftId) : null}
						viewShiftPopoverHandler={viewShiftPopoverHandler}
					/>
				</ReactModal>
			</section>
		);
	}
};

export default ShiftEntryForm;
