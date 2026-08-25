import React from 'react';
import BigNumber from 'bignumber.js';
import { FaCircleNotch } from 'react-icons/fa6';

const NetSalary = React.memo(({ salary, isUpdating = false, children }) => {
	if (!salary) {
		return (
			<div className="flex flex-col gap-2 rounded-xl border border-zinc-300 bg-zinc-50/60 p-2 dark:border-zinc-700 dark:bg-zinc-900/80 sm:flex-row sm:items-center sm:justify-between">
				<p className="text-xs font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
					Preview net salary
				</p>
				<p className="mt-1 flex items-center gap-2 text-sm font-medium text-yellow-600">
					Waiting for preview
					{isUpdating && <FaCircleNotch className="animate-spin text-xs text-blueAccent-500" />}
				</p>
				{children}
			</div>
		);
	}

	const totalEarned = (salary.earnedAmounts || []).reduce(
		(total, row) => total.plus(row.earnedAmount || 0),
		new BigNumber(0)
	);
	const totalDeductions = [
		'pfDeducted',
		'esiDeducted',
		'vpfDeducted',
		'advanceDeducted',
		'tdsDeducted',
		'labourWelfareFundDeducted',
		'othersDeducted',
	].reduce((total, field) => total.plus(salary[field] || 0), new BigNumber(0));
	const overtimeAmount = new BigNumber(salary.netOtAmountMonthly || 0);
	const incentiveAmount = new BigNumber(salary.incentiveAmount || 0);
	const totalBeforeDeductions = totalEarned.plus(overtimeAmount).plus(incentiveAmount);
	const netSalary =
		salary.netSalary != null
			? new BigNumber(salary.netSalary)
			: totalEarned
					.plus(salary.netOtAmountMonthly || 0)
					.plus(salary.incentiveAmount || 0)
					.minus(totalDeductions);

	return (
		<div className="dark:bg-teal-950/40 rounded-xl border border-teal-600/60 bg-teal-50/10 p-2 dark:border-teal-700">
			<div className="grid grid-cols-2 items-center gap-3 rounded-lg border border-blueAccent-900/50 bg-blueAccent-900/20 p-3 sm:grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)_auto_minmax(0,1fr)_auto_minmax(0,1.2fr)]">
				<div className="min-w-0 text-center sm:text-left">
					<p className="truncate text-lg font-semibold tabular-nums text-teal-500 dark:text-teal-300">
						{totalEarned.toFixed()}
					</p>
					<p className="text-[0.65rem] font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
						Earnings
					</p>
				</div>
				<span className="hidden text-zinc-500 dark:text-zinc-400 sm:block">+</span>
				<div className="min-w-0 text-center">
					<p className="truncate text-lg font-semibold tabular-nums text-teal-500 dark:text-teal-300">
						{overtimeAmount.toFixed()}
					</p>
					<p className="text-[0.65rem] font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
						Overtime
					</p>
				</div>
				<span className="hidden text-zinc-500 dark:text-zinc-400 sm:block">+</span>
				<div className="min-w-0 text-center">
					<p className="truncate text-lg font-semibold tabular-nums text-teal-500 dark:text-teal-300">
						{incentiveAmount.toFixed()}
					</p>
					<p className="text-[0.65rem] font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
						Incentive
					</p>
				</div>
				<span className="hidden text-zinc-500 dark:text-zinc-400 sm:block">=</span>
				<div className="col-span-2 min-w-0 border-t border-blueAccent-900/50 pt-2 text-center sm:col-span-1 sm:border-t-0 sm:border-l sm:pl-3 sm:pt-0 sm:text-right">
					<p className="flex items-center justify-center gap-2 truncate text-lg font-bold tabular-nums text-blueAccent-600 dark:text-blueAccent-300 sm:justify-end">
						{totalBeforeDeductions.toFixed()}
						{isUpdating && <FaCircleNotch className="animate-spin text-sm text-blueAccent-500" />}
					</p>
					<p className="text-[0.65rem] font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
						Total before deductions
					</p>
				</div>
			</div>
			<div className="mt-3 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
				<div>
					<p className="text-xs font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
						Preview net salary
					</p>
					<p className="mt-1 flex items-center gap-2 text-2xl font-bold tabular-nums text-teal-600 dark:text-teal-400">
						{netSalary.toFixed()}
						{isUpdating && <FaCircleNotch className="animate-spin text-sm text-blueAccent-500" />}
					</p>
				</div>
				{children}
			</div>
		</div>
	);
});

export default NetSalary;
