import React, { useState, useEffect } from 'react';
// import authSlice from "./store/slices/auth";
import { useDispatch, useSelector } from 'react-redux';
import {
	useGetWeeklyOffHolidayOffQuery,
	useAddWeeklyOffHolidayOffMutation,
	useUpdatedWeeklyOffHolidayOffMutation,
} from '../../../../authentication/api/weeklyOffHolidayOffApiSlice';
import { Formik } from 'formik';
import { useOutletContext } from 'react-router-dom';
import { FaCircleNotch } from 'react-icons/fa';
import { Field, ErrorMessage } from 'formik';
import { WeeklyOffHolidayOffSchema } from './WeeklyOffHolidayOffSchema';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const WeeklyOffHolidayOffForm = () => {
	const dispatch = useDispatch();

	const globalCompany = useSelector((state) => state.globalCompany);
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();

	const {
		data: { company, ...weeklyOffHolidayOff } = {},
		isLoading,
		isSuccess,
		isError,
		error,
		isFetching,
	} = useGetWeeklyOffHolidayOffQuery(globalCompany.id);

	const [
		addWeeklyOffHolidayOff,
		{
			isLoading: isAddingWeeklyOffHolidayOff,
			// isError: errorRegisteringRegular,
			isSuccess: isAddWeeklyOffHolidayOff,
		},
	] = useAddWeeklyOffHolidayOffMutation();
	const [
		updatedWeeklyOffHolidayOff,
		{
			isLoading: isUpdatingWeeklyOffHolidayOff,
			// isError: errorRegisteringRegular,
			isSuccess: isUpdatingWeeklyOffHolidayOffSuccess,
		},
	] = useUpdatedWeeklyOffHolidayOffMutation();
	const [errorMessage, setErrorMessage] = useState('');

	const updateButtonClicked = async (values, formikBag) => {
		console.log(values);
		try {
			const data = await updatedWeeklyOffHolidayOff({
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
	};

	useEffect(() => {
		setShowLoadingBar(
			isLoading ||
				isAddWeeklyOffHolidayOff ||
				isUpdatingWeeklyOffHolidayOff
		);
	}, [isLoading, isAddWeeklyOffHolidayOff, isUpdatingWeeklyOffHolidayOff]);

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
						<h1 className="text-3xl font-medium">
							Holiday / Weekly Off
						</h1>
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
									...weeklyOffHolidayOff,
							  }
							: {
									minDaysForHolidayOff: '',
									minDaysForWeeklyOff: '',
							  }
					}
					validationSchema={WeeklyOffHolidayOffSchema}
					onSubmit={updateButtonClicked}
				>
					{({ handleSubmit, errors, touched, values }) => (
						// {console.log(values)}
						<form id="" className="mt-2" onSubmit={handleSubmit}>
							<div className="flex w-full flex-col gap-2">
								<div>
									<label
										htmlFor="minDaysForHolidayOff"
										className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
									>
										Minimum Present Days For Holiday Off
									</label>
									<Field
										className={classNames(
											errors.minDaysForHolidayOff &&
												touched.minDaysForHolidayOff
												? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
												: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
											'custom-number-input w-full rounded border-2  bg-zinc-200   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-800 dark:focus:border-opacity-75 lg:w-1/3'
										)}
										type="number"
										name={`minDaysForHolidayOff`}
									/>
									<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
										<ErrorMessage
											name={`minDaysForHolidayOff`}
										/>
									</div>
								</div>
								<div>
									<label
										htmlFor="minDaysForWeeklyOff"
										className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
									>
										Minimum Present Days For Weekly Off
									</label>
									<Field
										className={classNames(
											errors.minDaysForWeeklyOff &&
												touched.minDaysForWeeklyOff
												? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
												: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
											'custom-number-input w-full rounded border-2  bg-zinc-200   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-800 dark:focus:border-opacity-75 lg:w-1/3'
										)}
										type="number"
										name={`minDaysForWeeklyOff`}
									/>
									<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
										<ErrorMessage
											name={`minDaysForWeeklyOff`}
										/>
									</div>
								</div>

								<div>
									<button
										className="mt-4 whitespace-nowrap rounded bg-teal-500 py-2 px-6 text-base font-medium hover:bg-teal-600 dark:bg-teal-700 dark:hover:bg-teal-600"
										type="submit"
									>
										Update
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

export default WeeklyOffHolidayOffForm;
