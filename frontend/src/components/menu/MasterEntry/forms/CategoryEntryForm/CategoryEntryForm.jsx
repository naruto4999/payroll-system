import React, { useEffect, useMemo, useState } from 'react';
import { createColumnHelper, flexRender, getCoreRowModel, useReactTable } from '@tanstack/react-table';
import { FaRegTrashAlt, FaPen } from 'react-icons/fa';
import { useSelector, useDispatch } from 'react-redux';
import {
	useGetCategoriesQuery,
	useAddCategoryMutation,
	useUpdateCategoryMutation,
	useDeleteCategoryMutation,
} from '../../../../authentication/api/categoryEntryApiSlice';
import EditCategory from './EditCategory';
import { useOutletContext } from 'react-router-dom';
import ReactModal from 'react-modal';
import { Formik } from 'formik';
import AddCategory from './AddCategory';
import { addCategorySchema, editCategorySchema } from './CategoryEntrySchema';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';

ReactModal.setAppElement('#root');

const CategoryEntryForm = () => {
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
	} = useGetCategoriesQuery(globalCompany);
	// console.log(fetchedData)
	const [addCategory, { isLoading: isAddingCategory }] = useAddCategoryMutation();
	const [updateCategory, { isLoading: isUpdatingCategory }] = useUpdateCategoryMutation();
	const [deleteCategory, { isLoading: isDeletingCategory }] = useDeleteCategoryMutation();
	const [addCategoryPopover, setAddCategoryPopover] = useState(false);
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();
	const [editCategoryPopover, setEditCategoryPopover] = useState(false);
	const [updateCategoryId, setUpdateCategoryId] = useState('');
	const [msg, setMsg] = useState('');

	console.log(updateCategoryId);

	const editCategoryPopoverHandler = (category) => {
		console.log(category);
		setUpdateCategoryId(category.id);
		setEditCategoryPopover(!editCategoryPopover);
	};

	const addButtonClicked = async (values, formikBag) => {
		try {
			const data = await addCategory({
				company: globalCompany.id,
				name: values.newCategory,
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

		setAddCategoryPopover(!addCategoryPopover);
		formikBag.resetForm();
	};

	const updateButtonClicked = async (values, formikBag) => {
		try {
			const data = await updateCategory({
				id: updateCategoryId,
				name: values.updatedCategory,
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
		editCategoryPopoverHandler({ id: '' });
	};

	const deleteButtonClicked = async (id) => {
		try {
			const data = await deleteCategory({ id: id, company: globalCompany.id }).unwrap();
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
		}),
		columnHelper.accessor('name', {
			header: () => 'Category Name',
			cell: (props) => props.renderValue(),
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
						onClick={() => editCategoryPopoverHandler(props.row.original)}
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
		setShowLoadingBar(isLoading || isAddingCategory || isDeletingCategory || isUpdatingCategory);
	}, [isLoading, isAddingCategory, isDeletingCategory, isUpdatingCategory]);

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
						<h1 className="text-3xl font-medium">Categories</h1>
						<p className="my-2 text-sm">Add more categories here</p>
					</div>
					<button
						className="my-auto whitespace-nowrap rounded bg-teal-500 p-2 text-base font-medium hover:bg-teal-600 dark:bg-teal-700 dark:hover:bg-teal-600"
						onClick={() => setAddCategoryPopover(true)}
					>
						Add Category
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
					isOpen={addCategoryPopover}
					onRequestClose={() => setAddCategoryPopover(false)}
					style={{
						overlay: {
							backgroundColor: 'rgba(0, 0, 0, 0.75)',
						},
					}}
				>
					<Formik
						initialValues={{ newCategory: '' }}
						validationSchema={addCategorySchema}
						onSubmit={addButtonClicked}
						component={(props) => <AddCategory {...props} setAddCategoryPopover={setAddCategoryPopover} />}
					/>
				</ReactModal>

				<ReactModal
					className="items-left fixed inset-0 mx-2 my-auto flex h-fit flex-col gap-4 rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-lg"
					isOpen={editCategoryPopover}
					onRequestClose={() => editCategoryPopoverHandler({ id: '' })}
					style={{
						overlay: {
							backgroundColor: 'rgba(0, 0, 0, 0.75)',
						},
					}}
				>
					<Formik
						initialValues={{ updatedCategory: '' }}
						validationSchema={editCategorySchema}
						onSubmit={updateButtonClicked}
						component={(props) => (
							<EditCategory {...props} editCategoryPopoverHandler={editCategoryPopoverHandler} />
						)}
					/>
				</ReactModal>
			</section>
		);
	}
};

export default CategoryEntryForm;
