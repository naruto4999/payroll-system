import React, { useMemo, useEffect, useRef, useState } from 'react';
import { Field, ErrorMessage, FieldArray, Formik } from 'formik';
import { FaCircleNotch } from 'react-icons/fa6';

import {
	useGetAllEmployeeMonthlyAttendanceDetailsQuery,
	useGetAllEmployeeSalaryEarningsQuery,
	useEmployeeBulkSalaryPreparedMutation,
	useGetAllEmployeePfEsiDetailsQuery,
} from '../../../../authentication/api/salaryPreparationApiSlice';
import { useGetEarningsHeadsQuery } from '../../../../authentication/api/earningsHeadEntryApiSlice';
import Deductions from './Deductions';
import { useGetAllEmployeeSalaryDetailQuery } from '../../../../authentication/api/timeUpdationApiSlice';
import BigNumber from 'bignumber.js';
import NetSalary from './NetSalary';
import { companyEntryApiSlice } from '../../../../authentication/api/companyEntryApiSlice';
import { useGetCalculationsQuery } from '../../../../authentication/api/calculationsApiSlice';
import ReactModal from 'react-modal';
import ConfirmationModal from '../../../../UI/ConfirmationModal';
import { ConfirmationModalSchema } from './SalaryPreperationSchema';
import { useDispatch, useSelector } from 'react-redux';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import LoadingSpinner from '../../../../UI/LoadingSpinner';

