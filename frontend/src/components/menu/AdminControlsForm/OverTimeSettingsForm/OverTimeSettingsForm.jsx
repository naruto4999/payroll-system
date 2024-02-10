import React, { useState, useMemo } from 'react';
import MonthYearSelector from '../../Reports/forms/MonthYearSelector';
import { useGetEmployeePersonalDetailsQuery } from '../../../authentication/api/employeeEntryApiSlice';
import { useUpdateOverTimeSettingsMutation } from '../../../authentication/api/overTimeSettingsApiSlice';
import { useDispatch, useSelector } from 'react-redux';
import EditOverTimeSettings from './EditOverTimeSettings';
import { alertActions } from '../../../authentication/store/slices/alertSlice';
import { Formik } from 'formik';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const OverTimeSettingsForm = () => {
	const dispatch = useDispatch();
	const globalCompany = useSelector((state) => state.globalCompany);

	const [selectedDate, setSelectedDate] = useState({
		year: new Date().getFullYear(),
		month: new Date().getMonth() + 1,
	});
	const {
		data: employeePersonalDetails,
		isLoading: isLoadingEmployeePersonalDetails,
		isSuccess: isSuccessEmployeePersonalDetails,
	} = useGetEmployeePersonalDetailsQuery(globalCompany);

	const [
		updateOverTimeSettings,
		{
			isLoading: isUpdatingOverTimeSettings,
			// isError: errorRegisteringRegular,
			isSuccess: isUpdateOverTimeSettingsSuccess,
		},
	] = useUpdateOverTimeSettingsMutation();

	const earliestMonthAndYear = useMemo(() => {
		let earliestDate = Infinity; // Initialize earliestDate to a very large value
		let earliestMonth = '';
		let earliestYear = '';
		if (employeePersonalDetails) {
			for (const employee of employeePersonalDetails) {
				const dateOfJoining = new Date(employee.dateOfJoining);

				if (dateOfJoining < earliestDate) {
					earliestDate = dateOfJoining;
					earliestMonth = dateOfJoining.getMonth() + 1;
					earliestYear = dateOfJoining.getFullYear();
				}
			}
		}
		return {
			earliestMonth: earliestMonth,
			earliestYear: earliestYear,
		};
	}, [employeePersonalDetails]);

	const generateInitialValues = () => {
		// get method returns a zero-based index for the month
		const firstDayOfMonth = new Date(selectedDate.year, selectedDate.month - 1, 1);
		const daysInMonth = new Date(selectedDate.year, selectedDate.month, 0).getDate();
		const dayArray = Array.from({ length: daysInMonth }, (_, index) => index + 1);
		// const dayOfWeek = firstDayOfMonth.getDay();

		const initialValues = { dayArray: [] };
		dayArray.map((day, index) => (initialValues.dayArray[index] = { day: day, maxOtHrs: '' }));

		// for (let day = 1; day <= daysInMonth; day++) {
		// 	initialValues.dayWiseShifts[day] = '';
		// }
		return initialValues;
	};
	const initialValues = useMemo(() => generateInitialValues(), []);

	const updateButtonClicked = async (values, formikBag) => {
		console.log(values);
		const filteredArray = values.dayArray.filter((obj) => Number.isInteger(obj.maxOtHrs) && obj.maxOtHrs > 0);
		console.log(filteredArray);
		let toSend = {
			dayArray: filteredArray,
			company: globalCompany.id,
			year: selectedDate.year,
			month: selectedDate.month,
		};

		try {
			const data = await updateOverTimeSettings(toSend).unwrap();

			dispatch(
				alertActions.createAlert({
					message: `Saved`,
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
	return (
		<div className="m-4 max-w-6xl">
			<div className="flex  flex-row flex-wrap place-content-between">
				<div className="mr-4">
					<h1 className="text-3xl font-medium">Over Time Settings</h1>
					<p className="my-2 text-sm">
						Change the maximum amount of OT that will be shown in the sub user account on each day
					</p>
				</div>
			</div>
			<section className="">
				<MonthYearSelector
					setSelectedDate={setSelectedDate}
					selectedDate={selectedDate}
					earliestMonthAndYear={earliestMonthAndYear}
				/>
				<Formik
					initialValues={initialValues}
					validationSchema={''}
					onSubmit={updateButtonClicked}
					component={(props) => (
						<EditOverTimeSettings {...props} selectedDate={selectedDate} globalCompany={globalCompany} />
					)}
				/>
			</section>
		</div>
	);
};

export default OverTimeSettingsForm;
