import React, { useMemo, useEffect } from 'react';
// import { useGetAllEmployeePfEsiDetailsQuery } from '../../../../authentication/api/salaryPreparationApiSlice';
import { useGetPfEsiSetupQuery } from '../../../../authentication/api/pfEsiSetupApiSlice';
import { useGetEmployeeAdvancePaymentsQuery } from '../../../../authentication/api/advanceUpdationApiSlice';
import { useSelector } from 'react-redux';
import BigNumber from 'bignumber.js';
import { Field, ErrorMessage, FieldArray } from 'formik';

const Deductions = React.memo(
	({
		values,
		globalCompany,
		updateEmployeeId,
		setFieldValue,
		currentEmployeeSalaryDetails,
		currentEmployeePfEsiDetails,
	}) => {
		const auth = useSelector((state) => state.auth);
		console.log(auth.account.role);
		const {
			data: { company, ...companyPfEsiSetup } = {},
			isLoading,
			isSuccess,
			isError,
			error,
			isFetching,
		} = useGetPfEsiSetupQuery(globalCompany.id, {
			skip: globalCompany === null || globalCompany === '',
		});

		const {
			data: employeeAdvancePayments,
			isLoading: isLoadingEmployeeAdvancePayments,
			isSuccess: isEmployeeAdvancePaymentsSuccess,
			isFetching: isFetchingEmployeeAdvancePayments,
		} = useGetEmployeeAdvancePaymentsQuery(
			{
				company: globalCompany.id,
				employee: updateEmployeeId,
			},
			{
				skip: globalCompany === null || globalCompany === '' || !updateEmployeeId,
			}
		);

		useEffect(() => {
			if (employeeAdvancePayments?.length != 0 && employeeAdvancePayments) {
				const totalEmiSum = employeeAdvancePayments?.reduce((accumulator, item) => {
					const itemDate = new Date(item.date);
					const dateSelectedPlusOneMonth = new Date(Date.UTC(values.year, values.month, 1));
					if (itemDate.getTime() < dateSelectedPlusOneMonth.getTime()) {
						return (
							accumulator +
							Number(
								item.emi <= item.principal - item.repaidAmount
									? item.emi
									: item.principal - item.repaidAmount > 0
									? item.principal - item.repaidAmount
									: 0
							)
						);
					} else {
						return accumulator + 0;
					} // Use 0 as a default value if emi is undefined or falsy
				}, 0);
				setFieldValue('employeeSalaryPrepared.advanceDeducted', totalEmiSum);
			} else {
				setFieldValue('employeeSalaryPrepared.advanceDeducted', 0);
			}
		}, [employeeAdvancePayments, updateEmployeeId]);

		// Calculate VPF
		useEffect(() => {
			let timeoutId;

			if (currentEmployeePfEsiDetails?.[0]?.vpfAmount != null) {
				const vpfDeducted = currentEmployeePfEsiDetails?.[0]?.vpfAmount;
				setFieldValue('employeeSalaryPrepared.vpfDeducted', vpfDeducted);
			} else {
				setFieldValue('employeeSalaryPrepared.vpfDeducted', 0);
			}
			if (currentEmployeePfEsiDetails?.[0]?.tdsAmount != null) {
				const tdsDeducted = currentEmployeePfEsiDetails?.[0]?.tdsAmount;
				setFieldValue('employeeSalaryPrepared.tdsDeducted', tdsDeducted);
			} else {
				setFieldValue('employeeSalaryPrepared.tdsDeducted', 0);
			}
		}, [currentEmployeePfEsiDetails, updateEmployeeId]);

		useEffect(() => {
			let timeoutId;

			const calculatePreparedSalaryBasedOnEarnedAmount = () => {
				const basicEarnedItem = values.earnedAmount.find((item) => item.earningsHead.name == 'Basic');
				const totalEarnedAmount = new BigNumber(
					values?.earnedAmount?.reduce((accumulator, item) => {
						// Convert the earnedAmount property to a number and add it to the accumulator
						return accumulator + Number(item.earnedAmount || 0); // Use 0 as a default value if earnedAmount is undefined or falsy
					}, 0)
				);
				if (currentEmployeePfEsiDetails?.[0]?.pfAllow && values.earnedAmount.length != 0) {
					const pfPercentage = new BigNumber(companyPfEsiSetup.ac1EpfEmployeePercentage);
					if (currentEmployeePfEsiDetails?.[0]?.pfLimitIgnoreEmployee == false) {
						const basicEarned = new BigNumber(basicEarnedItem.earnedAmount);
						const pfLimit = new BigNumber(companyPfEsiSetup.ac1EpfEmployeeLimit);
						const minimumValue = BigNumber.minimum(basicEarned, pfLimit);
						const pfDeducted = Math.round(
							pfPercentage.dividedBy(100).multipliedBy(minimumValue).toNumber()
						);
						setFieldValue('employeeSalaryPrepared.pfDeducted', pfDeducted);
					} else if (currentEmployeePfEsiDetails?.[0]?.pfLimitIgnoreEmployee == true) {
						let pfDeducted = 0;
						const basicEarned = new BigNumber(basicEarnedItem.earnedAmount);
						if (currentEmployeePfEsiDetails?.[0]?.pfLimitIgnoreEmployeeValue == null) {
							pfDeducted = Math.round(pfPercentage.dividedBy(100).multipliedBy(basicEarned).toNumber());
						} else {
							const pfLimit = new BigNumber(currentEmployeePfEsiDetails?.[0]?.pfLimitIgnoreEmployeeValue);
							const minimumValue = BigNumber.minimum(basicEarned, pfLimit);
							pfDeducted = Math.round(pfPercentage.dividedBy(100).multipliedBy(minimumValue).toNumber());
						}
						// isChanged = true;
						setFieldValue('employeeSalaryPrepared.pfDeducted', pfDeducted);
					}
				} else {
					setFieldValue('employeeSalaryPrepared.pfDeducted', 0);
				}
				if (
					currentEmployeePfEsiDetails?.[0]?.esiAllow &&
					values.earnedAmount.length != 0 &&
					companyPfEsiSetup
				) {
					let totalEarnedForEsiDeduction = totalEarnedAmount;
					if (currentEmployeePfEsiDetails?.[0]?.esiOnOt == true || auth.account.role == 'REGULAR') {
						totalEarnedForEsiDeduction = totalEarnedForEsiDeduction.plus(
							values.employeeSalaryPrepared.netOtAmountMonthly
						);
					}
					const esiEmployeePercentage = new BigNumber(companyPfEsiSetup.esiEmployeePercentage);

					const esiEmployeeLimit = new BigNumber(companyPfEsiSetup.esiEmployeeLimit);
					const minimumEsiLimit = BigNumber.minimum(totalEarnedForEsiDeduction, esiEmployeeLimit);
					const esiDeducted = Math.ceil(
						esiEmployeePercentage.dividedBy(100).multipliedBy(minimumEsiLimit).toNumber()
					);
					setFieldValue('employeeSalaryPrepared.esiDeducted', esiDeducted);
				} else {
					setFieldValue('employeeSalaryPrepared.esiDeducted', 0);
				}
				if (
					currentEmployeeSalaryDetails?.labourWellfareFund &&
					companyPfEsiSetup?.enableLabourWelfareFund == true
				) {
					const lwfLimit = new BigNumber(companyPfEsiSetup?.labourWelfareFundLimit);
					const labourWelfareFundDeducted = BigNumber.minimum(
						totalEarnedAmount
							.multipliedBy(new BigNumber(companyPfEsiSetup?.labourWelfareFundPercentage) ?? 0)
							.dividedBy(new BigNumber(100)),
						lwfLimit
					);

					setFieldValue(
						'employeeSalaryPrepared.labourWelfareFundDeducted',
						Math.round(labourWelfareFundDeducted.toNumber())
					);
				} else {
					setFieldValue('employeeSalaryPrepared.labourWelfareFundDeducted', 0);
				}
			};

			clearTimeout(timeoutId);
			timeoutId = setTimeout(() => {
				if (updateEmployeeId) {
					calculatePreparedSalaryBasedOnEarnedAmount();
				}
			}, 50);

			return () => {
				clearTimeout(timeoutId);
			};
		}, [
			values.earnedAmount.map((item) => item.earnedAmount).join(','),
			currentEmployeePfEsiDetails,
			companyPfEsiSetup,
			values.employeeSalaryPrepared.netOtAmountMonthly,
			updateEmployeeId,
		]);
		// if (values?.earnedAmount.length == 0) {
		// 	return <></>;
		// }

		return (
			<table className="w-full border-collapse text-center text-xs">
				<thead className="sticky top-0 z-20 bg-red-500 dark:bg-red-500 dark:bg-opacity-40">
					<tr>
						<th className="border border-slate-400 border-opacity-60 px-4 py-2 font-medium">Deductions</th>
						<th className="border border-slate-400 border-opacity-60 px-4 py-2 font-medium">Amount</th>
					</tr>
				</thead>
				<tbody className="h-fit max-h-20 divide-y divide-black divide-opacity-50 overflow-y-auto border-t border-black border-opacity-50 ">
					<tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
						<td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">PF</td>
						<td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
							{values.employeeSalaryPrepared.pfDeducted}
						</td>
					</tr>
					<tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
						<td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
							ESI
						</td>
						<td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
							{values.employeeSalaryPrepared.esiDeducted}
						</td>
					</tr>
					{companyPfEsiSetup?.enableLabourWelfareFund && currentEmployeeSalaryDetails?.labourWellfareFund && (
						<tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
							<td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
								LWF
							</td>
							<td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
								{values.employeeSalaryPrepared.labourWelfareFundDeducted}
							</td>
						</tr>
					)}
					<tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
						<td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
							VPF
						</td>
						<td className="relative border border-slate-400 border-opacity-60 bg-opacity-50 p-0 font-normal dark:bg-zinc-800">
							<Field
								className="custom-number-input h-8 w-32 bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
								type="number"
								name={`employeeSalaryPrepared.vpfDeducted`}
							/>
						</td>
					</tr>
					<tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
						<td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
							Advance
						</td>
						<td className="relative border border-slate-400 border-opacity-60 bg-opacity-50 p-0 font-normal dark:bg-zinc-800">
							<Field
								className="custom-number-input h-8 w-32 bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
								type="number"
								name={`employeeSalaryPrepared.advanceDeducted`}
							/>
						</td>
					</tr>
					<tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
						<td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
							TDS
						</td>
						<td className="relative border border-slate-400 border-opacity-60 bg-opacity-50 p-0 font-normal dark:bg-zinc-800">
							<Field
								className="custom-number-input h-8 w-32 bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
								type="number"
								name={`employeeSalaryPrepared.tdsDeducted`}
							/>
						</td>
					</tr>
					<tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
						<td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
							Others
						</td>
						<td className="relative border border-slate-400 border-opacity-60 bg-opacity-50 p-0 font-normal dark:bg-zinc-800">
							{/* {values.employeeSalaryPrepared.vpfDeducted} */}
							<Field
								className="custom-number-input h-8 w-32 bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
								type="number"
								name={`employeeSalaryPrepared.othersDeducted`}
							/>
						</td>
					</tr>
				</tbody>
			</table>
		);
	}
);

export default Deductions;
