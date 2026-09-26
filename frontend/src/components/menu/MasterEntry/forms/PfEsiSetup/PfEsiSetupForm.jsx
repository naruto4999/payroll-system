import React, { useState, useEffect } from 'react';
// import authSlice from "./store/slices/auth";
import { useDispatch, useSelector } from 'react-redux';
import {
	useGetPfEsiSetupQuery,
	useAddPfEsiSetupMutation,
	useUpdatePfEsiSetupMutation,
} from '../../../../authentication/api/pfEsiSetupApiSlice';
import { Formik } from 'formik';
import { useOutletContext } from 'react-router-dom';
import { FaCircleNotch } from 'react-icons/fa';
import { Field, ErrorMessage } from 'formik';
import { PfEsiSetupValidationSchema } from './PfEsiSetupValidationSchema';
// import { PfEsiVa}
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import { useGetEarningsHeadsQuery } from '../../../../authentication/api/earningsHeadEntryApiSlice';
import Button from '../../../../UI/Button';
import Checkbox from '../../../../UI/Checkbox';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const PfEsiSetupForm = () => {
	const dispatch = useDispatch();

	const globalCompany = useSelector((state) => state.globalCompany);
	const companyId = globalCompany?.id;
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();

	const {
		data: { company, ...pfEsiSetup } = {},
		isLoading,
		isSuccess,
		isError,
		error,
		isFetching,
	} = useGetPfEsiSetupQuery(companyId, { skip: !companyId });
	const {
		currentData: earningsHeads = [],
		isLoading: isLoadingEarningsHeads,
		isFetching: isFetchingEarningsHeads,
		isError: isEarningsHeadsError,
	} = useGetEarningsHeadsQuery(globalCompany, { skip: !companyId });

	const [
		addPfEsiSetup,
		{
			isLoading: isAddingPfEsiSetup,
			// isError: errorRegisteringRegular,
			isSuccess: isAddPfEsiSetupSuccess,
		},
	] = useAddPfEsiSetupMutation();
	const [
		updatePfEsiSetup,
		{
			isLoading: isUpdatingPfEsiSetup,
			// isError: errorRegisteringRegular,
			isSuccess: isUpdatingPfEsiSetupSuccess,
		},
	] = useUpdatePfEsiSetupMutation();
	const [errorMessage, setErrorMessage] = useState('');

	const updateButtonClicked = async (values, formikBag) => {
		if (!companyId) return;
		const toSend = {
			...values,
			esiEarningsHeads: (values.esiEarningsHeads || []).map(Number),
			company: companyId,
		};
		if (isSuccess) {
			try {
				await updatePfEsiSetup(toSend).unwrap();
				dispatch(
					alertActions.createAlert({
						message: 'Saved',
						type: 'Success',
						duration: 3000,
					})
				);
			} catch (err) {
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
				await addPfEsiSetup(toSend).unwrap();
				dispatch(
					alertActions.createAlert({
						message: 'Saved',
						type: 'Success',
						duration: 3000,
					})
				);
			} catch (err) {
				dispatch(
					alertActions.createAlert({
						message: 'Error Occurred',
						type: 'Error',
						duration: 5000,
					})
				);
			}
		}
	};

	useEffect(() => {
		setShowLoadingBar(
			isLoading ||
				isFetching ||
				isLoadingEarningsHeads ||
				isFetchingEarningsHeads ||
				isAddingPfEsiSetup ||
				isUpdatingPfEsiSetup
		);
	}, [
		isLoading,
		isFetching,
		isLoadingEarningsHeads,
		isFetchingEarningsHeads,
		isAddingPfEsiSetup,
		isUpdatingPfEsiSetup,
		setShowLoadingBar,
	]);

	if (!companyId) {
		return (
			<section className="flex flex-col items-center">
				<h4 className="text-x mt-10 font-bold text-redAccent-500 dark:text-redAccent-600">
					Please Select a Company First
				</h4>
			</section>
		);
	}

	if (isLoading || isFetching || isLoadingEarningsHeads || isFetchingEarningsHeads) {
		return (
			<div className="fixed inset-0 z-50 mx-auto my-auto flex h-fit w-fit items-center rounded bg-indigo-600 p-2 font-medium">
				<FaCircleNotch className="mr-2 animate-spin text-white" />
				Processing...
			</div>
		);
	} else {
		return (
			<section className="mx-4 mt-4 sm:mx-6">
				<div className="flex flex-row flex-wrap place-content-between">
					<div className="mr-4">
						<h1 className="text-3xl font-medium">PF and ESI Setup</h1>
						<p className="my-2 text-sm text-zinc-600 dark:text-zinc-400">Edit the values for PF and ESI calculations here</p>
						{/* <p className="text-sm my-2">
                            {isSuccess
                                ? "Sub user already exists, below are the details."
                                : "Create Sub User Here"}
                        </p> */}
					</div>
				</div>

				{/* Formik Implementation */}
				<Formik
					enableReinitialize
					validateOnMount
					initialValues={
						isSuccess
							? {
									...pfEsiSetup,
									employerPfCode: pfEsiSetup.employerPfCode ?? '',
									employerEsiCode: pfEsiSetup.employerEsiCode ?? '',
									labourWellfareFundEmployerCode: pfEsiSetup.labourWellfareFundEmployerCode ?? '',
									esiEarningsHeads: (pfEsiSetup.esiEarningsHeads || []).map((head) =>
										String(typeof head === 'object' ? head.id : head)
									),
							  }
							: {
									ac1EpfEmployeePercentage: '',
									ac1EpfEmployeeLimit: '',
									ac1EpfEmployerPercentage: '',
									ac1EpfEmployerLimit: '',
									ac10EpsEmployerPercentage: '',
									ac10EpsEmployerLimit: '',
									ac2EmployerPercentage: '',
									ac21EmployerPercentage: '',
									ac22EmployerPercentage: '',
									employerPfCode: '',
									esiEmployeePercentage: '',
									esiEmployeeLimit: '',
									esiEmployerPercentage: '',
									esiEmployerLimit: '',
									employerEsiCode: '',
									esiEarningsHeads: [],
							  }
					}
					validationSchema={PfEsiSetupValidationSchema}
					onSubmit={updateButtonClicked}
				>
					{({ handleSubmit, errors, touched, values, isValid }) => (
						<form
							id=""
							className="mt-2 [&_input:not([type=checkbox])]:!w-40"
							onSubmit={handleSubmit}
						>
							<section className="grid grid-cols-1 items-start gap-5 xl:grid-cols-2">
								<div className="flex min-w-0 flex-col gap-3">
									<div className="flex w-fit max-w-full flex-row flex-wrap gap-3 rounded-lg border border-zinc-300 bg-white/40 px-3 pb-3 pt-5 shadow-sm transition-colors focus-within:border-teal-500 dark:border-zinc-700 dark:bg-zinc-900/30 dark:focus-within:border-teal-600">
										<div className="my-auto block w-52 font-medium text-amber-600 dark:text-amber-600">
											{'Employer PF Code'}
										</div>
										<div className="relative ">
											<Field
												className={classNames(
													errors.employerPfCode && touched.employerPfCode
														? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
														: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
													'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
												)}
												type="text"
												name={`employerPfCode`}
												placeholder=" "
												id="employerPfCode"
											/>
											<label
												htmlFor="employerPfCode"
												className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
											>
												Code
											</label>
											<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
												<ErrorMessage name={`employerPfCode`} />
											</div>
										</div>
									</div>
										<div>
										<div className="flex w-fit max-w-full flex-row flex-wrap gap-3 rounded-lg border border-zinc-300 bg-white/40 px-3 pb-3 pt-5 shadow-sm transition-colors focus-within:border-teal-500 dark:border-zinc-700 dark:bg-zinc-900/30 dark:focus-within:border-teal-600">
											<div className="my-auto block w-52 font-medium text-blueAccent-700 dark:text-blueAccent-400">
												{'A/C No. 1 (EPF - Employee)'}
											</div>
											<div className="relative ">
												<Field
													className={classNames(
														errors.ac1EpfEmployeePercentage &&
															touched.ac1EpfEmployeePercentage
															? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
															: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
														'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
													)}
													type="number"
													name={`ac1EpfEmployeePercentage`}
													placeholder=" "
													id="ac1EpfEmployeePercentage"
													step="0.01"
												/>
												<label
													htmlFor="ac1EpfEmployeePercentage"
													className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
												>
													Percentage
												</label>
												<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
													<ErrorMessage name={`ac1EpfEmployeePercentage`} />
												</div>
											</div>

											<div>
												<div className="relative ">
													<Field
														className={classNames(
															errors.ac1EpfEmployeeLimit && touched.ac1EpfEmployeeLimit
																? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
															'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
														)}
														type="number"
														name={`ac1EpfEmployeeLimit`}
														placeholder=" "
														id="ac1EpfEmployeeLimit"
													/>
													<label
														htmlFor="ac1EpfEmployeeLimit"
														className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
													>
														Limit
													</label>
												</div>
												<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
													<ErrorMessage name={`ac1EpfEmployeeLimit`} />
												</div>
											</div>
										</div>
									</div>

									<div>
									<div className="flex w-fit max-w-full flex-row flex-wrap gap-3 rounded-lg border border-zinc-300 bg-white/40 px-3 pb-3 pt-5 shadow-sm transition-colors focus-within:border-teal-500 dark:border-zinc-700 dark:bg-zinc-900/30 dark:focus-within:border-teal-600">
											<div className="my-auto block w-52 font-medium text-blueAccent-700 dark:text-blueAccent-400">
												{'A/C No. 1 (EPF - Employer)'}
											</div>
											<div className="relative ">
												<Field
													className={classNames(
														errors.ac1EpfEmployerPercentage &&
															touched.ac1EpfEmployerPercentage
															? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
															: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
														'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
													)}
													type="number"
													name={`ac1EpfEmployerPercentage`}
													placeholder=" "
													id="ac1EpfEmployerPercentage"
													step="0.01"
												/>
												<label
													htmlFor="ac1EpfEmployerPercentage"
													className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
												>
													Percentage
												</label>
												<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
													<ErrorMessage name={`ac1EpfEmployerPercentage`} />
												</div>
											</div>

											<div>
												<div className="relative ">
													<Field
														className={classNames(
															errors.ac1EpfEmployerLimit && touched.ac1EpfEmployerLimit
																? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
															'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
														)}
														type="number"
														name={`ac1EpfEmployerLimit`}
														placeholder=" "
														id="ac1EpfEmployerLimit"
													/>
													<label
														htmlFor="ac1EpfEmployerLimit"
														className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
													>
														Limit
													</label>
												</div>
												<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
													<ErrorMessage name={`ac1EpfEmployerLimit`} />
												</div>
											</div>
										</div>
									</div>

									<div>
										<div className="flex w-fit max-w-full flex-row flex-wrap gap-3 rounded-lg border border-zinc-300 bg-white/40 px-3 pb-3 pt-5 shadow-sm transition-colors focus-within:border-teal-500 dark:border-zinc-700 dark:bg-zinc-900/30 dark:focus-within:border-teal-600">
											<div className="my-auto block w-52 font-medium text-blueAccent-700 dark:text-blueAccent-400">
												{'A/C No. 10 (EPS - Employer)'}
											</div>
											<div className="relative ">
												<Field
													className={classNames(
														errors.ac10EpsEmployerPercentage &&
															touched.ac10EpsEmployerPercentage
															? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
															: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
														'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
													)}
													type="number"
													name={`ac10EpsEmployerPercentage`}
													placeholder=" "
													id="ac10EpsEmployerPercentage"
													step="0.01"
												/>
												<label
													htmlFor="ac10EpsEmployerPercentage"
													className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
												>
													Percentage
												</label>
												<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
													<ErrorMessage name={`ac10EpsEmployerPercentage`} />
												</div>
											</div>

											<div>
												<div className="relative ">
													<Field
														className={classNames(
															errors.ac10EpsEmployerLimit && touched.ac10EpsEmployerLimit
																? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
															'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
														)}
														type="number"
														name={`ac10EpsEmployerLimit`}
														placeholder=" "
														id="ac10EpsEmployerLimit"
													/>
													<label
														htmlFor="ac10EpsEmployerLimit"
														className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
													>
														Limit
													</label>
												</div>
												<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
													<ErrorMessage name={`ac10EpsEmployerLimit`} />
												</div>
											</div>
										</div>
									</div>

									<div>
										<div className="flex w-fit max-w-full flex-row flex-wrap gap-3 rounded-lg border border-zinc-300 bg-white/40 px-3 pb-3 pt-5 shadow-sm transition-colors focus-within:border-teal-500 dark:border-zinc-700 dark:bg-zinc-900/30 dark:focus-within:border-teal-600">
											<div className="my-auto block w-52 font-medium text-blueAccent-700 dark:text-blueAccent-400">
												{'A/C No. 2 (Employer)'}
											</div>
											<div className="relative ">
												<Field
													className={classNames(
														errors.ac2EmployerPercentage && touched.ac2EmployerPercentage
															? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
															: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
														'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
													)}
													type="number"
													name={`ac2EmployerPercentage`}
													placeholder=" "
													id="ac2EmployerPercentage"
													step="0.01"
												/>
												<label
													htmlFor="ac2EmployerPercentage"
													className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
												>
													Percentage
												</label>
												<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
													<ErrorMessage name={`ac2EmployerPercentage`} />
												</div>
											</div>
										</div>
									</div>

									<div>
										<div className="flex w-fit max-w-full flex-row flex-wrap gap-3 rounded-lg border border-zinc-300 bg-white/40 px-3 pb-3 pt-5 shadow-sm transition-colors focus-within:border-teal-500 dark:border-zinc-700 dark:bg-zinc-900/30 dark:focus-within:border-teal-600">
											<div className="my-auto block w-52 font-medium text-blueAccent-700 dark:text-blueAccent-400">
												{'A/C No. 21 (Employer)'}
											</div>
											<div className="relative ">
												<Field
													className={classNames(
														errors.ac21EmployerPercentage && touched.ac21EmployerPercentage
															? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
															: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
														'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
													)}
													type="number"
													name={`ac21EmployerPercentage`}
													placeholder=" "
													id="ac21EmployerPercentage"
													step="0.01"
												/>
												<label
													htmlFor="ac21EmployerPercentage"
													className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
												>
													Percentage
												</label>
												<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
													<ErrorMessage name={`ac21EmployerPercentage`} />
												</div>
											</div>
										</div>
									</div>

									<div>
										<div className="flex w-fit max-w-full flex-row flex-wrap gap-3 rounded-lg border border-zinc-300 bg-white/40 px-3 pb-3 pt-5 shadow-sm transition-colors focus-within:border-teal-500 dark:border-zinc-700 dark:bg-zinc-900/30 dark:focus-within:border-teal-600">
											<div className="my-auto block w-52 font-medium text-blueAccent-700 dark:text-blueAccent-400">
												{'A/C No. 22 (Employer)'}
											</div>
											<div className="relative ">
												<Field
													className={classNames(
														errors.ac22EmployerPercentage && touched.ac22EmployerPercentage
															? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
															: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
														'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
													)}
													type="number"
													name={`ac22EmployerPercentage`}
													placeholder=" "
													id="ac22EmployerPercentage"
													step="0.01"
												/>
												<label
													htmlFor="ac22EmployerPercentage"
													className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
												>
													Percentage
												</label>
												<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
													<ErrorMessage name={`ac22EmployerPercentage`} />
												</div>
											</div>
										</div>
									</div>
								</div>

								<div className="flex min-w-0 flex-col gap-3">

									<div className="flex w-fit max-w-full flex-row flex-wrap gap-3 rounded-lg border border-zinc-300 bg-white/40 px-3 pb-3 pt-5 shadow-sm transition-colors focus-within:border-teal-500 dark:border-zinc-700 dark:bg-zinc-900/30 dark:focus-within:border-teal-600">
										<div className="my-auto block w-52 font-medium text-amber-600 dark:text-amber-600">
											{'Employer ESI Code'}
										</div>
										<div className="relative ">
											<Field
												className={classNames(
													errors.employerEsiCode && touched.employerEsiCode
														? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
														: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
													'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
												)}
												type="text"
												name={`employerEsiCode`}
												placeholder=" "
												id="employerEsiCode"
											/>
											<label
												htmlFor="employerEsiCode"
												className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
											>
												Code
											</label>
											<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
												<ErrorMessage name={`employerEsiCode`} />
											</div>
										</div>
									</div>

									<div>
										<div className="flex w-fit max-w-full flex-row flex-wrap gap-3 rounded-lg border border-zinc-300 bg-white/40 px-3 pb-3 pt-5 shadow-sm transition-colors focus-within:border-teal-500 dark:border-zinc-700 dark:bg-zinc-900/30 dark:focus-within:border-teal-600">
											<div className="my-auto block w-52 font-medium text-blueAccent-700 dark:text-blueAccent-400">
												{'ESI Employee'}
											</div>
											<div className="relative ">
												<Field
													className={classNames(
														errors.esiEmployeePercentage && touched.esiEmployeePercentage
															? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
															: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
														'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
													)}
													type="number"
													name={`esiEmployeePercentage`}
													placeholder=" "
													id="esiEmployeePercentage"
													step="0.01"
												/>
												<label
													htmlFor="esiEmployeePercentage"
													className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
												>
													Percentage
												</label>
												<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
													<ErrorMessage name={`esiEmployeePercentage`} />
												</div>
											</div>

											<div>
												<div className="relative ">
													<Field
														className={classNames(
															errors.esiEmployeeLimit && touched.esiEmployeeLimit
																? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
															'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
														)}
														type="number"
														name={`esiEmployeeLimit`}
														placeholder=" "
														id="esiEmployeeLimit"
													/>
													<label
														htmlFor="esiEmployeeLimit"
														className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
													>
														Limit
													</label>
												</div>
												<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
													<ErrorMessage name={`esiEmployeeLimit`} />
												</div>
											</div>
										</div>
									</div>

									<div>
										<div className="flex w-fit max-w-full flex-row flex-wrap gap-3 rounded-lg border border-zinc-300 bg-white/40 px-3 pb-3 pt-5 shadow-sm transition-colors focus-within:border-teal-500 dark:border-zinc-700 dark:bg-zinc-900/30 dark:focus-within:border-teal-600">
											<div className="my-auto block w-52 font-medium text-blueAccent-700 dark:text-blueAccent-400">
												{'ESI Employer'}
											</div>
											<div className="relative ">
												<Field
													className={classNames(
														errors.esiEmployerPercentage && touched.esiEmployerPercentage
															? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
															: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
														'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
													)}
													type="number"
													name={`esiEmployerPercentage`}
													placeholder=" "
													id="esiEmployerPercentage"
													step="0.01"
												/>
												<label
													htmlFor="esiEmployerPercentage"
													className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
												>
													Percentage
												</label>
												<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
													<ErrorMessage name={`esiEmployerPercentage`} />
												</div>
											</div>

											<div>
												<div className="relative ">
													<Field
														className={classNames(
															errors.esiEmployerLimit && touched.esiEmployerLimit
																? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
															'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
														)}
														type="number"
														name={`esiEmployerLimit`}
														placeholder=" "
														id="esiEmployerLimit"
													/>
													<label
														htmlFor="esiEmployerLimit"
														className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
													>
														Limit
													</label>
												</div>
												<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
													<ErrorMessage name={`esiEmployerLimit`} />
												</div>
											</div>
										</div>
									</div>

										<fieldset className="w-full rounded-lg border border-zinc-300 bg-white/30 px-3 py-3 shadow-sm transition-colors focus-within:border-teal-500 dark:border-zinc-700 dark:bg-zinc-900/20 dark:focus-within:border-teal-600">
										<legend className="px-1 font-medium text-blueAccent-700 dark:text-blueAccent-400">
											ESI Earnings Heads
										</legend>
										<p className="text-xs text-zinc-600 dark:text-zinc-400">
											Select the earnings heads included when calculating ESI for this company.
										</p>
											<div className="mt-2 grid gap-2 rounded-lg border border-zinc-300 bg-zinc-100/70 p-3 dark:border-zinc-600 dark:bg-zinc-700/80 sm:grid-cols-2">
											{isEarningsHeadsError ? (
												<p className="text-sm text-red-700 dark:text-red-400 sm:col-span-2">
													Unable to load earnings heads for this company.
												</p>
											) : earningsHeads.length === 0 ? (
												<p className="text-sm text-amber-700 dark:text-amber-400 sm:col-span-2">
													No earnings heads are available for this company.
												</p>
											) : (
												earningsHeads.map((head) => (
														<Field
															as={Checkbox}
															key={head.id}
															type="checkbox"
															name="esiEarningsHeads"
															value={String(head.id)}
															variant="primary"
															className="min-h-10 rounded-md px-2 py-1 text-sm transition-colors hover:bg-white/70 dark:hover:bg-zinc-800/70"
														>
															{head.name}
														</Field>
													))
											)}
										</div>
										<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
											<ErrorMessage name="esiEarningsHeads" />
										</div>
									</fieldset>

								<div className="flex min-w-0 flex-col gap-3 rounded-xl border border-zinc-300 bg-white/40 p-4 shadow-sm dark:border-zinc-700 dark:bg-zinc-900/30 sm:p-5">
									<div className="flex items-start justify-between gap-4">
										<div>
											<h2 className="font-semibold text-amber-600 dark:text-amber-500">Labour Welfare Fund</h2>
											<p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">Configure the employer contribution and applicable limit.</p>
										</div>
										<Field
											as={Checkbox}
											type="checkbox"
												name="enableLabourWelfareFund"
												aria-label="Enable Labour Welfare Fund"
												variant="primary"
												className="shrink-0 rounded-full border border-zinc-300 px-3 py-2 text-sm font-medium dark:border-zinc-600"
										>
											Enable
										</Field>
									</div>

									{values.enableLabourWelfareFund && (
										<div className="flex w-full flex-row flex-wrap gap-3 rounded-lg border border-zinc-300 px-3 pb-3 pt-5 shadow-sm transition-colors focus-within:border-teal-500 dark:border-zinc-700 dark:focus-within:border-teal-600">
											<div className="my-auto block w-52 font-medium text-amber-600 dark:text-amber-600">
												{'Labour Wellfare Code'}
											</div>
											<div className="relative ">
												<Field
													className={classNames(
														errors.labourWellfareFundEmployerCode &&
															touched.labourWellfareFundEmployerCode
															? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
															: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
														'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
													)}
													type="text"
													name={`labourWellfareFundEmployerCode`}
													placeholder=" "
													id="labourWellfareFundEmployerCode"
												/>
												<label
													htmlFor="labourWellfareFundEmployerCode"
													className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
												>
													Code
												</label>
												<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
													<ErrorMessage name={`labourWellfareFundEmployerCode`} />
												</div>
											</div>
										</div>
									)}

									{values.enableLabourWelfareFund && (
										<div>
											<div className="flex w-full flex-row flex-wrap gap-3 rounded-lg border border-zinc-300 px-3 pb-3 pt-5 shadow-sm transition-colors focus-within:border-teal-500 dark:border-zinc-700 dark:focus-within:border-teal-600">
												<div className="my-auto block w-52 font-medium text-blueAccent-700 dark:text-blueAccent-400">
													{'Labour Wellfare Fund'}
												</div>
												<div className="relative ">
													<Field
														className={classNames(
															errors.labourWelfareFundPercentage &&
																touched.labourWelfareFundPercentage
																? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
															'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
														)}
														type="number"
														name={`labourWelfareFundPercentage`}
														placeholder=" "
														id="labourWelfareFundPercentage"
														step="0.01"
													/>
													<label
														htmlFor="labourWelfareFundPercentage"
														className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
													>
														Percentage
													</label>
													<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
														<ErrorMessage name={`labourWelfareFundPercentage`} />
													</div>
												</div>

												<div>
													<div className="relative ">
														<Field
															className={classNames(
																errors.labourWelfareFundLimit &&
																	touched.labourWelfareFundLimit
																	? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																	: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
																'custom-number-input peer w-full rounded border-2 bg-transparent p-1 outline-none transition focus:border-opacity-100 dark:focus:border-opacity-75'
															)}
															type="number"
															name={`labourWelfareFundLimit`}
															placeholder=" "
															id="labourWelfareFundLimit"
														/>
														<label
															htmlFor="labourWelfareFundLimit"
															className="absolute left-2 top-1 cursor-text text-gray-900 text-opacity-70 transition-all duration-200 peer-focus:-top-4 peer-focus:left-0 peer-focus:text-xs peer-focus:text-blueAccent-700 peer-[&:not(:placeholder-shown)]:left-0 peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70 dark:peer-focus:text-blueAccent-400 "
														>
															Limit
														</label>
													</div>
													<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
														<ErrorMessage name={`labourWelfareFundLimit`} />
													</div>
												</div>
											</div>
										</div>
									)}
								</div>
							</div>
							</section>

							<div className="mt-5 border-t border-zinc-200 pt-4 dark:border-zinc-800">
								<Button
									type="submit"
									size="sm"
									variant={isValid ? 'primary' : 'secondary'}
									disabled={!isValid || isAddingPfEsiSetup || isUpdatingPfEsiSetup}
									className="disabled:cursor-not-allowed disabled:bg-zinc-500 disabled:text-zinc-200 disabled:opacity-80 dark:disabled:bg-zinc-800 dark:disabled:text-zinc-500"
								>
									Update
								</Button>
							</div>
						</form>
					)}
				</Formik>
			</section>
		);
	}
};

export default PfEsiSetupForm;
