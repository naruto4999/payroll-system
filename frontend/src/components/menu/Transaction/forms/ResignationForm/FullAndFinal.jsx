import React, { useEffect, useState, useMemo } from 'react';
import { useGetSingleEmployeePersonalDetailQuery } from '../../../../authentication/api/employeeEntryApiSlice';
import { useGetSingleEmployeeProfessionalDetailPrefetchQuery } from '../../../../authentication/api/resignationApiSlice';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import { useDispatch, useSelector } from 'react-redux';

import {
	useGetFullAndFinalQuery,
	useGetElLeftQuery,
	useGetYearlyBonusAmountQuery,
	useEarnedAmountWithPreparedSalaryQuery,
} from '../../../../authentication/api/fullAndFinalApiSlice';
import { useGetCalculationsQuery } from '../../../../authentication/api/calculationsApiSlice';
// import { useEarnedAmountWithPreparedSalaryQuery } from '../../../../authentication/api/fullAndFinalApiSlice';

import { Field, ErrorMessage } from 'formik';
import EarningsTable from './EarningsTable';
import DeductionsTable from './DeductionsTable';
import { FaCalculator } from 'react-icons/fa6';
import BigNumber from 'bignumber.js';
import { FaCircleNotch } from 'react-icons/fa';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const dateDifference = (date1, date2) => {
	const [year1, month1, day1] = date1.split('-').map(Number);
	const [year2, month2, day2] = date2.split('-').map(Number);

	const date1Obj = new Date(year1, month1 - 1, day1);
	const date2Obj = new Date(year2, month2 - 1, day2);

	const timeDifference = date2Obj - date1Obj;

	const yearsDifference =
		date2Obj.getMonth() > date1Obj.getMonth() ||
		(date2Obj.getDate() >= date1Obj.getDate() && date2Obj.getMonth() == date1Obj.getMonth())
			? date2Obj.getFullYear() - date1Obj.getFullYear()
			: date2Obj.getFullYear() - date1Obj.getFullYear() - 1;
	const monthsDifference =
		date2Obj.getMonth() > date1Obj.getMonth() ||
		(date2Obj.getMonth() == date1Obj.getMonth() && date2Obj.getDate() >= date1Obj.getDate())
			? date2Obj.getMonth() - date1Obj.getMonth()
			: date2Obj.getMonth() < date1Obj.getMonth()
			? date2Obj.getMonth() + 12 - date1Obj.getMonth()
			: date2Obj.getMonth() == date1Obj.getMonth() &&
			  date2Obj.getDate() < date1Obj.getDate() &&
			  date2Obj.getFullYear() > date1Obj.getFullYear()
			? 11
			: 0;
	const daysDifference =
		date2Obj.getDate() >= date1Obj.getDate()
			? date2Obj.getDate() - date1Obj.getDate()
			: new Date(date2Obj.getFullYear(), date2Obj.getMonth(), 0).getDate() -
			  date1Obj.getDate() +
			  date2Obj.getDate();

	return {
		years: yearsDifference,
		months: monthsDifference,
		days: daysDifference,
		totalMilliseconds: timeDifference,
	};
};

