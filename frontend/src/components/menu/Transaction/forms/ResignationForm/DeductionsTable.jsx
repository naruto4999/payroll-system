import React from 'react';
import { useEarnedAmountWithPreparedSalaryQuery } from '../../../../authentication/api/fullAndFinalApiSlice';
import { useGetPfEsiSetupQuery } from '../../../../authentication/api/pfEsiSetupApiSlice';

const DeductionsTable = ({ globalCompany, fullAndFinalEmployeeId }) => {
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
		data: earnedAmountWithPreparedSalary,
		isLoading: isLoadingEarnedAmountWithPreparedSalary,
		isSuccess: isEarnedAmountWithPreparedSalarySuccess,
		isError: isEarnedAmountWithPreparedSalaryError,
	} = useEarnedAmountWithPreparedSalaryQuery({ company: globalCompany.id, employee: fullAndFinalEmployeeId });
	console.log(earnedAmountWithPreparedSalary);
	if (earnedAmountWithPreparedSalary == undefined || earnedAmountWithPreparedSalary.length == 0) {
		return <></>;
	}
	return (
		<table className="w-full border-collapse text-center text-xs">
			<thead className="sticky top-0 z-20 bg-red-500 text-slate-200 dark:bg-red-500 dark:bg-opacity-40">
				<tr>
					<th className="border border-slate-400 border-opacity-60 px-4 py-1.5 font-medium">Deductions</th>
					<th className="border border-slate-400 border-opacity-60 px-4 py-1.5 font-medium">Amount</th>
				</tr>
			</thead>
			<tbody className="h-fit max-h-20 divide-y divide-black divide-opacity-50 overflow-y-auto border-t border-black border-opacity-50 text-slate-200">
				<tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
					<td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 font-normal">PF</td>
					<td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 text-right font-normal text-redAccent-500">
						{earnedAmountWithPreparedSalary?.[0]?.salaryPrepared.pfDeducted}
					</td>
				</tr>
				<tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
					<td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 font-normal">ESI</td>
					<td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 text-right font-normal text-redAccent-500">
						{earnedAmountWithPreparedSalary?.[0]?.salaryPrepared.esiDeducted}
					</td>
				</tr>
				{companyPfEsiSetup?.enableLabourWelfareFund && (
					<tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
						<td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 font-normal">
							LWF
						</td>
						<td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 text-right font-normal text-redAccent-500">
							{earnedAmountWithPreparedSalary?.[0]?.salaryPrepared.labourWelfareFundDeducted}
						</td>
					</tr>
				)}
				<tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
					<td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 font-normal">VPF</td>
					<td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 text-right font-normal text-redAccent-500">
						{/* <Field
							className="custom-number-input h-8 w-32 bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
							type="number"
							name={`employeeSalaryPrepared.vpfDeducted`}
						/> */}
						{earnedAmountWithPreparedSalary?.[0]?.salaryPrepared.vpfDeducted}
					</td>
				</tr>
				<tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
					<td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 font-normal ">
						Advance
					</td>
					<td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 text-right font-normal text-redAccent-500">
						{/* <Field
							className="custom-number-input h-8 w-32 bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
							type="number"
							name={`employeeSalaryPrepared.advanceDeducted`}
						/> */}
						{earnedAmountWithPreparedSalary?.[0]?.salaryPrepared.advanceDeducted}
					</td>
				</tr>
				<tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
					<td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 font-normal">TDS</td>
					<td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 text-right font-normal text-redAccent-500">
						{/* <Field
							className="custom-number-input h-8 w-32 bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
							type="number"
							name={`employeeSalaryPrepared.tdsDeducted`}
						/> */}
						{earnedAmountWithPreparedSalary?.[0]?.salaryPrepared.tdsDeducted}
					</td>
				</tr>
				<tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
					<td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 font-normal">
						Others
					</td>
					<td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 text-right font-normal text-redAccent-500">
						{/* <Field
							className="custom-number-input h-8 w-32 bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
							type="number"
							name={`employeeSalaryPrepared.othersDeducted`}
						/> */}
						{earnedAmountWithPreparedSalary?.[0]?.salaryPrepared.othersDeducted}
					</td>
				</tr>
			</tbody>
		</table>
	);
};

export default DeductionsTable;
