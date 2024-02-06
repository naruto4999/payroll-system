import React, { useEffect, useMemo, useState } from 'react';
import { createColumnHelper, flexRender, getCoreRowModel, useReactTable } from '@tanstack/react-table';
import { FaRegTrashAlt, FaPen } from 'react-icons/fa';
import { useSelector, useDispatch } from 'react-redux';
import {
	useGetDepartmentsQuery,
	useAddDepartmentMutation,
	useDeleteDepartmentMutation,
	useUpdateDepartmentMutation,
} from '../../../../authentication/api/departmentEntryApiSlice';
import EditDepartment from './EditDepartment';
import { useOutletContext } from 'react-router-dom';
import ReactModal from 'react-modal';
import { Formik } from 'formik';
import AddDepartment from './AddDepartment';
import { addDepartmentSchema, editDepartmentSchema } from './DepartmentEntrySchema';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';

ReactModal.setAppElement('#root');

const DepartmentEntryForm = () => {
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
	} = useGetDepartmentsQuery(globalCompany);
	const [addDepartment, { isLoading: isAddingDepartment }] = useAddDepartmentMutation();
	const [updateDepartment, { isLoading: isUpdatingDepartment }] = useUpdateDepartmentMutation();
	const [deleteDepartment, { isLoading: isDeletingDepartment }] = useDeleteDepartmentMutation();
	const [addDepartmentPopover, setAddDepartmentPopover] = useState(false);
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();
	const [editDepartmentPopover, setEditDepartmentPopover] = useState(false);
	const [updateDepartmentId, setUpdateDepartmentId] = useState('');

	const editDepartmentPopoverHandler = (department) => {
		console.log(department);
		setUpdateDepartmentId(department.id);
		setEditDepartmentPopover(!editDepartmentPopover);
	};

	const addButtonClicked = async (values, formikBag) => {
		try {
			const data = await addDepartment({
				company: globalCompany.id,
				name: values.newDepartment,
			}).unwrap();
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
		formikBag.resetForm();
		setAddDepartmentPopover(!addDepartmentPopover);
	};

	const updateButtonClicked = async (values, formikBag) => {
		try {
			const data = await updateDepartment({
				id: updateDepartmentId,
				name: values.updatedDepartment,
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
			console.log(err);
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

		formikBag.resetForm();
		editDepartmentPopoverHandler({ id: '' });
	};

	const deleteButtonClicked = async (id) => {
		try {
			const data = await deleteDepartment({ id: id, company: globalCompany.id }).unwrap();
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
			header: () => 'Deparment Name',
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
						onClick={() => editDepartmentPopoverHandler(props.row.original)}
					>
						<FaPen className="h-4" />
					</div>
				</div>
			),
		}),
	];

	const data = useMemo(() => (fetchedData ? [...fetchedData] : []), [fetchedData]);

	const table = useReactTable({
		data,
		columns,
		getCoreRowModel: getCoreRowModel(),
	});

	useEffect(() => {
		setShowLoadingBar(isLoading || isAddingDepartment || isDeletingDepartment || isUpdatingDepartment);
	}, [isLoading, isAddingDepartment, isDeletingDepartment, isUpdatingDepartment]);

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
						<h1 className="text-3xl font-medium">Departments</h1>
						<p className="my-2 text-sm">Add more departments here</p>
					</div>
					<button
						className="my-auto whitespace-nowrap rounded bg-teal-500 p-2 text-base font-medium hover:bg-teal-600 dark:bg-teal-700 dark:hover:bg-teal-600"
						onClick={() => setAddDepartmentPopover(true)}
					>
						Add Department
					</button>
				</div>
				<div className="m-5 mx-auto max-w-5xl overflow-hidden rounded border border-black border-opacity-50 shadow-md">
					<table className="w-full border-collapse text-center text-sm">
						<thead className="bg-blueAccent-600 dark:bg-blueAccent-700">
							{table.getHeaderGroups().map((headerGroup) => (
								<tr key={headerGroup.id}>
									{headerGroup.headers.map((header) => (
										<th key={header.id} scope="col" className="px-4 py-4 font-medium">
											{header.isPlaceholder
												? null
												: flexRender(header.column.columnDef.header, header.getContext())}
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
					className="items-left fixed inset-0 mx-2 my-auto flex h-fit flex-col gap-4 rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-lg"
					isOpen={addDepartmentPopover}
					onRequestClose={() => setAddDepartmentPopover(false)}
					style={{
						overlay: {
							backgroundColor: 'rgba(0, 0, 0, 0.75)',
						},
					}}
				>
					<Formik
						initialValues={{ newDepartment: '' }}
						validationSchema={addDepartmentSchema}
						onSubmit={addButtonClicked}
						component={(props) => (
							<AddDepartment {...props} setAddDepartmentPopover={setAddDepartmentPopover} />
						)}
					/>
				</ReactModal>

				<ReactModal
					className="items-left fixed inset-0 mx-2 my-auto flex h-fit flex-col gap-4 rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-lg"
					isOpen={editDepartmentPopover}
					onRequestClose={() => editDepartmentPopoverHandler({ id: '' })}
					style={{
						overlay: {
							backgroundColor: 'rgba(0, 0, 0, 0.75)',
						},
					}}
				>
					<Formik
						initialValues={{ updatedDepartment: '' }}
						validationSchema={editDepartmentSchema}
						onSubmit={updateButtonClicked}
						component={(props) => (
							<EditDepartment {...props} editDepartmentPopoverHandler={editDepartmentPopoverHandler} />
						)}
					/>
				</ReactModal>
			</section>
		);
	}
};

export default DepartmentEntryForm;
