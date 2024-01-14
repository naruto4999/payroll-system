import React, { useState, useEffect } from 'react';
// import authSlice from "./store/slices/auth";
import { useDispatch, useSelector } from 'react-redux';
import {
	useGetCalculationsQuery,
	useAddCalculationsMutation,
	useUpdateCalculationsMutation,
} from '../../../../authentication/api/calculationsApiSlice';
import { Formik } from 'formik';
import { useOutletContext } from 'react-router-dom';
import { FaCircleNotch } from 'react-icons/fa';
import { Field, ErrorMessage } from 'formik';
// import { WeeklyOffHolidayOffSchema } from './WeeklyOffHolidayOffSchema';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const CalculationsForm = () => {
	const dispatch = useDispatch();

	const globalCompany = useSelector((state) => state.globalCompany);
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();

	const months = [
		'January',
		'February',
		'March',
		'April',
		'May',
		'June',
		'July',
		'August',
		'September',
		'October',
		'November',
		'December',
	];

	const {
		data: { company, ...calculations } = {},
		isLoading,
		isSuccess,
		isError,
		error,
		isFetching,
	} = useGetCalculationsQuery(globalCompany.id);

	console.log(isSuccess);
	const [
		addCalculations,
		{
			isLoading: isAddingCalculations,
			// isError: errorRegisteringRegular,
			isSuccess: isAddCalculationsSuccess,
		},
	] = useAddCalculationsMutation();
	const [
		updateCalculations,
		{
			isLoading: isUpdatingCalculations,
			// isError: errorRegisteringRegular,
			isSuccess: isUpdatingCalculationsSuccess,
		},
	] = useUpdateCalculationsMutation();
	const [errorMessage, setErrorMessage] = useState('');
	console.log(calculations);

	const updateButtonClicked = async (values, formikBag) => {
		console.log(values);
		if (isSuccess) {
			try {
				const data = await updateCalculations({
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
				const data = await addCalculations({
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
		setShowLoadingBar(isLoading || isAddingCalculations || isUpdatingCalculations);
	}, [isLoading, isAddingCalculations, isUpdatingCalculations]);

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
						<h1 className="text-3xl font-medium">Calculations</h1>
						<p className="my-2 text-sm">
							Edit Values for Overtime Time Calculation, EL Calculation, Notice Pay Calculation, Service
							Calculation and Gratuity Calculation
						</p>
					</div>
				</div>

				{/* Formik Implementation */}
				<Formik
					initialValues={
						isSuccess
							? {
									...calculations,
									elDaysCalculation: calculations.elDaysCalculation ?? '',
							  }
							: {
									otCalculation: '26',
									elCalculation: '26',
									noticePay: '30',
									serviceCalculation: '30',
									gratuityCalculation: '26',
									elDaysCalculation: 20,
									bonusStartMonth: 1,
							  }
					}
					validationSchema={''}
					onSubmit={updateButtonClicked}
				>
					{({ handleSubmit, errors, touched, values }) => (
						// {console.log(values)}
						<form id="" className="mt-2" onSubmit={handleSubmit}>
							<div className="flex w-full flex-col gap-2">
								<div>
									<label
										htmlFor="otCalculation"
										className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
									>
										Overtime Calculation
									</label>
									<Field
										as="select"
										name="otCalculation"
										id="otCalculation"
										className="my-1 block rounded-md bg-zinc-300 bg-opacity-50 p-1 dark:bg-zinc-800 "
									>
										<option value="26">26 Days</option>
										<option value="30">30 Days</option>
										<option value="month_days">Monthly Days</option>
									</Field>
									<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
										<ErrorMessage name={`otCalculation`} />
									</div>
								</div>

								<div>
									<label
										htmlFor="elCalculation"
										className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
									>
										EL Calculation
									</label>
									<Field
										as="select"
										name="elCalculation"
										id="elCalculation"
										className="my-1 block rounded-md bg-zinc-300 bg-opacity-50 p-1 dark:bg-zinc-800 "
									>
										<option value="26">26 Days</option>
										<option value="30">30 Days</option>
									</Field>
									<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
										<ErrorMessage name={`elCalculation`} />
									</div>
								</div>

								<div>
									<label
										htmlFor="elDaysCalculation"
										className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
									>
										EL Days Calculation
									</label>
									<Field
										className={classNames(
											errors.elDaysCalculation && touched.elDaysCalculation
												? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
												: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
											'custom-number-input w-20 rounded  border-2 bg-zinc-200 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-800 dark:focus:border-opacity-75'
										)}
										type="number"
										name={`elDaysCalculation`}
										id="elDaysCalculation"
									/>
									<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
										<ErrorMessage name={`elDaysCalculation`} />
									</div>
								</div>

								<div>
									<label
										htmlFor="noticePay"
										className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
									>
										Notice Pay
									</label>
									<Field
										as="select"
										name="noticePay"
										id="noticePay"
										className="my-1 block rounded-md bg-zinc-300 bg-opacity-50 p-1 dark:bg-zinc-800 "
									>
										<option value="26">26 Days</option>
										<option value="30">30 Days</option>
									</Field>
									<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
										<ErrorMessage name={`noticePay`} />
									</div>
								</div>

								<div>
									<label
										htmlFor="serviceCalculation"
										className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
									>
										Service Calculation
									</label>
									<Field
										as="select"
										name="serviceCalculation"
										id="serviceCalculation"
										className="my-1 block rounded-md bg-zinc-300 bg-opacity-50 p-1 dark:bg-zinc-800 "
									>
										<option value="26">26 Days</option>
										<option value="30">30 Days</option>
									</Field>
									<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
										<ErrorMessage name={`serviceCalculation`} />
									</div>
								</div>
								<div>
									<label
										htmlFor="gratuityCalculation"
										className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
									>
										Gratuity Calculation
									</label>
									<Field
										as="select"
										name="gratuityCalculation"
										id="gratuityCalculation"
										className="my-1 block rounded-md bg-zinc-300 bg-opacity-50 p-1 dark:bg-zinc-800 "
									>
										<option value="26">26 Days</option>
										<option value="30">30 Days</option>
									</Field>
									<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
										<ErrorMessage name={`gratuityCalculation`} />
									</div>
								</div>
								<div>
									<label
										htmlFor="bonusStartMonth"
										className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
									>
										Bonus Period
									</label>
									<p className="inline">From: </p>
									<Field
										as="select"
										name="bonusStartMonth"
										id="bonusStartMonth"
										className="my-1 mx-1 inline rounded-md bg-zinc-300 bg-opacity-50 p-1 dark:bg-zinc-800 "
									>
										{months.map((monthName, index) => (
											<option key={index} value={index + 1}>
												{monthName}
											</option>
										))}
									</Field>
									<p className="ml-4 inline">
										To:{' '}
										{
											months[
												(parseInt(values.bonusStartMonth) + 11) % 12 === 0
													? 11
													: ((parseInt(values.bonusStartMonth) + 11) % 12) - 1
											]
										}
									</p>

									<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
										<ErrorMessage name={`bonusStartMonth`} />
									</div>
								</div>

								<div>
									<button
										className="mt-4 whitespace-nowrap rounded bg-teal-500 py-2 px-6 text-base font-medium hover:bg-teal-600 dark:bg-teal-700 dark:hover:bg-teal-600"
										type="submit"
									>
										{isSuccess ? 'Update' : 'Create'}
									</button>
								</div>
							</div>
						</form>
					)}
				</Formik>
			</section>
		);
	}
};

export default CalculationsForm;
