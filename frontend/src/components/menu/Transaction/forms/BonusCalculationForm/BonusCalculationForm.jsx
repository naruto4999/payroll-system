import React, { useState, useMemo, useEffect } from 'react';
import { useGetEmployeePersonalDetailsQuery } from '../../../../authentication/api/employeeEntryApiSlice';
import { useDispatch, useSelector } from 'react-redux';
import YearSelector from './YearSelector';
import { useGetCalculationsQuery } from '../../../../authentication/api/calculationsApiSlice';
import TableHeader from './TableHeader';
import { Formik } from 'formik';
import { useGetCategoriesQuery } from '../../../../authentication/api/categoryEntryApiSlice';
import { current } from '@reduxjs/toolkit';
import { FaCircleNotch } from 'react-icons/fa';
import { Field, ErrorMessage } from 'formik';
import {
	useAddOrUpdateBonusCalculationMutation,
	useGetBonusCalculationsQuery,
	useGetBonusPercentageQuery,
} from '../../../../authentication/api/bonusCalculationApiSlice';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import Table from './Table';
import { useOutletContext } from 'react-router-dom';

const BonusCalculationForm = () => {
	const globalCompany = useSelector((state) => state.globalCompany);
	const dispatch = useDispatch();
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();

	const [selectedDate, setSelectedDate] = useState({
		year: new Date().getFullYear(),
	});

	const {
		data: { company, ...calculations } = {},
		isLoading,
		isSuccess,
		isError,
		error,
		isFetching,
	} = useGetCalculationsQuery(globalCompany.id);

	const {
		data: bonusPercentage,
		isLoadingBonusPercentage,
		isBonusPercentageSuccess,
		isBonusPercentageError,
		errorbonusPercentage,
		isFetchingbonusPercentage,
	} = useGetBonusPercentageQuery(globalCompany.id);

	console.log(bonusPercentage);

	const {
		data: categories,
		isLoadingCategories,
		isSuccessCategories,
		isErrorCategories,
		errorCategories,
		isFetchingCategories,
	} = useGetCategoriesQuery(globalCompany);

	const {
		data: bonusCalculations,
		isLoadingbonusCalculations,
		isSuccessbonusCalculations,
		isErrorbonusCalculations,
		errorbonusCalculations,
		isFetchingbonusCalculations,
	} = useGetBonusCalculationsQuery(
		{
			company: globalCompany.id,
			startDate: `${selectedDate.year}-${calculations.bonusStartMonth < 10 ? '0' : ''}${
				calculations.bonusStartMonth
			}-01`,
			endDate: `${parseInt(selectedDate.year) + Math.floor((calculations.bonusStartMonth - 1 + 11) / 12)}-${(
				((calculations.bonusStartMonth - 1 + 11) % 12) +
				1
			)
				.toString()
				.padStart(2, '0')}-01`,
		},
		{ skip: isLoadingCategories || isLoading }
	);

	const categorizedBonusCalculations = useMemo(() => {
		if (bonusCalculations != undefined) {
			return bonusCalculations.reduce((result, obj) => {
				const { category, date, amount } = obj;

				if (!result[category]) {
					result[category] = {};
				}

				result[category][date] = amount;

				return result;
			}, {});
		}
	}, [bonusCalculations]);

	const [
		addOrUpdateBonusCalculation,
		{
			isLoading: isAddingOrUpdatingBonusCalculation,
			// isError: errorRegisteringRegular,
			isSuccess: isAddingOrUpdatingBonusCalculationSuccess,
		},
	] = useAddOrUpdateBonusCalculationMutation();

	const {
		data: employeePersonalDetails,
		isLoading: isLoadingEmployeePersonalDetails,
		isSuccess: isSuccessEmployeePersonalDetails,
	} = useGetEmployeePersonalDetailsQuery(globalCompany);

	const updateButtonClicked = async (values, formikBag) => {
		console.log(values);
		let toSend = {
			calculations: { ...values.bonusCalculationsMonthWise },
			company: globalCompany.id,
			bonusPercentage: values.bonusPercentage,
		};
		try {
			const data = await addOrUpdateBonusCalculation(toSend).unwrap();
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

	const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

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

	// const generateInitialValues = () => {
	// 	let initialValues = {};
	// 	if (categories != undefined) {
	// 		initialValues = categories.map((category) => {
	// 			initialValues[category.id] = {};

	// 			const startDate = new Date(Date.UTC(selectedDate.year, calculations.bonusStartMonth - 1, 1));
	// 			let currentDate = startDate;
	// 			for (let i = 1; i <= 11; i++) {
	// 				let currentMonth = currentDate.getMonth();
	// 				let currentYear = currentDate.getFullYear();
	// 				const newMonth = (currentMonth + 1) % 12;
	// 				currentDate.setMonth(newMonth);
	// 				if (newMonth < currentMonth) {
	// 					currentDate.setFullYear(currentYear + 1);
	// 				}
	// 				const year = currentDate.getFullYear();
	// 				const month = currentDate.getMonth() + 1;
	// 				const day = currentDate.getDate();

	// 				initialValues[category.id][`${year}-${month}-${day}`] = 0;
	// 			}
	// 		});

	// 		// for (let day = 1; day <= daysInMonth; day++) {
	// 		// 	initialValues.dayWiseShifts[day] = '';
	// 		// }
	// 	}
	// 	return initialValues;
	// };
	const generateInitialValues = () => {
		let initialValues = {
			bonusPercentage: bonusPercentage != undefined ? bonusPercentage[0].bonusPercentage : 8.33,
			bonusCalculationsMonthWise: {},
		};
		if (categories !== undefined) {
			categories.forEach((category) => {
				initialValues['bonusCalculationsMonthWise'][category.id] = {};

				const startDate = new Date(Date.UTC(selectedDate.year, calculations.bonusStartMonth - 1, 1));
				let currentDate = startDate;

				for (let i = 0; i < 12; i++) {
					let year = currentDate.getFullYear();
					let month = currentDate.getMonth() + 1;
					let day = currentDate.getDate();

					initialValues['bonusCalculationsMonthWise'][category.id][
						`${year}-${month < 10 ? '0' : ''}${month}-${day < 10 ? '0' : ''}${day}`
					] = 0;

					// Move to the next month
					currentDate.setMonth(currentDate.getMonth() + 1);
				}
			});
		}
		return initialValues;
	};

	const initialValues = useMemo(
		() => generateInitialValues(),
		[categories, calculations, parseInt(selectedDate.year), bonusPercentage]
	);
	console.log(initialValues);

	useEffect(() => {
		setShowLoadingBar(
			isLoading ||
				isLoadingEmployeePersonalDetails ||
				isLoadingCategories ||
				isLoadingbonusCalculations ||
				isAddingOrUpdatingBonusCalculation
		);
	}, [
		isLoading,
		isLoadingEmployeePersonalDetails,
		isLoadingCategories,
		isLoadingbonusCalculations,
		isAddingOrUpdatingBonusCalculation,
	]);

	if (
		isLoading ||
		isLoadingEmployeePersonalDetails ||
		isLoadingCategories ||
		isLoadingbonusCalculations ||
		Object.keys(initialValues).length == 0
	) {
		return (
			<div className="fixed inset-0 z-50 mx-auto my-auto flex h-fit w-fit items-center rounded bg-indigo-600 p-2 font-medium">
				<FaCircleNotch className="mr-2 animate-spin text-white" />
				Processing...
			</div>
		);
	} else {
		return (
			<section className="mt-4 w-full">
				<div className="ml-4 flex flex-row flex-wrap place-content-between">
					<div className="mr-4">
						<h1 className="text-3xl font-medium">Bonus Calculation</h1>
						<p className="my-2 text-sm">Manage bonus calculations here</p>
					</div>
				</div>
				<div className="ml-4">
					<YearSelector
						earliestMonthAndYear={earliestMonthAndYear}
						setSelectedDate={setSelectedDate}
						selectedDate={selectedDate}
					/>
				</div>
				<div className="mx-4">
					<Formik
						initialValues={initialValues}
						validationSchema={''}
						onSubmit={updateButtonClicked}
						component={(props) => (
							<Table
								{...props}
								selectedDate={selectedDate}
								categorizedBonusCalculations={categorizedBonusCalculations}
								calculations={calculations}
								categories={categories}
							/>
						)}
					/>
				</div>
			</section>
		);
	}
};

export default BonusCalculationForm;
