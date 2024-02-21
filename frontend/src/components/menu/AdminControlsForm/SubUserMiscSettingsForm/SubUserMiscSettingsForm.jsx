import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
	useGetSubUserMiscSettingsQuery,
	useAddSubUserMiscSettingsMutation,
	useUpdateSubUserMiscSettingsMutation,
} from '../../../authentication/api/subUserMiscSettingsApiSlice';
import { useOutletContext } from 'react-router-dom';
import { Formik } from 'formik';
import { Field, ErrorMessage } from 'formik';
import { alertActions } from '../../../authentication/store/slices/alertSlice';
import { FaCircleNotch } from 'react-icons/fa';

const SubUserMiscSettingsForm = () => {
	const dispatch = useDispatch();
	const globalCompany = useSelector((state) => state.globalCompany);
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();
	const {
		data: { company, ...subUserMiscSettings } = {},
		isLoading: isLoadingSubUserMiscSettings,
		isSuccess: isSubUserMiscSettingsSuccess,
		isError: isSubUserMiscSettingsError,
		isFetching: isFetchingSubUserMiscSettings,
	} = useGetSubUserMiscSettingsQuery(globalCompany.id);
	console.log(isSubUserMiscSettingsSuccess);
	console.log(subUserMiscSettings);

	const [
		addSubUserMiscSettings,
		{
			isLoading: isAddingSubUserMiscSettings,
			// isError: errorRegisteringRegular,
			isSuccess: isAddSubUserMiscSettingsSuccess,
		},
	] = useAddSubUserMiscSettingsMutation();
	const [
		updateSubUserMiscSettings,
		{
			isLoading: isUpdateSubUserMiscSettings,
			// isError: errorRegisteringRegular,
			isSuccess: isUpdateSubUserMiscSettingsSuccess,
		},
	] = useUpdateSubUserMiscSettingsMutation();

	const updateButtonClicked = async (values, formikBag) => {
		console.log(values);
		if (isSubUserMiscSettingsSuccess) {
			try {
				const data = await updateSubUserMiscSettings({
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
		} else if (!isSubUserMiscSettingsSuccess) {
			try {
				const data = await addSubUserMiscSettings({
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

	if (isLoadingSubUserMiscSettings) {
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
						<h1 className="text-3xl font-medium">SubUser Misc Settings</h1>
						<p className="my-2 text-sm">Some More settings for Sub User</p>
					</div>
				</div>

				{/* Formik Implementation */}
				<Formik
					initialValues={
						isSubUserMiscSettingsSuccess
							? {
									...subUserMiscSettings,
							  }
							: {
									enableFemaleMaxPunchOut: true,
									maxFemalePunchOut: '19:00',
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
										htmlFor="maxFemalePunchOut"
										className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
									>
										Max Female Punch Out Time
									</label>
									<Field
										type="time"
										name={`maxFemalePunchOut`}
										id={`maxFemalePunchOut`}
										className="h-full w-fit rounded border border-slate-100 border-opacity-50 bg-zinc-800 pl-2 pr-2 text-xs duration-300 sm:text-base"
									/>
									<div className="my-1 text-xs font-bold text-red-500 dark:text-red-700">
										<ErrorMessage name={`maxFemalePunchOut`} />
									</div>
								</div>
								<div>
									<label
										htmlFor="enableFemaleMaxPunchOut"
										className="my-auto font-medium text-blueAccent-700 dark:text-blueAccent-400"
									>
										Enable Female Max Punch Out
										<Field
											type="checkbox"
											name="enableFemaleMaxPunchOut"
											id="enableFemaleMaxPunchOut"
											className="ml-2.5 inline h-4 w-4 translate-y-0.5 rounded accent-teal-600"
										/>
									</label>

									<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
										<ErrorMessage name={`enableFemaleMaxPunchOut`} />
									</div>
								</div>
								<div>
									<button
										className="mt-4 whitespace-nowrap rounded bg-teal-500 py-2 px-6 text-base font-medium hover:bg-teal-600 dark:bg-teal-700 dark:hover:bg-teal-600"
										type="submit"
									>
										{isSubUserMiscSettingsSuccess ? 'Update' : 'Create'}
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

export default SubUserMiscSettingsForm;