ReactModal.setAppElement('#root');

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const EditSalary = ({
	updateEmployeeId,
	globalCompany,
	values,
	handleChange,
	errors,
	isSubmitting,
	setFieldValue,
	earliestMonthAndYear,
	setSelectedDate,
	handleReset,
	touched,
	isValid,
	handleSubmit,
}) => {
	const auth = useSelector((state) => state.auth);
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
	const dispatch = useDispatch();

	const isDateWithinRange = (fromDate, toDate) => {
		const dateSelected = new Date(Date.UTC(values.year, values.month - 1, 1));
		// console.log('Selected Date', dateSelected);
		const fromDateObj = new Date(fromDate);
		const toDateObj = new Date(toDate);
		return dateSelected >= fromDateObj && dateSelected <= toDateObj;
	};
	const [showConfirmModal, setShowConfirmModal] = useState(false);

	// const {
	//     data: earningsHeads,
	//     isLoading: isLoadingEarningsHeads,
	//     isSuccess: isEarningsHeadsSuccess,
	//     isError: isEarningsHeadsError,
	//     error: earningsHeadsError,
	// } = useGetEarningsHeadsQuery(globalCompany);

	const [
		employeeBulkSalaryPrepared,
		{
			isLoading: isBulkPreparingEmployeeSalaries,
			// isError: errorRegisteringRegular,
			isSuccess: isEmployeeBulkSalaryPrepareddSuccess,
		},
	] = useEmployeeBulkSalaryPreparedMutation();

	const {
		data: companyCalculations,
		isLoading: isLoadingCompanyCalculations,
		isSuccess: isCompanyCalculationsSuccess,
		isError: isCompanyCalculationsError,
	} = useGetCalculationsQuery(globalCompany.id);

	const {
		data: allEmployeeMonthlyAttendanceDetails,
		isLoading: isLoadingAllEmployeeMonthlyAttendanceDetails,
		isSuccess: isAllEmployeeMonthlyAttendanceDetailsSuccess,
		isFetching: isFetchingAllEmployeeMonthlyAttendanceDetails,
	} = useGetAllEmployeeMonthlyAttendanceDetailsQuery(
		{
			company: globalCompany?.id,
			year: values?.year,
		},
		{
			skip: globalCompany === null || globalCompany === '' || values?.year == undefined,
		}
	);

	const {
		data: allEmployeeSalaryDetails,
		isLoading: isLoadingAllEmployeeSalaryDetails,
		isSuccess: isAllEmployeeSalaryDetailsSuccess,
		isFetching: isFetchingAllEmployeeSalaryDetails,
	} = useGetAllEmployeeSalaryDetailQuery(
		{
			company: globalCompany?.id,
		},
		{
			skip: globalCompany === null || globalCompany === '',
		}
	);

	const {
		data: allEmployeeSalaryEarnings,
		isLoading: isLoadingAllEmployeeSalaryEarnings,
		isSuccess: isAllEmployeeSalaryEarningsSuccess,
		isFetching: isFetchingAllEmployeeSalaryEarnings,
	} = useGetAllEmployeeSalaryEarningsQuery(
		{
			company: globalCompany?.id,
			year: values?.year,
		},
		{
			skip: globalCompany === null || globalCompany === '' || values?.year == undefined,
		}
	);

	const {
		data: allEmployeePfEsiDetails,
		isLoading: isLoadingAllEmployeePfEsiDetails,
		isSuccess: isAllEmployeePfEsiDetailsSuccess,
		isFetching: isFetchingAllEmployeePfEsiDetails,
	} = useGetAllEmployeePfEsiDetailsQuery(
		{
			company: globalCompany?.id,
		},
		{
			skip: globalCompany === null || globalCompany === '',
		}
	);

	const currentEmployeeMonthlyAttendanceDetails = useMemo(() => {
		if (allEmployeeMonthlyAttendanceDetails && updateEmployeeId) {
			const selectedEmployeeData = allEmployeeMonthlyAttendanceDetails.filter((item) => {
				const dateOfInstance = new Date(item.date);
				const currentSelectedDate = new Date(Date.UTC(values.year, values.month - 1, 1));
				return item.employee === updateEmployeeId && dateOfInstance.getTime() === currentSelectedDate.getTime();
			});
			return selectedEmployeeData;
		}
		// handleReset();
		return [];
	}, [allEmployeeMonthlyAttendanceDetails, updateEmployeeId]);

	const currentEmployeeSalaryEarning = useMemo(() => {
		const currentEmployeeSalaryEarning =
			allEmployeeSalaryEarnings?.filter(
				(item) => item.employee === updateEmployeeId && isDateWithinRange(item.fromDate, item.toDate)
			) ?? [];
		return currentEmployeeSalaryEarning;
	}, [allEmployeeSalaryEarnings, updateEmployeeId]);

	const currentEmployeePfEsiDetails = useMemo(() => {
		const selectedEmployeeData = allEmployeePfEsiDetails?.filter((item) => item.employee === updateEmployeeId);
		return selectedEmployeeData;
	}, [allEmployeePfEsiDetails, updateEmployeeId]);

	const currentEmployeeSalaryDetails = useMemo(() => {
		const matchingItem = allEmployeeSalaryDetails?.find((item) => item.employee === updateEmployeeId);
		return matchingItem || null; // Return null (or another default value) when no match is found
	}, [allEmployeeSalaryDetails, updateEmployeeId]);

	useEffect(() => {
		if (currentEmployeeMonthlyAttendanceDetails?.length != 0 && updateEmployeeId) {
			setFieldValue(
				'employeeSalaryPrepared.netOtMinutesMonthly',
				currentEmployeeMonthlyAttendanceDetails?.[0]?.netOtMinutesMonthly
			);
		} else if (currentEmployeeMonthlyAttendanceDetails?.length == 0) {
			setFieldValue('employeeSalaryPrepared.netOtMinutesMonthly', 0);
		}
	}, [currentEmployeeMonthlyAttendanceDetails]);

	useEffect(() => {
		if (currentEmployeeSalaryDetails) {
			setFieldValue('employeeSalaryPrepared.paymentMode', currentEmployeeSalaryDetails?.paymentMode);

			if (currentEmployeeSalaryEarning?.length != 0 && currentEmployeeSalaryDetails.overtimeRate != null) {
				const netOtHrsMonthly = new BigNumber(values.employeeSalaryPrepared.netOtMinutesMonthly).dividedBy(
					new BigNumber(60)
				);
				const totalSalaryRate = new BigNumber(
					currentEmployeeSalaryEarning?.reduce((accumulator, item) => {
						return accumulator + Number(item.value || 0); // Use 0 as a default value if earnedAmount is undefined or falsy
					}, 0)
				);
				let overtimeRateMultiplier = new BigNumber(2);
				if (auth.account.role == 'OWNER') {
					overtimeRateMultiplier = new BigNumber(currentEmployeeSalaryDetails?.overtimeRate == 'D' ? 2 : 1);
				}
				let overtimeDivisor = new BigNumber(26);

				// OT Calculation Days
				if (auth.account.role == 'OWNER') {
					if (companyCalculations?.otCalculation == 'month_days') {
						overtimeDivisor = new BigNumber(new Date(values.year, values.month, 0).getDate());
					} else if (
						companyCalculations?.otCalculation != undefined &&
						companyCalculations?.otCalculation != null
					) {
						overtimeDivisor = new BigNumber(companyCalculations?.otCalculation);
					}
				}

				const netOtAmountMonthly = totalSalaryRate
					.dividedBy(overtimeDivisor)
					.dividedBy(new BigNumber(8))
					.multipliedBy(netOtHrsMonthly)
					.multipliedBy(overtimeRateMultiplier);
				setFieldValue('employeeSalaryPrepared.netOtAmountMonthly', Math.round(netOtAmountMonthly.toNumber()));
			}
		} else {
			setFieldValue('employeeSalaryPrepared.paymentMode', '');
			if (currentEmployeeSalaryEarning?.length == 0 || currentEmployeeSalaryDetails?.overtimeRate == null) {
				setFieldValue('employeeSalaryPrepared.netOtAmountMonthly', 0);
			}
		}
	}, [
		currentEmployeeSalaryDetails,
		currentEmployeeSalaryEarning,
		values.employeeSalaryPrepared.netOtMinutesMonthly,
		companyCalculations,
	]);

	useEffect(() => {
		if (
			currentEmployeeSalaryEarning.length != 0 &&
			!isSubmitting &&
			currentEmployeeMonthlyAttendanceDetails?.length != 0
		) {
			const earnedAmountArray = currentEmployeeSalaryEarning.map((item) => ({
				earningsHead: item.earningsHead,
				rate: item.value,
				earnedAmount: Math.round(
					((item.value * 100) / new Date(values.year, values.month, 0).getDate() / 100) *
						(currentEmployeeMonthlyAttendanceDetails?.[0]?.paidDaysCount / 2)
				),
				arearAmount: 0,
			}));
			setFieldValue(`earnedAmount`, earnedAmountArray);
		} else if (currentEmployeeMonthlyAttendanceDetails?.length == 0 || currentEmployeeSalaryEarning?.length == 0) {
			setFieldValue(`earnedAmount`, []);
		}
	}, [
		currentEmployeeSalaryEarning.map((item) => item.value).join(','),
		currentEmployeeMonthlyAttendanceDetails,
		updateEmployeeId,
	]);

	// This use Effect is causing problem with updation of rate
	const prevArearAmounts = useRef(values.earnedAmount.map((item) => item.arearAmount).join(','));

	// Recalculate earned if arrear is added
	useEffect(() => {
		if (prevArearAmounts.current != values.earnedAmount.map((item) => item.arearAmount).join(',')) {
			const updatedEarnedAmount = values.earnedAmount.map((item, index) => {
				const rate = item.rate;
				const year = values.year;
				const month = values.month;
				const daysInMonth = new Date(year, month, 0).getDate();
				const paidDaysCount = currentEmployeeMonthlyAttendanceDetails?.[0]?.paidDaysCount || 0;
				const arearAmount = item.arearAmount || 0;
				const earnedAmount = Math.round(((rate * 100) / daysInMonth / 100) * (paidDaysCount / 2)) + arearAmount;

				return { ...item, earnedAmount };
			});
			if (updatedEarnedAmount.length != 0) {
				setFieldValue('earnedAmount', updatedEarnedAmount);
			}
			prevArearAmounts.current = values.earnedAmount.map((item) => item.arearAmount).join(',');
		}
	}, [values.earnedAmount.map((item) => item.arearAmount).join(',')]);

	const optionsForYear = useMemo(() => {
		if (earliestMonthAndYear) {
			const options = [];
			for (let i = earliestMonthAndYear.earliestYear; i <= new Date().getFullYear(); i++) {
				options.push(
					<option key={i} value={i}>
						{i}
					</option>
				);
			}
			return options;
		}
	}, [earliestMonthAndYear]);

	const bulkPrepareSalaries = async (formikBag) => {
		console.log(values.year);
		console.log(values.month);
		let toSend = {
			company: globalCompany.id,
			month: values.month,
			year: values.year,
		};
		try {
			// setShowLoadingBar(true);
			const startTime = performance.now();
			const data = await employeeBulkSalaryPrepared(toSend).unwrap();
			const endTime = performance.now(); // Record the end time
			const responseTime = endTime - startTime;
			const responseTimeInSeconds = (responseTime / 1000).toFixed(2);
			dispatch(
				alertActions.createAlert({
					message: `Saved, Time Taken: ${responseTimeInSeconds} seconds`,
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
	if (
		isLoadingCompanyCalculations ||
		isLoadingAllEmployeeMonthlyAttendanceDetails ||
		isLoadingAllEmployeeSalaryDetails ||
		isLoadingAllEmployeeSalaryEarnings ||
		isLoadingAllEmployeePfEsiDetails
	) {
		return (
			<div className="mx-auto">
				<LoadingSpinner />
			</div>
		);
	} else if (
		currentEmployeeMonthlyAttendanceDetails?.length == 0 ||
		currentEmployeeSalaryEarning?.length == 0 ||
		currentEmployeeSalaryDetails == null ||
		currentEmployeePfEsiDetails?.length == 0
	) {
		return (
			<div>
				<section>
					<label
						htmlFor="year"
						className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
					>
						Month and Year :
					</label>
					<select
						name="month"
						id="month"
						value={values.month}
						onChange={(e) => {
							handleChange(e);
							setSelectedDate((prevValue) => ({ ...prevValue, month: e.target.value }));
						}}
						className="my-1 mr-2 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
					>
						{months.map((month, index) => {
							return (
								<option key={index} value={index + 1}>
									{month}
								</option>
							);
						})}
					</select>

					<select
						name="year"
						id="year"
						onChange={(e) => {
							handleChange(e);
							setSelectedDate((prevValue) => ({ ...prevValue, year: e.target.value }));
						}}
						value={values.year}
						className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
					>
						{optionsForYear}
					</select>
				</section>
				<section>
					{currentEmployeeMonthlyAttendanceDetails?.length == 0 && (
						<h2 className="mx-auto text-lg dark:text-red-600">
							This Employee has no attendance in {`${months[values.month - 1]}, ${values.year}`}
						</h2>
					)}
					{currentEmployeePfEsiDetails?.length == 0 && (
						<h2 className="mx-auto text-lg dark:text-red-600">
							PF ESI Details haven't been added for this employee
						</h2>
					)}
					{!currentEmployeeSalaryDetails && (
						<h2 className="mx-auto text-lg dark:text-red-600">
							Salary Details hasn't been added for this employee
						</h2>
					)}
				</section>
			</div>
		);
	} else {
		return (
			<div>
				<div>
					<h3 className="text-lg font-bold text-blueAccent-600">{'Default Mode'}</h3>
					<div className="my-2 text-xs text-slate-300">
						<p>
							1. The amounts listed below will be used for salary calculation and do not represent the
							already prepared salary.
						</p>
					</div>
				</div>
				<section>
					<label
						htmlFor="year"
						className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
					>
						Month and Year :
					</label>
					<select
						name="month"
						id="month"
						value={values.month}
						onChange={(e) => {
							handleChange(e);
							setSelectedDate((prevValue) => ({ ...prevValue, month: e.target.value }));
						}}
						className="my-1 mr-2 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
					>
						{months.map((month, index) => {
							return (
								<option key={index} value={index + 1}>
									{month}
								</option>
							);
						})}
					</select>

					<select
						name="year"
						id="year"
						onChange={(e) => {
							handleChange(e);
							setSelectedDate((prevValue) => ({ ...prevValue, year: e.target.value }));
						}}
						value={values.year}
						className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
					>
						{optionsForYear}
					</select>
				</section>
				<section className="mt-2 flex flex-row gap-4">
					<div className="w-full">
						<table className="w-full border-collapse text-center text-xs">
							<thead className="sticky top-0 z-20 bg-yellow-600 dark:bg-yellow-700 dark:bg-opacity-40">
								<tr>
									<th className="border border-slate-400 border-opacity-60 px-4 py-2 font-medium">
										Earning Head
									</th>
									<th className="border border-slate-400 border-opacity-60 px-4 py-2 font-medium">
										Rate
									</th>
									<th className="border border-slate-400 border-opacity-60 px-4 py-2 font-medium">
										Arear
									</th>
									<th className="border border-slate-400 border-opacity-60 px-4 py-2 font-medium">
										Earned
									</th>
								</tr>
							</thead>
							<tbody className="max-h-20 divide-y divide-black divide-opacity-50 overflow-y-auto border-t border-black border-opacity-50 ">
								{values?.earnedAmount
									?.sort((a, b) => a.earningsHead.id - b.earningsHead.id)
									?.map((earning, index) => {
										return (
											<tr
												key={index}
												className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50"
											>
												<td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
													{earning.earningsHead.name}
												</td>
												<td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
													{earning.rate}
												</td>
												<td className="relative border border-slate-400 border-opacity-60 bg-opacity-50 p-0 font-normal dark:bg-zinc-800">
													<Field
														className="custom-number-input h-8 w-32 bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
														type="number"
														name={`earnedAmount.${index}.arearAmount`}
													/>
												</td>
												<td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal dark:text-green-600">
													{earning.earnedAmount}
												</td>
											</tr>
										);
									})}
								{/* Calculate total rate */}
								<tr>
									<td className="relative  px-4 py-2 font-medium text-orange-500">Total</td>
									<td className="relative  px-4 py-2 font-medium text-orange-500">
										{values.earnedAmount?.reduce((total, earning) => total + earning.rate, 0)}
									</td>
									<td className="relative  px-4 py-2 font-medium text-orange-500">
										{values.earnedAmount?.reduce((total, earning) => {
											if (
												earning.arearAmount != '' &&
												earning.arearAmount != null &&
												earning.arearAmount != undefined
											) {
												return total + earning.arearAmount;
											}
											return total;
										}, 0)}
									</td>
									<td className="relative  px-4 py-2 font-medium text-orange-500">
										{values.earnedAmount?.reduce(
											(total, earning) => total + earning.earnedAmount,
											0
										)}
									</td>
								</tr>
							</tbody>
						</table>
					</div>
					<Deductions
						globalCompany={globalCompany}
						updateEmployeeId={updateEmployeeId}
						values={values}
						setFieldValue={setFieldValue}
						currentEmployeeSalaryDetails={currentEmployeeSalaryDetails}
						currentEmployeePfEsiDetails={currentEmployeePfEsiDetails}
					/>
				</section>
				<section className="mt-10 flex flex-row justify-between">
					<div className="flex flex-col gap-4">
						<div>
							<h5 className="inline dark:text-slate-300">Paid Days: </h5>
							<span className=" m-1 font-bold dark:text-green-600">
								{currentEmployeeMonthlyAttendanceDetails?.[0]?.paidDaysCount / 2 || 0}
							</span>
						</div>
						<div>
							<label
								htmlFor={`employeeSalaryPrepared.incentiveAmount`}
								className=" font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							>
								Incentive:{' '}
							</label>
							<Field
								className={classNames(
									errors.employeeSalaryPrepared?.incentiveAmount &&
										touched.employeeSalaryPrepared?.incentiveAmount
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input  ml-1 w-32 rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-800 dark:focus:border-opacity-75'
								)}
								type="number"
								name={`employeeSalaryPrepared.incentiveAmount`}
							/>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name={`employeeSalaryPrepared.incentiveAmount`} />
							</div>
						</div>
					</div>

					<div className="flex flex-col gap-4">
						<div>
							<h5 className="inline dark:text-slate-300">Overtime Duration: </h5>
							<span className="ml-1 font-bold dark:text-green-600">
								{`${String(Math.floor(values.employeeSalaryPrepared.netOtMinutesMonthly / 60)).padStart(
									2,
									'0'
								)}:${String(values.employeeSalaryPrepared.netOtMinutesMonthly % 60).padStart(2, '0')}`}
							</span>
						</div>

						<div>
							<h5 className="inline dark:text-slate-300">Overtime Amount: </h5>
							<span className="ml-1 font-bold dark:text-green-600">
								{values.employeeSalaryPrepared.netOtAmountMonthly}
							</span>
						</div>
					</div>
				</section>
				<section className="w-full">
					<p className="mx-auto mt-6 w-fit dark:text-yellow-600">
						Total Before Deductions :{' '}
						{(Number(values?.employeeSalaryPrepared?.netOtAmountMonthly) || 0) +
							(values?.employeeSalaryPrepared?.incentiveAmount === ''
								? 0
								: Number(values?.employeeSalaryPrepared?.incentiveAmount)) +
							values?.earnedAmount?.reduce((accumulator, item) => {
								// Convert the earnedAmount property to a number and add it to the accumulator
								return accumulator + Number(item.earnedAmount || 0); // Use 0 as a default value if earnedAmount is undefined or falsy
							}, 0)}
					</p>
					<NetSalary values={values} updateEmployeeId={updateEmployeeId} />
				</section>
				<section>
					<div className="mt-4 mb-2 flex w-fit flex-row gap-4">
						<button
							className={classNames(
								isValid ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
								'h-10 w-fit rounded bg-teal-500 p-2 px-4 text-base font-medium dark:bg-teal-700'
							)}
							type="submit"
							disabled={!isValid}
							onClick={handleSubmit}
						>
							Update
							{isSubmitting && (
								<FaCircleNotch className="my-auto ml-2 inline animate-spin text-xl text-amber-700 dark:text-amber-600 " />
							)}
						</button>
						<button
							className="h-10 w-fit rounded  bg-blueAccent-400 p-2 px-4 text-base font-medium hover:bg-blueAccent-500 dark:bg-blueAccent-700 dark:hover:bg-blueAccent-600"
							type="submit"
							// disabled={!isValid}
							onClick={() => {
								setShowConfirmModal(true);
							}}
						>
							Bulk Prepare Salaries
							{isSubmitting && (
								<FaCircleNotch className="my-auto ml-2 inline animate-spin text-xl text-amber-700 dark:text-amber-600 " />
							)}
						</button>
					</div>
				</section>
				<ReactModal
					className="items-left fixed inset-0 mx-2 my-auto flex h-fit flex-col gap-4 rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-lg"
					isOpen={showConfirmModal}
					onRequestClose={() => setShowConfirmModal(false || isBulkPreparingEmployeeSalaries)}
					style={{
						overlay: {
							backgroundColor: 'rgba(0, 0, 0, 0.75)',
						},
					}}
				>
					<Formik
						initialValues={{ userInput: '' }}
						validationSchema={ConfirmationModalSchema}
						onSubmit={bulkPrepareSalaries}
						component={(props) => (
							<ConfirmationModal
								{...props}
								displayHeading={'Bulk Prepare Salaries'}
								isBulkPreparingEmployeeSalaries={isBulkPreparingEmployeeSalaries}
								setShowConfirmModal={setShowConfirmModal}
							/>
						)}
					/>
				</ReactModal>
			</div>
		);
	}
};

export default EditSalary;