const FullAndFinal = ({
	fullAndFinalEmployeeId,
	globalCompany,
	handleChange,
	values,
	isValid,
	handleSubmit,
	isSubmitting,
	setFieldValue,
	generateButtonClicked,
}) => {
	const dispatch = useDispatch();

	const {
		data: companyCalculations,
		isLoading: isLoadingCompanyCalculations,
		isSuccess: isCompanyCalculationsSuccess,
		isError: isCompanyCalculationsError,
	} = useGetCalculationsQuery(globalCompany.id);

	const {
		data: earnedAmountWithPreparedSalary,
		isLoading: isLoadingEarnedAmountWithPreparedSalary,
		isSuccess: isEarnedAmountWithPreparedSalarySuccess,
		isError: isEarnedAmountWithPreparedSalaryError,
	} = useEarnedAmountWithPreparedSalaryQuery({ company: globalCompany.id, employee: fullAndFinalEmployeeId });
	const [durationWorked, setDurationWorked] = useState(null);
	console.log(earnedAmountWithPreparedSalary);

	const {
		data: employeePersonalDetail,
		isLoadingEmployeePersonalDetail,
		isEmployeePersonalDetailSuccess,
		isEmployeePersonalDetailError,
		errorEmployeePersonalDetail,
	} = useGetSingleEmployeePersonalDetailQuery({ company: globalCompany.id, id: fullAndFinalEmployeeId });

	const {
		data: elLeftObj,
		isLoadingElLeft,
		isElLeftSuccess,
		isElLeftError,
		errorElLeft,
	} = useGetElLeftQuery({ company: globalCompany.id, employee: fullAndFinalEmployeeId });

	const {
		data: employeeFullAndFinal,
		isLoadingEmployeeFullAndFinal,
		isSuccess: isEmployeeFullAndFinalSuccess,
		isEmployeeFullAndFinalError,
		errorEmployeeFullAndFinal,
	} = useGetFullAndFinalQuery({ company: globalCompany.id, employee: fullAndFinalEmployeeId });
	console.log(isEmployeeFullAndFinalSuccess);

	const {
		data: employeeProfessionalDetail,
		isLoadingEmployeeProfessionalDetail,
		isEmployeeProfessionalDetailSuccess,
		isEmployeeProfessionalDetailError,
		errorEmployeeProfessionalDetail,
	} = useGetSingleEmployeeProfessionalDetailPrefetchQuery({ company: globalCompany.id, id: fullAndFinalEmployeeId });

	// Current Year Bonus Amount
	const {
		data: currentYearBonusAmount,
		isLoading: isLoadingCurrentYearBonusAmount,
		isSuccess: isCurrentYearBonusAmountSuccess,
		isError: isCurrentYearBonusAmountError,
	} = useGetYearlyBonusAmountQuery(
		{
			company: globalCompany.id,
			employee: fullAndFinalEmployeeId,
			year: new Date(employeeProfessionalDetail?.resignationDate).getFullYear() - 1,
		},
		{ skip: globalCompany === null || globalCompany === '' || employeeProfessionalDetail == undefined }
	);

	// Prev Year Bonus Amount
	const {
		data: previousYearBonusAmount,
		isLoading: isLoadingPreviousYearBonusAmount,
		isSuccess: isPreviousYearBonusAmountSuccess,
		isError: isPreviousYearBonusAmountError,
	} = useGetYearlyBonusAmountQuery(
		{
			company: globalCompany.id,
			employee: fullAndFinalEmployeeId,
			year: new Date(employeeProfessionalDetail?.resignationDate).getFullYear() - 2,
		},
		{ skip: globalCompany === null || globalCompany === '' || employeeProfessionalDetail == undefined }
	);
	// if (employeePersonalDetail && employeeProfessionalDetail) {
	// 	console.log(
	// 		dateDifference(employeeProfessionalDetail?.dateOfJoining, employeeProfessionalDetail?.resignationDate)
	// 	);
	// }
	useEffect(() => {
		if (employeePersonalDetail && employeeProfessionalDetail) {
			setDurationWorked(
				dateDifference(employeeProfessionalDetail?.dateOfJoining, employeeProfessionalDetail?.resignationDate)
			);
		}
	}, [employeeProfessionalDetail, employeePersonalDetail]);
	useEffect(() => {
		if (employeeFullAndFinal && !isSubmitting) {
			setFieldValue('fullAndFinalDate', employeeFullAndFinal?.fullAndFinalDate);
			setFieldValue('elEncashmentDays', employeeFullAndFinal?.elEncashmentDays);
			setFieldValue('elEncashmentAmount', employeeFullAndFinal?.elEncashmentAmount);
			setFieldValue('bonusPrevYear', employeeFullAndFinal?.bonusPrevYear);
			setFieldValue('bonusCurrentYear', employeeFullAndFinal?.bonusCurrentYear);
			setFieldValue('gratuity', employeeFullAndFinal?.gratuity);
			setFieldValue('serviceCompensationDays', employeeFullAndFinal?.serviceCompensationDays);
			setFieldValue('serviceCompensationAmount', employeeFullAndFinal?.serviceCompensationAmount);
			setFieldValue('earningsNoticePeriodDays', employeeFullAndFinal?.earningsNoticePeriodDays);
			setFieldValue('earningsNoticePeriodAmount', employeeFullAndFinal?.earningsNoticePeriodAmount);
			setFieldValue('otMin', employeeFullAndFinal?.otMin);
			setFieldValue('otAmount', employeeFullAndFinal?.otAmount);
			setFieldValue('earningsOthers', employeeFullAndFinal?.earningsOthers);
			setFieldValue('deductionsNoticePeriodDays', employeeFullAndFinal?.deductionsNoticePeriodDays);
			setFieldValue('deductionsNoticePeriodAmount', employeeFullAndFinal?.deductionsNoticePeriodAmount);
			setFieldValue('deductionsOthers', employeeFullAndFinal?.deductionsOthers);
		}
	}, [employeeFullAndFinal]);

	useEffect(() => {
		if (employeeProfessionalDetail && !isSubmitting && employeeFullAndFinal == undefined) {
			setFieldValue('fullAndFinalDate', employeeProfessionalDetail?.resignationDate);
		}
	}, [employeeProfessionalDetail]);

	const salaryRate = useMemo(() => {
		let sum = 0;

		if (earnedAmountWithPreparedSalary) {
			earnedAmountWithPreparedSalary.forEach((earning) => {
				sum += earning.rate;
			});
		}

		return sum;
	}, [earnedAmountWithPreparedSalary]);

	useEffect(() => {
		let elLeftDays = 0;
		if (values.elEncashmentDays != '') {
			elLeftDays = values.elEncashmentDays;
		}
		if (earnedAmountWithPreparedSalary && companyCalculations) {
			let elAmount = new BigNumber(salaryRate)
				.dividedBy(new BigNumber(companyCalculations.elCalculation))
				.multipliedBy(new BigNumber(elLeftDays));
			setFieldValue('elEncashmentAmount', Math.round(elAmount.toNumber()));
		}
	}, [values.elEncashmentDays]);

	useEffect(() => {
		let serviceCompensationDays = 0;
		if (values.serviceCompensationDays != '') {
			serviceCompensationDays = values.serviceCompensationDays;
		}
		if (earnedAmountWithPreparedSalary && companyCalculations) {
			let serviceAmount = new BigNumber(salaryRate)
				.dividedBy(new BigNumber(companyCalculations.serviceCalculation))
				.multipliedBy(new BigNumber(serviceCompensationDays));
			setFieldValue('serviceCompensationAmount', Math.round(serviceAmount.toNumber()));
		}
	}, [values.serviceCompensationDays]);

	useEffect(() => {
		let earningsNoticePeriodDays = 0;
		if (values.earningsNoticePeriodDays != '') {
			earningsNoticePeriodDays = values.earningsNoticePeriodDays;
		}
		if (earnedAmountWithPreparedSalary && companyCalculations) {
			let noticeEarningAmount = new BigNumber(salaryRate)
				.dividedBy(new BigNumber(companyCalculations.noticePay))
				.multipliedBy(new BigNumber(earningsNoticePeriodDays));
			setFieldValue('earningsNoticePeriodAmount', Math.round(noticeEarningAmount.toNumber()));
		}
	}, [values.earningsNoticePeriodDays]);

	useEffect(() => {
		let deductionsNoticePeriodDays = 0;
		if (values.deductionsNoticePeriodDays != '') {
			deductionsNoticePeriodDays = values.deductionsNoticePeriodDays;
		}
		if (earnedAmountWithPreparedSalary && companyCalculations) {
			let noticeDeductionAmount = new BigNumber(salaryRate)
				.dividedBy(new BigNumber(companyCalculations.noticePay))
				.multipliedBy(new BigNumber(deductionsNoticePeriodDays));
			setFieldValue('deductionsNoticePeriodAmount', Math.round(noticeDeductionAmount.toNumber()));
		}
	}, [values.deductionsNoticePeriodDays]);

	const calculateElDaysElAmount = () => {
		setFieldValue('elEncashmentDays', parseFloat(elLeftObj.elLeft));
	};

	const calculateOtAmount = () => {
		if (earnedAmountWithPreparedSalary) {
			setFieldValue('otAmount', earnedAmountWithPreparedSalary?.[0]?.salaryPrepared?.netOtAmountMonthly);
			setFieldValue('otMin', earnedAmountWithPreparedSalary?.[0]?.salaryPrepared?.netOtMinutesMonthly);
		}
	};
	const resetOtAmount = () => {
		setFieldValue('otAmount', 0);
		setFieldValue('otMin', 0);
	};

	const calculateBonusAmountPrevYear = () => {
		if (previousYearBonusAmount) {
			setFieldValue('bonusPrevYear', previousYearBonusAmount.bonusAmount);
		}
	};
	const calculateBonusAmountCurrentYear = () => {
		if (currentYearBonusAmount) {
			setFieldValue('bonusCurrentYear', currentYearBonusAmount.bonusAmount);
		}
	};

	const calculateGratuity = () => {
		if (durationWorked.years >= 4 && companyCalculations != undefined) {
			if (durationWorked.years == 4 && durationWorked.months >= 6) {
				let gratuityAmount = 0;
				let salary = 0;
				if (companyCalculations.gratuitySalary == 'gross') {
					salary = salaryRate;
				} else if (companyCalculations.gratuitySalary == 'basic' && earnedAmountWithPreparedSalary) {
					earnedAmountWithPreparedSalary.forEach((earning) => {
						if (earning.earningsHead.name == 'Basic') {
							salary = earning.rate;
						}
					});
				}
				gratuityAmount = new BigNumber(salary)
					.dividedBy(new BigNumber(parseInt(companyCalculations.gratuityCalculation)))
					.multipliedBy(new BigNumber(15))
					.multipliedBy(new BigNumber(5));
				setFieldValue('gratuity', Math.round(gratuityAmount.toNumber()));
			} else if (durationWorked.years > 4) {
				let gratuityAmount = 0;
				let salary = 0;
				if (companyCalculations.gratuitySalary == 'gross') {
					salary = salaryRate;
				} else if (companyCalculations.gratuitySalary == 'basic' && earnedAmountWithPreparedSalary) {
					earnedAmountWithPreparedSalary.forEach((earning) => {
						if (earning.earningsHead.name == 'Basic') {
							salary = earning.rate;
						}
					});
				}
				gratuityAmount = new BigNumber(salary)
					.dividedBy(new BigNumber(parseInt(companyCalculations.gratuityCalculation)))
					.multipliedBy(new BigNumber(15))
					.multipliedBy(new BigNumber(durationWorked.years));
				// Adding the gratuity amount for the months left
				gratuityAmount = gratuityAmount.plus(
					BigNumber(gratuityAmount)
						.dividedBy(new BigNumber(durationWorked.years))
						.dividedBy(new BigNumber(12))
						.multipliedBy(new BigNumber(durationWorked.months))
				);
				setFieldValue('gratuity', Math.round(gratuityAmount.toNumber()));
			}
			// setFieldValue('bonusCurrentYear', gratuityAmount);
		}
	};

	if (isLoadingEmployeePersonalDetail || isLoadingEmployeeProfessionalDetail) {
		return (
			<div className="fixed inset-0 z-50 mx-auto my-auto flex h-fit w-fit items-center rounded bg-indigo-600 p-2 font-medium">
				<FaCircleNotch className="mr-2 animate-spin text-white" />
				Processing...
			</div>
		);
	} else if (earnedAmountWithPreparedSalary && earnedAmountWithPreparedSalary.length == 0) {
		return <div className="font-semibold text-redAccent-600">Please Prepare Salary for this Employee first</div>;
	} else {
		return (
			<div className="flex w-fit flex-col gap-1">
				<section className="flex flex-col rounded-lg border border-slate-500 p-2 text-sm">
					<div className="flex h-6 flex-row">
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">Paycode:</div>
							<div className="w-72 font-medium text-blueAccent-500">
								{employeePersonalDetail?.paycode}
							</div>
						</div>
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">ACN:</div>
							<div className="w-72 font-medium text-blueAccent-500">
								{employeePersonalDetail?.attendanceCardNo}
							</div>
						</div>
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">Date of Joining:</div>
							<div className="w-72 font-medium text-blueAccent-500">
								{employeeProfessionalDetail?.dateOfJoining}
							</div>
						</div>
					</div>
					<div className="flex h-6 flex-row">
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">Name:</div>
							<div className="w-72 font-medium text-blueAccent-500">{employeePersonalDetail?.name}</div>
						</div>
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">Department:</div>
							<div className="w-72 font-medium text-blueAccent-500">
								{employeeProfessionalDetail?.department?.name}
							</div>
						</div>
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">Resignation Date:</div>
							<div className="w-72 font-medium text-blueAccent-500">
								{employeeProfessionalDetail?.resignationDate}
							</div>
						</div>
					</div>
					<div className="flex h-6 flex-row">
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">F/H Name:</div>
							<div className="w-72 font-medium text-blueAccent-500">
								{employeePersonalDetail?.fatherOrHusbandName}
							</div>
						</div>
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">Designation:</div>
							<div className="w-72 font-medium text-blueAccent-500">
								{employeeProfessionalDetail?.designation?.name}
							</div>
						</div>
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">Full & Final Date:</div>
							<div className="w-72 text-sm font-medium text-slate-100">
								<Field
									className="block h-6 w-44 rounded border-2 border-gray-800 border-opacity-25 bg-zinc-50  bg-opacity-50 p-1  outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-700 dark:focus:border-opacity-75"
									type="date"
									maxLength={100}
									name="fullAndFinalDate"
								/>
							</div>
						</div>
					</div>
					<div className="mx-auto flex h-6 flex-row">
						<div className="w-36 font-medium text-slate-400">Working Duration:</div>
						<div className="w-72 font-medium text-yellow-600">
							{durationWorked != null
								? `  ${durationWorked.years} Years, ${durationWorked.months} Months, ${durationWorked.days} Days`
								: ''}
						</div>
					</div>
				</section>
				<section className="flex w-full flex-row justify-between gap-1">
					<div className="w-1/2 rounded-lg border border-slate-500">
						<div className="m-2 rounded-lg bg-emerald-900 bg-opacity-30 p-1 text-base font-bold text-green-600">
							<div className="mx-auto w-fit">Earnings</div>
						</div>
						<div className="mx-auto max-w-md">
							<EarningsTable
								globalCompany={globalCompany}
								fullAndFinalEmployeeId={fullAndFinalEmployeeId}
							/>
						</div>
						<div className="mt-4 flex flex-col gap-4 p-2">
							<div className="flex flex-row gap-2 border-b-[1px] border-slate-500 border-opacity-40 pb-[6px]">
								<div className="flex w-2/3 flex-row justify-between text-sm font-medium text-slate-200">
									<div> {'Over Time'}</div>
									<div className=" flex flex-row gap-2">
										<button
											onClick={resetOtAmount}
											className="rounded-lg bg-redAccent-600 bg-opacity-60 px-2 py-1 text-xs hover:bg-opacity-100"
										>
											Reset
										</button>
										<button
											onClick={calculateOtAmount}
											className="rounded-lg bg-blueAccent-600 bg-opacity-60 px-2 py-1 text-xs hover:bg-opacity-100"
										>
											Calculate
										</button>
									</div>
								</div>
								<div className="flex w-1/3 flex-row-reverse justify-between gap-1 text-sm font-medium text-slate-200">
									<div className="relative w-2/3">
										<label
											htmlFor="otAmount"
											className="absolute -top-4 text-[10px] text-blueAccent-500"
										>
											Amount :
										</label>
										<Field
											className="custom-number-input h-6 w-full rounded border border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
											type="number"
											name="otAmount"
											id="otAmount"
											disabled={true}
										/>
									</div>
									<div className="relative w-1/3">
										<label
											htmlFor="otMin"
											className="absolute -top-4 text-[10px] text-blueAccent-500"
										>
											Hrs :
										</label>
										<div
											className="custom-number-input h-6 w-full rounded border border-gray-800
											border-opacity-25 bg-zinc-200 bg-opacity-50 p-1 outline-none transition
											focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25
											dark:bg-zinc-800 dark:focus:border-opacity-75"
										>
											{values.otMin != '' ? values.otMin / 60 : 0}
										</div>
									</div>
								</div>
							</div>
							<div className="flex flex-row gap-2 border-b-[1px] border-slate-500 border-opacity-40 pb-[6px]">
								<div className="flex w-2/3 flex-row justify-between text-sm font-medium text-slate-200">
									<div> EL Encashment</div>
									<div className="">
										<button
											onClick={calculateElDaysElAmount}
											className="rounded-lg bg-blueAccent-600 bg-opacity-60 px-2 py-1 text-xs hover:bg-opacity-100"
										>
											Calculate
										</button>
									</div>
								</div>
								<div className="flex w-1/3 flex-row-reverse justify-between gap-1 text-sm font-medium text-slate-200">
									<div className="relative w-2/3">
										<label
											htmlFor="elEncashmentAmount"
											className="absolute -top-4 text-[10px] text-blueAccent-500"
										>
											Amount :
										</label>
										<Field
											className="custom-number-input h-6 w-full rounded border border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
											type="number"
											name="elEncashmentAmount"
											id="elEncashmentAmount"
										/>{' '}
									</div>
									<div className="relative w-1/3">
										<label
											htmlFor="elEncashmentDays"
											className="absolute -top-4 text-[10px] text-blueAccent-500"
										>
											Days :
										</label>
										<Field
											className="custom-number-input h-6 w-full rounded border border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
											type="number"
											name="elEncashmentDays"
											id="elEncashmentDays"
										/>
									</div>
								</div>
							</div>
							<div className="flex flex-row gap-2 border-b-[1px] border-slate-500 border-opacity-40 pb-[6px]">
								<div className="flex w-2/3 flex-row justify-between text-sm font-medium text-slate-200">
									<div>
										{employeeProfessionalDetail &&
											`Bonus ${
												new Date(employeeProfessionalDetail?.resignationDate).getFullYear() - 2
											}-${
												new Date(employeeProfessionalDetail?.resignationDate).getFullYear() - 1
											}`}
									</div>
									<div className="">
										<button
											onClick={calculateBonusAmountPrevYear}
											className="rounded-lg bg-blueAccent-600 bg-opacity-60 px-2 py-1 text-xs hover:bg-opacity-100"
										>
											Calculate
										</button>
									</div>
								</div>
								<div className="flex w-1/3 flex-row-reverse justify-between gap-1 text-sm font-medium text-slate-200">
									<div className="relative w-2/3">
										<label
											htmlFor="bonusPrevYear"
											className="absolute -top-4 text-[10px] text-blueAccent-500"
										>
											Amount :
										</label>
										<Field
											className="custom-number-input h-6 w-full rounded border border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
											type="number"
											name="bonusPrevYear"
											id="bonusPrevYear"
										/>{' '}
									</div>
								</div>
							</div>
							<div className="flex flex-row gap-2 border-b-[1px] border-slate-500 border-opacity-40 pb-[6px]">
								<div className="flex w-2/3 flex-row justify-between text-sm font-medium text-slate-200">
									<div>
										{employeeProfessionalDetail &&
											`Bonus ${
												new Date(employeeProfessionalDetail?.resignationDate).getFullYear() - 1
											}-${new Date(employeeProfessionalDetail?.resignationDate).getFullYear()}`}
									</div>
									<div className="">
										<button
											onClick={calculateBonusAmountCurrentYear}
											className="rounded-lg bg-blueAccent-600 bg-opacity-60 px-2 py-1 text-xs hover:bg-opacity-100"
										>
											Calculate
										</button>
									</div>
								</div>
								<div className="flex w-1/3 flex-row-reverse justify-between gap-1 text-sm font-medium text-slate-200">
									<div className="relative w-2/3">
										<label
											htmlFor="bonusCurrentYear"
											className="absolute -top-4 text-[10px] text-blueAccent-500"
										>
											Amount :
										</label>
										<Field
											className="custom-number-input h-6 w-full rounded border border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
											type="number"
											name="bonusCurrentYear"
											id="bonusCurrentYear"
										/>{' '}
									</div>
								</div>
							</div>
							<div className="flex flex-row gap-2 border-b-[1px] border-slate-500 border-opacity-40 pb-[6px]">
								<div className="flex w-2/3 flex-row justify-between text-sm font-medium text-slate-200">
									<div>{'Gratuity (if applicable)'}</div>
									<div className="">
										<button
											onClick={calculateGratuity}
											className="rounded-lg bg-blueAccent-600 bg-opacity-60 px-2 py-1 text-xs hover:bg-opacity-100"
										>
											Calculate
										</button>
									</div>
								</div>
								<div className="flex w-1/3 flex-row-reverse justify-between gap-1 text-sm font-medium text-slate-200">
									<div className="relative w-2/3">
										<label
											htmlFor="gratuity"
											className="absolute -top-4 text-[10px] text-blueAccent-500"
										>
											Amount :
										</label>
										<Field
											className="custom-number-input h-6 w-full rounded border border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
											type="number"
											name="gratuity"
											id="gratuity"
										/>{' '}
									</div>
								</div>
							</div>
							<div className="flex flex-row gap-2 border-b-[1px] border-slate-500 border-opacity-40 pb-[6px]">
								<div className="flex w-2/3 flex-row justify-between text-sm font-medium text-slate-200">
									<div> {'Service Compensation (If Applicable)'}</div>
								</div>
								<div className="flex w-1/3 flex-row-reverse justify-between gap-1 text-sm font-medium text-slate-200">
									<div className="relative w-2/3">
										<label
											htmlFor="serviceCompensationAmount"
											className="absolute -top-4 text-[10px] text-blueAccent-500"
										>
											Amount :
										</label>
										<Field
											className="custom-number-input h-6 w-full rounded border border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
											type="number"
											name="serviceCompensationAmount"
											id="serviceCompensationAmount"
										/>
									</div>
									<div className="relative w-1/3">
										<label
											htmlFor="serviceCompensationDays"
											className="absolute -top-4 text-[10px] text-blueAccent-500"
										>
											Days :
										</label>
										<Field
											className="custom-number-input h-6 w-full rounded border border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
											type="number"
											name="serviceCompensationDays"
											id="serviceCompensationDays"
										/>
									</div>
								</div>
							</div>
							<div className="flex flex-row gap-2 border-b-[1px] border-slate-500 border-opacity-40 pb-[6px]">
								<div className="flex w-2/3 flex-row justify-between text-sm font-medium text-slate-200">
									<div> {'Notice Period'}</div>
								</div>
								<div className="flex w-1/3 flex-row-reverse justify-between gap-1 text-sm font-medium text-slate-200">
									<div className="relative w-2/3">
										<label
											htmlFor="earningsNoticePeriodAmount"
											className="absolute -top-4 text-[10px] text-blueAccent-500"
										>
											Amount :
										</label>
										<Field
											className="custom-number-input h-6 w-full rounded border border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
											type="number"
											name="earningsNoticePeriodAmount"
											id="earningsNoticePeriodAmount"
										/>
									</div>
									<div className="relative w-1/3">
										<label
											htmlFor="earningsNoticePeriodDays"
											className="absolute -top-4 text-[10px] text-blueAccent-500"
										>
											Days :
										</label>
										<Field
											className="custom-number-input h-6 w-full rounded border border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
											type="number"
											name="earningsNoticePeriodDays"
											id="earningsNoticePeriodDays"
										/>
									</div>
								</div>
							</div>
							<div className="flex flex-row gap-2">
								<div className="flex w-2/3 flex-row justify-between text-sm font-medium text-slate-200">
									<div> {'Other Earnings'}</div>
								</div>
								<div className="flex w-1/3 flex-row-reverse justify-between gap-1 text-sm font-medium text-slate-200">
									<div className="relative w-2/3">
										<label
											htmlFor="earningsOthers"
											className="absolute -top-4 text-[10px] text-blueAccent-500"
										>
											Amount :
										</label>
										<Field
											className="custom-number-input h-6 w-full rounded border border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
											type="number"
											name="earningsOthers"
											id="earningsOthers"
										/>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div className="w-1/2 rounded-lg border border-slate-500">
						<div className="m-2 rounded-lg bg-red-900 bg-opacity-30 p-1 text-base font-bold text-red-700">
							<div className="mx-auto w-fit">Deductions</div>
						</div>
						<div className="mx-auto max-w-md">
							<DeductionsTable
								globalCompany={globalCompany}
								fullAndFinalEmployeeId={fullAndFinalEmployeeId}
							/>
						</div>
						<div className="mt-4 flex flex-col gap-4 p-2">
							<div className="flex flex-row gap-2 border-b-[1px] border-slate-500 border-opacity-40 pb-[6px]">
								<div className="flex w-2/3 flex-row justify-between text-sm font-medium text-slate-200">
									<div> {'Notice Period'}</div>
								</div>
								<div className="flex w-1/3 flex-row-reverse justify-between gap-1 text-sm font-medium text-slate-200">
									<div className="relative w-2/3">
										<label
											htmlFor="deductionsNoticePeriodAmount"
											className="absolute -top-4 text-[10px] text-redAccent-500"
										>
											Amount :
										</label>
										<Field
											className="custom-number-input h-6 w-full rounded border border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
											type="number"
											name="deductionsNoticePeriodAmount"
											id="deductionsNoticePeriodAmount"
										/>
									</div>
									<div className="relative w-1/3">
										<label
											htmlFor="deductionsNoticePeriodDays"
											className="absolute -top-4 text-[10px] text-redAccent-500"
										>
											Days :
										</label>
										<Field
											className="custom-number-input h-6 w-full rounded border border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
											type="number"
											name="deductionsNoticePeriodDays"
											id="deductionsNoticePeriodDays"
										/>
									</div>
								</div>
							</div>
							<div className="flex flex-row gap-2">
								<div className="flex w-2/3 flex-row justify-between text-sm font-medium text-slate-200">
									<div> {'Other Deductions'}</div>
								</div>
								<div className="flex w-1/3 flex-row-reverse justify-between gap-1 text-sm font-medium text-slate-200">
									<div className="relative w-2/3">
										<label
											htmlFor="deductionsOthers"
											className="absolute -top-4 text-[10px] text-redAccent-500"
										>
											Amount :
										</label>
										<Field
											className="custom-number-input h-6 w-full rounded border border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
											type="number"
											name="deductionsOthers"
											id="deductionsOthers"
										/>
									</div>
								</div>
							</div>
						</div>
					</div>
				</section>
				<section className="flex flex-row gap-10 text-slate-200">
					<div className="flex h-8 w-1/3 flex-row justify-around rounded-lg border border-slate-500 bg-emerald-900 bg-opacity-30 text-sm font-medium">
						<p className="w-1/2 p-1 px-2"> Total Earnings</p>
						<p className="w-1/2 p-1 px-2 text-right text-green-600">
							{values.elEncashmentAmount +
								values.bonusPrevYear +
								values.bonusCurrentYear +
								values.gratuity +
								values.serviceCompensationAmount +
								values.earningsNoticePeriodAmount +
								values.otAmount +
								values.earningsOthers}
						</p>
					</div>
					<div className="flex h-8 w-1/3 flex-row justify-around rounded-lg border border-slate-500 bg-blueAccent-800 bg-opacity-30 text-sm font-medium">
						<p className="w-1/2 p-1 px-2"> Net Paid Amount</p>
						<p className="w-1/2 p-1 px-2 text-right text-blueAccent-500">
							{values.elEncashmentAmount +
								values.bonusPrevYear +
								values.bonusCurrentYear +
								values.gratuity +
								values.serviceCompensationAmount +
								values.earningsNoticePeriodAmount +
								values.otAmount +
								values.earningsOthers -
								(values.deductionsNoticePeriodAmount + values.deductionsOthers)}
						</p>
					</div>
					<div className="flex h-8 w-1/3 flex-row justify-around rounded-lg border border-slate-500 bg-red-900 bg-opacity-20 text-sm font-medium">
						<p className="w-1/2 p-1 px-2"> Total Deductions</p>
						<p className="w-1/2 p-1 px-2 text-right text-red-600">
							{values.deductionsNoticePeriodAmount + values.deductionsOthers}
						</p>
					</div>
				</section>
				<section className="flex flex-row gap-2">
					<button
						className={classNames(
							isValid ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
							'h-7 w-1/2 rounded bg-teal-500 py-1 px-4 text-sm font-medium dark:bg-teal-700'
						)}
						type="submit"
						disabled={!isValid}
						onClick={handleSubmit}
					>
						Save
					</button>
					<button
						className={classNames(
							isEmployeeFullAndFinalSuccess
								? 'hover:bg-blueAccent-500  dark:hover:bg-blueAccent-500'
								: 'opacity-40',
							'h-7 w-1/2 rounded bg-blueAccent-600 py-1 px-4 text-sm font-medium dark:bg-blueAccent-600'
						)}
						disabled={!isEmployeeFullAndFinalSuccess}
						onClick={generateButtonClicked}
					>
						Generate Report
						{/* {isSubmitting && (
							<FaCircleNotch className="my-auto ml-2 inline animate-spin text-xl text-amber-700 dark:text-amber-600 " />
						)} */}
					</button>
				</section>
			</div>
		);
	}
};

export default FullAndFinal;
