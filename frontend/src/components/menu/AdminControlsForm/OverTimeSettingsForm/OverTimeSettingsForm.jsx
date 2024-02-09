import React, { useState, useMemo } from 'react';
import MonthYearSelector from '../../Reports/forms/MonthYearSelector';
import { useGetEmployeePersonalDetailsQuery } from '../../../authentication/api/employeeEntryApiSlice';
import { useDispatch, useSelector } from 'react-redux';
import EditOverTimeSettings from './EditOverTimeSettings';
import { Formik } from 'formik';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const OverTimeSettingsForm = () => {
	const globalCompany = useSelector((state) => state.globalCompany);

	const [selectedDate, setSelectedDate] = useState({
		year: new Date().getFullYear(),
		month: new Date().getMonth() + 1,
	});
	console.log(selectedDate);
	const {
		data: employeePersonalDetails,
		isLoading: isLoadingEmployeePersonalDetails,
		isSuccess: isSuccessEmployeePersonalDetails,
	} = useGetEmployeePersonalDetailsQuery(globalCompany);

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
		dayArray.map((day, index) => (initialValues.dayArray[index] = { day: day, maxOtHrs: 0 }));

		// for (let day = 1; day <= daysInMonth; day++) {
		// 	initialValues.dayWiseShifts[day] = '';
		// }
		return initialValues;
	};
	const initialValues = useMemo(() => generateInitialValues(), []);
	console.log(initialValues);

	const updateButtonClicked = async (values, formikBag) => {
		console.log(values);
	};
	return (
		<div className="m-4 mx-auto max-w-5xl">
			<MonthYearSelector
				setSelectedDate={setSelectedDate}
				selectedDate={selectedDate}
				earliestMonthAndYear={earliestMonthAndYear}
			/>
			<Formik
				initialValues={initialValues}
				validationSchema={''}
				onSubmit={updateButtonClicked}
				component={(props) => <EditOverTimeSettings {...props} selectedDate={selectedDate} />}
			/>
		</div>
	);
};

export default OverTimeSettingsForm;
