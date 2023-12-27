import React, { useMemo } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useState } from 'react';
import { createColumnHelper, flexRender, getCoreRowModel, useReactTable } from '@tanstack/react-table';
import { FaRegTrashAlt, FaPen, FaCircleNotch } from 'react-icons/fa';
import EditCompany from './EditCompany';
import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';
import { globalCompanyActions } from '../../../../authentication/store/slices/globalCompany';
import AddCompany from './AddCompany';
import DeleteCompany from './DeleteCompany';
import { addCompanySchema, editCompanySchema } from './NewCompanyEntrySchema';

//imports after using RTK query
import {
	useGetCompaniesQuery,
	useAddCompaniesMutation,
	useDeleteCompanyMutation,
	useUpdateCompaniesMutation,
} from '../../../../authentication/api/newCompanyEntryApiSlice';
import { useUpdateCompanyDetailsMutation } from '../../../../authentication/api/companyEntryApiSlice';
import ReactModal from 'react-modal';
import { Formik } from 'formik';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';

ReactModal.setAppElement('#root');

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const NewCompanyEntryForm = () => {
	//using RTK query
	const { data: fetchedData, isLoading, isSuccess, isError, error, isFetching } = useGetCompaniesQuery();
	const [addCompanies, { isLoading: isAddingCompany }] = useAddCompaniesMutation();
	const [deleteCompany, { isLoading: isDeletingComapny }] = useDeleteCompanyMutation();
	const [updateCompany, { isLoading: isUpdatingCompany }] = useUpdateCompaniesMutation();
	const [addCompanyPopover, setAddCompanyPopover] = useState(false);
	const [editCompanyPopover, setEditCompanyPopover] = useState(false);
	const [deleteCompanyPopover, setDeleteCompanyPopover] = useState(false);
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();
	const [confirmDelete, setConfirmDelete] = useState({ id: '', phrase: '' });
	const dispatch = useDispatch();

	const globalCompany = useSelector((state) => state.globalCompany);
	const [newCompany, setNewCompany] = useState('');
	const [updatedCompanyId, setUpdatedCompanyId] = useState();

	const editCompanyPopoverHandler = (company) => {
		setUpdatedCompanyId(company.id);
		setEditCompanyPopover(!editCompanyPopover);
	};

	const deleteCompanyChangeHandler = (event) => {
		setConfirmDelete((prevState) => {
			return { ...prevState, phrase: event.target.value.toLowerCase() };
		});
	};

	const addButtonClicked = async (values, formikBag) => {
		console.log(values);
		try {
			const data = await addCompanies({
				name: values.newCompany,
			}).unwrap();
			dispatch(
				alertActions.createAlert({
					message: `Success`,
					type: 'Success',
					duration: 3000,
				})
			);
			setAddCompanyPopover(!addCompanyPopover);
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
		// addCompanies({
		// 	name: values.newCompany,
		// });
		formikBag.resetForm();
	};

	const updateButtonClicked = async (values, formikBag) => {
		console.log(values);
		updateCompany({
			id: updatedCompanyId,
			name: values.updatedCompany,
		});
		formikBag.resetForm();
		editCompanyPopoverHandler({ id: '' });
	};

	const deleteButtonClicked = async (e) => {
		e.preventDefault();
		if (confirmDelete.phrase == 'confirm') {
			deleteCompany({ id: confirmDelete.id });
			setDeleteCompanyPopover(false);
			if (globalCompany.id == confirmDelete.id) {
				dispatch(globalCompanyActions.deselectComapny());
			}
		}
	};
	console.log(confirmDelete);

	const columnHelper = createColumnHelper();

	const columns = [
		columnHelper.accessor('id', {
			header: () => 'ID',
			cell: (props) => props.renderValue(),
			//   footer: props => props.column.id,
		}),
		columnHelper.accessor('name', {
			header: () => 'Company Name',
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
						onClick={() => {
							setConfirmDelete({
								id: props.row.original.id,
								phrase: '',
							});
							setDeleteCompanyPopover(true);
						}}
					>
						<FaRegTrashAlt className="h-4" />
					</div>
					<div
						className="rounded bg-teal-600 p-1.5 hover:bg-teal-700 dark:bg-teal-700 dark:hover:bg-teal-600"
						onClick={() => editCompanyPopoverHandler(props.row.original)}
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
		setShowLoadingBar(isAddingCompany || isDeletingComapny || isUpdatingCompany);
	}, [isAddingCompany, isDeletingComapny, isUpdatingCompany]);

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
						<h1 className="text-3xl font-medium">Companies</h1>
						<p className="my-2 text-sm">Add more companies here</p>
					</div>
					<button
						className="my-4 rounded bg-teal-500 p-2 text-base font-medium hover:bg-teal-600 dark:bg-teal-700 dark:hover:bg-teal-600"
						onClick={() => setAddCompanyPopover(true)}
					>
						Add Company
					</button>
				</div>

				<div className={`m-5 mx-auto overflow-hidden rounded border border-black border-opacity-50 shadow-md`}>
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
					isOpen={addCompanyPopover}
					onRequestClose={() => setAddCompanyPopover(false)}
					style={{
						overlay: {
							backgroundColor: 'rgba(0, 0, 0, 0.75)',
						},
					}}
				>
					<Formik
						initialValues={{ newCompany: '' }}
						validationSchema={addCompanySchema}
						onSubmit={addButtonClicked}
						component={(props) => <AddCompany {...props} setAddCompanyPopover={setAddCompanyPopover} />}
					/>
				</ReactModal>

				{/* <ReactModal
                    className="fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-lg h-fit bg-zinc-300 dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl"
                    isOpen={editCompanyPopover}
                    onRequestClose={() => setEditCompanyPopover(false)}
                    style={{
                        overlay: {
                            backgroundColor: "rgba(0, 0, 0, 0.75)",
                        },
                    }}
                >
                    <EditCompany
                        editCompanyPopoverHandler={editCompanyPopoverHandler}
                        updatedCompanyChangeHandler={
                            updatedCompanyChangeHandler
                        }
                        updateButtonClicked={updateButtonClicked}
                    />
                </ReactModal> */}

				<ReactModal
					className="items-left fixed inset-0 mx-2 my-auto flex h-fit flex-col gap-4 rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-lg"
					isOpen={editCompanyPopover}
					onRequestClose={() => editCompanyPopoverHandler({ id: '' })}
					style={{
						overlay: {
							backgroundColor: 'rgba(0, 0, 0, 0.75)',
						},
					}}
				>
					<Formik
						initialValues={{ updatedCompany: '' }}
						validationSchema={editCompanySchema}
						onSubmit={updateButtonClicked}
						component={(props) => (
							<EditCompany {...props} editCompanyPopoverHandler={editCompanyPopoverHandler} />
						)}
					/>
				</ReactModal>

				<ReactModal
					className="items-left fixed inset-0 mx-2 my-auto flex h-fit flex-col gap-4 rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-lg"
					isOpen={deleteCompanyPopover}
					onRequestClose={() => setDeleteCompanyPopover(false)}
					style={{
						overlay: {
							backgroundColor: 'rgba(0, 0, 0, 0.75)',
						},
					}}
				>
					<DeleteCompany
						deleteCompanyChangeHandler={deleteCompanyChangeHandler}
						deleteButtonClicked={deleteButtonClicked}
						setConfirmDelete={setConfirmDelete}
						setDeleteCompanyPopover={setDeleteCompanyPopover}
					/>
				</ReactModal>

				<div
					className={classNames(
						isAddingCompany || isDeletingComapny || isUpdatingCompany ? '' : 'hidden',
						'z-50 mx-auto flex h-fit w-fit items-center rounded bg-indigo-600 p-2 font-medium'
					)}
				>
					<FaCircleNotch className="mr-2 animate-spin text-white" />
					Processing...
				</div>
			</section>
		);
	}
};

export default NewCompanyEntryForm;
