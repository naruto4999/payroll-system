import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
	useGetCompanyDetailsQuery,
	useUpdateCompanyDetailsMutation,
	useAddCompanyDetailsMutation,
} from '../../../../authentication/api/companyEntryApiSlice';
import { useState, useEffect } from 'react';
import { useOutletContext } from 'react-router-dom';
import { Field, ErrorMessage } from 'formik';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import { Formik } from 'formik';

// Convert Tin Number to GST in backend

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};
const CompanyEntryForm = () => {
	const dispatch = useDispatch();
	const globalCompany = useSelector((state) => state.globalCompany);
	const {
		data: companyDetails,
		isLoading,
		isSuccess,
		isError,
		error: getError,
	} = useGetCompanyDetailsQuery(globalCompany.id);
	const [updateCompanyDetails] = useUpdateCompanyDetailsMutation();
	const [addCompanyDetails, { error: postError }] = useAddCompanyDetailsMutation();
	const [disableEdit, setDisableEdit] = useState(true);
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();

	console.log(companyDetails);

	const changeHandler = (event) => {
		setCompanyDetails((prevState) => {
			return { ...prevState, [event.target.name]: event.target.value };
		});
	};
	// console.log(companyDetails)

	const updateButtonClicked = async (values, formikBag) => {
		console.log(values);
		let toSend = { ...values };
		for (const key in toSend) {
			if (toSend.hasOwnProperty(key) && toSend[key] === '') {
				toSend[key] = null;
			}
		}
		if (isSuccess) {
			try {
				const data = await updateCompanyDetails({
					...toSend,
					company: globalCompany.id,
				}).unwrap();
				console.log(data);
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
		} else if (!isSuccess) {
			try {
				const data = await addCompanyDetails({
					...toSend,
					company: globalCompany.id,
				}).unwrap();
				console.log(data);
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
		}
		setDisableEdit(true);
		// event.preventDefault();
		// if (isSuccess) {
		// 	const details = { ...companyDetails };
		// 	updateCompanyDetails({ details: details, id: globalCompany.id });
		// } else {
		// 	let toSend = { ...companyDetails };
		// 	if ((toSend.esiNo = '')) {
		// 		toSend.esiNo = null;
		// 	}
		// 	if ((toSend.phoneNo = '')) {
		// 		toSend.phoneNo = null;
		// 	}
		// 	const details = { ...companyDetails };
		// 	console.log(details);
		// 	try {
		// 		const response = await addCompanyDetails(details);
		// 	} catch (err) {
		// 		console.log(err);
		// 	}
		// }
		// setDisableEdit(true);
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

	if (isLoading) {
		return <div></div>;
	} else {
		return (
			<section className="mx-6 mt-2">
				<Formik
					initialValues={
						isSuccess
							? {
									...companyDetails,
									address: companyDetails.address ?? '',
									keyPerson: companyDetails.keyPerson ?? '',
									involvingIndustry: companyDetails.involvingIndustry ?? '',
									phoneNo: companyDetails.phoneNo ?? '',
									email: companyDetails.email ?? '',
									pfNo: companyDetails.pfNo ?? '',
									esiNo: companyDetails.esiNo ?? '',
									headOfficeAddress: companyDetails.headOfficeAddress ?? '',
									panNo: companyDetails.panNo ?? '',
									gstNo: companyDetails.gstNo ?? '',
							  }
							: {
									address: '',
									keyPerson: '',
									involvingIndustry: '',
									phoneNo: '',
									email: '',
									pfNo: '',
									esiNo: '',
									headOfficeAddress: '',
									panNo: '',
									gstNo: '',
							  }
					}
					validationSchema={''}
					onSubmit={updateButtonClicked}
				>
					{({ handleSubmit, errors, touched, values }) => (
						<div>
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
										onClick={handleSubmit}
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
										<Field
											disabled={disableEdit}
											type="text"
											name="address"
											className={classNames(
												disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
												'w-full rounded bg-slate-200 p-2 dark:bg-zinc-800 lg:w-3/4'
											)}
										/>
									</div>
									<div>
										<label
											htmlFor="keyPerson"
											className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
										>
											Key Person
										</label>
										<Field
											disabled={disableEdit}
											type="text"
											name="keyPerson"
											className={classNames(
												disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
												'w-1/3 min-w-fit rounded bg-slate-200 p-2 dark:bg-zinc-800'
											)}
										/>
									</div>
									<div>
										<label
											htmlFor="involvingIndustry"
											className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
										>
											Involving Industry
										</label>
										<Field
											disabled={disableEdit}
											type="text"
											name="involvingIndustry"
											className={classNames(
												disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
												'w-1/3 min-w-fit rounded bg-slate-200 p-2 dark:bg-zinc-800'
											)}
										/>
									</div>
									{/* {console.log(values)} */}

									<div>
										<label
											htmlFor="phoneNo"
											className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
										>
											Phone Number
										</label>
										<Field
											disabled={disableEdit}
											type="tel"
											maxLength="10"
											minLength="10"
											name="phoneNo"
											className={classNames(
												disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
												'rounded bg-slate-200 p-2 dark:bg-zinc-800'
											)}
											size="10"
										/>
									</div>

									<div>
										<label
											htmlFor="email"
											className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
										>
											Email
										</label>
										<Field
											disabled={disableEdit}
											type="email"
											name="email"
											className={classNames(
												disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
												'w-1/4 min-w-fit rounded bg-slate-200 p-2 dark:bg-zinc-800'
											)}
											size="30"
										/>
									</div>
									<div>
										<label
											htmlFor="pfNo"
											className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
										>
											P.F Number
										</label>
										<Field
											disabled={disableEdit}
											type="text"
											name="pfNo"
											className={classNames(
												disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
												'rounded bg-slate-200 p-2 dark:bg-zinc-800'
											)}
											minLength="22"
											maxLength="22"
											size="22"
										/>
									</div>
									<div>
										<label
											htmlFor="esiNo"
											className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
										>
											E.S.I Number
										</label>
										<Field
											disabled={disableEdit}
											type="number"
											name="esiNo"
											className={classNames(
												disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
												'custom-number-input rounded bg-slate-200 p-2 dark:bg-zinc-800'
											)}
											maxLength="17"
											minLength="17"
											size="17"
										/>
									</div>

									<div>
										<label
											htmlFor="headOfficeAddress"
											className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
										>
											Head Office Address
										</label>
										<Field
											disabled={disableEdit}
											type="text"
											name="headOfficeAddress"
											className={classNames(
												disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
												'w-full rounded bg-slate-200 p-2 dark:bg-zinc-800 lg:w-3/4'
											)}
										/>
									</div>

									<div>
										<label
											htmlFor="panNo"
											className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
										>
											Pan Number
										</label>
										<Field
											disabled={disableEdit}
											type="text"
											maxLength="10"
											minLength="10"
											name="panNo"
											className={classNames(
												disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
												'rounded bg-slate-200 p-2 dark:bg-zinc-800'
											)}
											size="10"
										/>
									</div>

									<div>
										<label
											htmlFor="gstNo"
											className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
										>
											GST Number
										</label>
										<Field
											disabled={disableEdit}
											type="text"
											maxLength="15"
											minLength="15"
											name="gstNo"
											className={classNames(
												disableEdit ? 'text-teal-600 dark:text-teal-700' : '',
												'rounded bg-slate-200 p-2 dark:bg-zinc-800'
											)}
											size="15"
										/>
									</div>
								</div>
							</form>
						</div>
					)}
				</Formik>
			</section>
		);
	}
};
export default CompanyEntryForm;
