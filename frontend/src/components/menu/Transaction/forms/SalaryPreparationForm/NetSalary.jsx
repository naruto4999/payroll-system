import React, { useEffect, useState } from 'react';
import BigNumber from 'bignumber.js';

const NetSalary = React.memo(({ values, updateEmployeeId }) => {
	const [netPayableSalary, setNetPayableSalary] = useState(0);

	useEffect(() => {
		if (updateEmployeeId) {
			let netSalary = new BigNumber(0);
			const totalEarned = new BigNumber(
				values?.earnedAmount?.reduce((accumulator, item) => {
					return accumulator + Number(item.earnedAmount || 0);
				}, 0)
			);
			// Deductions
			const labourWelfareFundDeducted = new BigNumber(values.employeeSalaryPrepared.labourWelfareFundDeducted);
			const pfDeducted = new BigNumber(values.employeeSalaryPrepared.pfDeducted);
			const esiDeducted = new BigNumber(values.employeeSalaryPrepared.esiDeducted);
			const vpfDeducted = new BigNumber(values.employeeSalaryPrepared.vpfDeducted);
			const advanceDeducted = new BigNumber(values.employeeSalaryPrepared.advanceDeducted);
			const tdsDeducted = new BigNumber(values.employeeSalaryPrepared.tdsDeducted);
			const othersDeducted = new BigNumber(values.employeeSalaryPrepared.othersDeducted);
			const incentiveAmount =
				values.employeeSalaryPrepared.incentiveAmount === ''
					? new BigNumber(0)
					: new BigNumber(values.employeeSalaryPrepared.incentiveAmount);

			netSalary = netSalary
				.plus(totalEarned)
				.minus(pfDeducted)
				.minus(labourWelfareFundDeducted)
				.minus(esiDeducted)
				.minus(vpfDeducted)
				.minus(advanceDeducted)
				.minus(tdsDeducted)
				.minus(othersDeducted)
				.plus(incentiveAmount);
			setNetPayableSalary(netSalary.toNumber());
		}
	}, [
		values.earnedAmount.map((item) => item.earnedAmount).join(','),
		values.employeeSalaryPrepared.incentiveAmount,
		values.employeeSalaryPrepared.labourWelfareFundDeducted,
		values.employeeSalaryPrepared.pfDeducted,
		values.employeeSalaryPrepared.esiDeducted,
		values.employeeSalaryPrepared.advanceDeducted,
		values.employeeSalaryPrepared.tdsDeducted,
		values.employeeSalaryPrepared.othersDeducted,
		values.employeeSalaryPrepared.vpfDeducted,
	]);
	return (
		<div className="mx-auto mt-4 w-fit">
			<h2 className="inline text-xl dark:text-slate-300">Net Salary:</h2>
			<span className="ml-2 text-2xl font-bold dark:text-green-600">{netPayableSalary}</span>
		</div>
	);
});

export default NetSalary;
