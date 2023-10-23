import React from 'react';
import { useSelector } from 'react-redux';
import {
	useGetCompanyDetailsQuery,
	useUpdateCompanyDetailsMutation,
	usePostCompanyDetailsMutation,
} from '../../../../authentication/api/companyEntryApiSlice';
import { useState, useEffect } from 'react';
import { useOutletContext } from 'react-router-dom';
// Convert Tin Number to GST in backend

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};
const CompanyEntryForm = () => {
	const globalCompany = useSelector((state) => state.globalCompany);
	const {
		data: fetchedData,
		isLoading,
		isSuccess: detailsExist,
		isError,
		error: getError,
	} = useGetCompanyDetailsQuery(globalCompany.id);
	const [updateCompanyDetails] = useUpdateCompanyDetailsMutation();
	const [postCompanyDetails, { error: postError }] = usePostCompanyDetailsMutation();
	const defaultCompanyDetails = {
		company: globalCompany.id,
		address: '',
		key_person: '',
		involving_industry: '',
		phone_no: '',
		email: '',
		pf_no: '',
		esi_no: '',
		head_office_address: '',
		pan_no: '',
		gst_no: '',
	};
	const [companyDetails, setCompanyDetails] = useState(defaultCompanyDetails);
	const [disableEdit, setDisableEdit] = useState(true);
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();

	console.log(companyDetails);

	const changeHandler = (event) => {
		setCompanyDetails((prevState) => {
			return { ...prevState, [event.target.name]: event.target.value };
		});
	};
	// console.log(companyDetails)

	const saveButtonClicked = async (event) => {
		event.preventDefault();
		if (detailsExist) {
			const details = { ...companyDetails };
			updateCompanyDetails({ details: details, id: globalCompany.id });
		} else {
			let toSend = { ...companyDetails };
			if ((toSend.esi_no = '')) {
				toSend.esi_no = null;
			}
			if ((toSend.phone_no = '')) {
				toSend.phone_no = null;
			}

			const details = { ...companyDetails };
			console.log(details);
			try {
				const response = await postCompanyDetails(details);
			} catch (err) {
				console.log(err);
			}
		}
		setDisableEdit(true);
	};

	const editButtonClicked = () => {
		setDisableEdit(!disableEdit);
	};

	if (globalCompany.id == null) {
		return (
			<section className="flex flex-col items-center">
				<h4 className="text-x mt-10 font-bold text-redAccent-500 dark:text-redAccent-600">
					Please Select a Company First
				</h4>
			</section>
		);
	}

	useEffect(() => {
		setShowLoadingBar(isLoading);
		if (detailsExist) {
			setCompanyDetails(fetchedData);
		}
	}, [isLoading]);

	if (isLoading) {
		return <div></div>;
	} else {
		return (
			<section className="mx-6 mt-2">
				<div className="flex flex-row flex-wrap place-content-between gap-4">
					<div>
						<h1 className="text-3xl font-medium">Company Details</h1>
						<p className="my-2 text-sm">Add/Edit details of selected company here</p>
						<p
							className={classNames(
								disableEdit
									? 'text-redAccent-600 dark:text-redAccent-500'
									: 'text-teal-700 dark:text-teal-600',
								'my-2 text-sm font-semibold'
							)}
						>
							{disableEdit ? 'Click edit button to edit information' : 'Edit enabled'}
						</p>
					</div>
					<div className="">
						<button
							type="submit"
							form="company-entry-form"
							className="mr-4 w-20 rounded bg-teal-500 p-2 text-base font-medium hover:bg-teal-600 dark:bg-teal-700 dark:hover:bg-teal-600"
							onClick={saveButtonClicked}
						>
							Save
						</button>
						<button
							className="w-20 rounded bg-zinc-400 p-2 text-base font-medium hover:bg-zinc-500 dark:bg-zinc-700 dark:hover:bg-zinc-600"
							onClick={editButtonClicked}
						>
							Edit
						</button>
					</div>
				</div>
				<form id="company-entry-form" className="mt-2">
					<div className="flex w-full flex-col gap-2">
						<div>
							<label
								htmlFor="company"
								className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
							>
								Name
							</label>
							<input
								type="text"
								name="company"
								id="company"
								className="w-full rounded bg-slate-200 p-2 text-slate-500 dark:bg-zinc-800 dark:text-slate-400 lg:w-fit"
								value={globalCompany.name}
								disabled
								size={globalCompany.name.length}
							/>
						</div>
						<div>
							<label
								htmlFor="address"
								className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
							>
								Address
							</label>
							<input
								disabled={disableEdit}
								type="text"
								name="address"
								onChange={changeHandler}
								id="address"
								className={classNames(
									disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
									'w-full rounded bg-slate-200 p-2 dark:bg-zinc-800 lg:w-3/4'
								)}
								value={companyDetails.address}
							/>
						</div>
						<div>
							<label
								htmlFor="key_person"
								className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
							>
								Key Person
							</label>
							<input
								disabled={disableEdit}
								type="text"
								name="key_person"
								onChange={changeHandler}
								id="key_person"
								className={classNames(
									disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
									'w-1/3 min-w-fit rounded bg-slate-200 p-2 dark:bg-zinc-800'
								)}
								value={companyDetails.key_person}
							/>
						</div>
						<div>
							<label
								htmlFor="involving_industry"
								className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
							>
								Involving Industry
							</label>
							<input
								disabled={disableEdit}
								type="text"
								name="involving_industry"
								onChange={changeHandler}
								id="involving_industry"
								className={classNames(
									disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
									'w-1/3 min-w-fit rounded bg-slate-200 p-2 dark:bg-zinc-800'
								)}
								value={companyDetails.involving_industry}
							/>
						</div>

						<div>
							<label
								htmlFor="phone_no"
								className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
							>
								Phone Number
							</label>
							<input
								disabled={disableEdit}
								type="tel"
								maxLength="10"
								minLength="10"
								name="phone_no"
								onChange={changeHandler}
								id="phone_no"
								className={classNames(
									disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
									'rounded bg-slate-200 p-2 dark:bg-zinc-800'
								)}
								size="10"
								value={companyDetails.phone_no}
							/>
						</div>

						<div>
							<label
								htmlFor="email"
								className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
							>
								Email
							</label>
							<input
								disabled={disableEdit}
								type="email"
								name="email"
								onChange={changeHandler}
								id="email"
								className={classNames(
									disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
									'w-1/4 min-w-fit rounded bg-slate-200 p-2 dark:bg-zinc-800'
								)}
								size="30"
								value={companyDetails.email}
							/>
						</div>
						<div>
							<label
								htmlFor="pf_no"
								className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
							>
								P.F Number
							</label>
							<input
								disabled={disableEdit}
								type="text"
								name="pf_no"
								onChange={changeHandler}
								id="pf_no"
								className={classNames(
									disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
									'rounded bg-slate-200 p-2 dark:bg-zinc-800'
								)}
								minLength="22"
								maxLength="22"
								size="22"
								value={companyDetails.pf_no}
							/>
						</div>
						<div>
							<label
								htmlFor="esi_no"
								className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
							>
								E.S.I Number
							</label>
							<input
								disabled={disableEdit}
								type="number"
								name="esi_no"
								onChange={changeHandler}
								id="esi_no"
								className={classNames(
									disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
									'rounded bg-slate-200 p-2 dark:bg-zinc-800'
								)}
								maxLength="17"
								minLength="17"
								size="17"
								value={companyDetails.esi_no}
							/>
						</div>

						<div>
							<label
								htmlFor="head_office_address"
								className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
							>
								Head Office Address
							</label>
							<input
								disabled={disableEdit}
								type="text"
								name="head_office_address"
								onChange={changeHandler}
								id="head_office_address"
								className={classNames(
									disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
									'w-full rounded bg-slate-200 p-2 dark:bg-zinc-800 lg:w-3/4'
								)}
								value={companyDetails.head_office_address}
							/>
						</div>

						<div>
							<label
								htmlFor="pan_no"
								className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
							>
								Pan Number
							</label>
							<input
								disabled={disableEdit}
								type="text"
								maxLength="10"
								minLength="10"
								name="pan_no"
								onChange={changeHandler}
								id="pan_no"
								className={classNames(
									disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
									'rounded bg-slate-200 p-2 dark:bg-zinc-800'
								)}
								size="10"
								value={companyDetails.pan_no}
							/>
						</div>

						<div>
							<label
								htmlFor="gst_no"
								className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
							>
								GST Number
							</label>
							<input
								disabled={disableEdit}
								type="text"
								maxLength="15"
								minLength="15"
								name="gst_no"
								onChange={changeHandler}
								id="gst_no"
								className={classNames(
									disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
									'rounded bg-slate-200 p-2 dark:bg-zinc-800'
								)}
								size="15"
								value={companyDetails.gst_no}
							/>
						</div>
					</div>
				</form>
			</section>
		);
	}
};
export default CompanyEntryForm;
