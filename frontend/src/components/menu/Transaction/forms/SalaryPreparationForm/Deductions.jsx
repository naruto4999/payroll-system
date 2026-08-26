import React from 'react';
import { ErrorMessage, Field } from 'formik';
import { FaCircleInfo, FaCircleNotch } from 'react-icons/fa6';

const waitingForPreview = 'Waiting for preview';

const Deductions = React.memo(({ salary, isUpdating = false }) => {
	const serverDeductions = [
		['PF', 'pfDeducted'],
		['ESI', 'esiDeducted'],
		['LWF', 'labourWelfareFundDeducted'],
	];
	const editableDeductions = [
		['VPF', 'vpfDeducted'],
		['TDS', 'tdsDeducted'],
		['Advance', 'advanceDeducted'],
		['Others', 'othersDeducted'],
	];
	const deductionTotal = salary
		? [...serverDeductions, ...editableDeductions].reduce(
				(total, [, field]) => total + Number(salary[field] || 0),
				0
			)
		: null;

	return (
		<table className="w-full border-collapse text-left text-xs">
			<thead className="bg-[#76252d]/80 text-xs uppercase tracking-wide text-white">
				<tr>
					<th className="px-3 py-1 font-semibold">Head</th>
					<th className="px-3 py-1 text-right font-semibold">Amount</th>
				</tr>
			</thead>
			<tbody className="divide-y divide-zinc-200 dark:divide-zinc-700">
				{serverDeductions.map(([label, field]) => (
					<tr key={field} className="hover:bg-zinc-50 dark:hover:bg-zinc-800/70">
						<td className="px-3 py-1.5 font-normal text-zinc-600 dark:text-zinc-300">{label}</td>
						<td className="px-3 py-1.5 text-right font-normal tabular-nums">
							<span className="inline-flex items-center justify-end gap-2">
								{salary ? salary[field] : waitingForPreview}
								{isUpdating && salary && (
									<FaCircleNotch className="animate-spin text-xs text-blueAccent-500" />
								)}
							</span>
						</td>
					</tr>
				))}
				{editableDeductions.map(([label, field]) => (
					<tr key={field} className="hover:bg-zinc-50 dark:hover:bg-zinc-800/70">
						<td className="px-3 py-1.5 font-normal text-zinc-600 dark:text-zinc-300">
							<span className="inline-flex items-center gap-1.5">
								{label}
								{field === 'advanceDeducted' && (
									<button
										type="button"
										className="text-zinc-400 transition hover:text-blueAccent-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-1 focus-visible:outline-blueAccent-600 dark:text-zinc-500 dark:hover:text-blueAccent-300"
										aria-label="Why is an advance deduction shown?"
										title="This amount is based on the employee's active advance repayment schedule. If this month's salary was already prepared, its existing repayment is excluded while recalculating and replaced when saved, not charged twice."
									>
										<FaCircleInfo aria-hidden="true" />
									</button>
								)}
							</span>
						</td>
						<td className="p-0 text-right font-normal dark:bg-zinc-800/40">
							<Field name={`employeeSalaryPrepared.${field}`}>
								{({ field: formikField }) => (
									<input
										{...formikField}
										className="custom-number-input h-8 w-full rounded-none border-0 bg-transparent px-3 text-right outline-none transition focus:bg-blueAccent-50 dark:focus:bg-blueAccent-900/30"
										type="number"
										value={formikField.value ?? ''}
									/>
								)}
							</Field>
							<ErrorMessage
								name={`employeeSalaryPrepared.${field}`}
								component="p"
								className="text-red-600"
							/>
						</td>
					</tr>
				))}
				<tr className="bg-zinc-50 dark:bg-zinc-800/50">
					<td className="px-3 py-2 font-semibold">Preview total</td>
					<td className="px-3 py-2 text-right font-semibold tabular-nums text-blueAccent-600 dark:text-blueAccent-300">
						<span className="inline-flex items-center justify-end gap-2">
							{deductionTotal ?? waitingForPreview}
							{isUpdating && deductionTotal !== null && (
								<FaCircleNotch className="animate-spin text-xs text-blueAccent-500" />
							)}
						</span>
					</td>
				</tr>
			</tbody>
		</table>
	);
});

export default Deductions;
