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

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const PfEsiSetupForm = () => {
	const dispatch = useDispatch();

	const globalCompany = useSelector((state) => state.globalCompany);
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();

	const {
		data: { company, ...pfEsiSetup } = {},
		isLoading,
		isSuccess,
		isError,
		error,
		isFetching,
	} = useGetPfEsiSetupQuery(globalCompany.id);

	console.log(pfEsiSetup);
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
		// console.log(values);
		if (isSuccess) {
			try {
				const data = await updatePfEsiSetup({
					...values,
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
				const data = await addPfEsiSetup({
					...values,
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
	};

	useEffect(() => {
		setShowLoadingBar(isLoading || isAddingPfEsiSetup || isUpdatingPfEsiSetup || isLoading);
	}, [isLoading, isAddingPfEsiSetup, isUpdatingPfEsiSetup]);

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
				<div className="flex flex-row flex-wrap place-content-between">
					<div className="mr-4">
						<h1 className="text-3xl font-medium">PF and ESI Setup</h1>
						<p className="my-2 text-sm">Edit the values for PF and ESI calculations here</p>
						{/* <p className="text-sm my-2">
                            {isSuccess
                                ? "Sub user already exists, below are the details."
                                : "Create Sub User Here"}
                        </p> */}
					</div>
				</div>

				{/* Formik Implementation */}
				<Formik
					initialValues={
						isSuccess
							? {
									...pfEsiSetup,
									employerPfCode: pfEsiSetup.employerPfCode ?? '',
									employerEsiCode: pfEsiSetup.employerEsiCode ?? '',
									labourWellfareFundEmployerCode: pfEsiSetup.labourWellfareFundEmployerCode ?? '',
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
							  }
					}
					validationSchema={PfEsiSetupValidationSchema}
					onSubmit={updateButtonClicked}
				>
					{({ handleSubmit, errors, touched, values }) => (
						<form id="" className="mt-2" onSubmit={handleSubmit}>
							<section className="flex flex-row flex-wrap gap-4">
								<div className="flex flex-col gap-2">
									<div className="flex w-fit flex-row flex-wrap gap-3 rounded border px-2 pt-5 pb-2 dark:border-slate-300 dark:border-opacity-20 dark:focus-within:border-opacity-60">
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
										<div className="flex w-fit flex-row flex-wrap gap-3 rounded border px-2 pt-5 pb-2 dark:border-slate-300 dark:border-opacity-20 dark:focus-within:border-opacity-60">
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
										<div className="flex w-fit flex-row flex-wrap gap-3 rounded border px-2 pt-5 pb-2 dark:border-slate-300 dark:border-opacity-20 dark:focus-within:border-opacity-60">
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
										<div className="flex w-fit flex-row flex-wrap gap-3 rounded border px-2 pt-5 pb-2 dark:border-slate-300 dark:border-opacity-20 dark:focus-within:border-opacity-60">
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
										<div className="flex w-fit flex-row flex-wrap gap-3 rounded border px-2 pt-5 pb-2 dark:border-slate-300 dark:border-opacity-20 dark:focus-within:border-opacity-60">
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
										<div className="flex w-fit flex-row flex-wrap gap-3 rounded border px-2 pt-5 pb-2 dark:border-slate-300 dark:border-opacity-20 dark:focus-within:border-opacity-60">
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
										<div className="flex w-fit flex-row flex-wrap gap-3 rounded border px-2 pt-5 pb-2 dark:border-slate-300 dark:border-opacity-20 dark:focus-within:border-opacity-60">
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

									<div className="flex w-fit flex-row flex-wrap gap-3 rounded border px-2 pt-5 pb-2 dark:border-slate-300 dark:border-opacity-20 dark:focus-within:border-opacity-60">
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
										<div className="flex w-fit flex-row flex-wrap gap-3 rounded border px-2 pt-5 pb-2 dark:border-slate-300 dark:border-opacity-20 dark:focus-within:border-opacity-60">
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
										<div className="flex w-fit flex-row flex-wrap gap-3 rounded border px-2 pt-5 pb-2 dark:border-slate-300 dark:border-opacity-20 dark:focus-within:border-opacity-60">
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
								</div>

								<div className="flex flex-col gap-2">
									<div>
										<div className="my-auto block w-72 font-medium text-amber-600 dark:text-amber-600">
											{'Enable Labour Wellfare Fund ?'}

											<Field
												type="checkbox"
												name={`enableLabourWelfareFund`}
												className="my-auto ml-4 inline h-4 w-4 rounded accent-teal-600"
											/>
										</div>
									</div>

									{values.enableLabourWelfareFund && (
										<div className="flex w-fit flex-row flex-wrap gap-3 rounded border px-2 pt-5 pb-2 dark:border-slate-300 dark:border-opacity-20 dark:focus-within:border-opacity-60">
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
											<div className="flex w-fit flex-row flex-wrap gap-3 rounded border px-2 pt-5 pb-2 dark:border-slate-300 dark:border-opacity-20 dark:focus-within:border-opacity-60">
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
							</section>

							<div>
								<button
									className="mt-4 whitespace-nowrap rounded bg-teal-500 py-2 px-6 text-base font-medium hover:bg-teal-600 dark:bg-teal-700 dark:hover:bg-teal-600"
									type="submit"
								>
									Update
								</button>
							</div>
						</form>
					)}
				</Formik>
			</section>
		);
	}
};

export default PfEsiSetupForm;
