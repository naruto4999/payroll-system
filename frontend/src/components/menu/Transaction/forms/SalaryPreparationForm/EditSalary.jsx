import React, { useMemo, useEffect, useRef, useState } from 'react';
import { Field, ErrorMessage, Formik } from 'formik';
import { FaChevronDown, FaChevronUp, FaCircleNotch } from 'react-icons/fa6';

import {
	useEmployeeBulkSalaryPreparedMutation,
	useGetSalaryPreparationPreviewQuery,
} from '../../../../authentication/api/salaryPreparationApiSlice';
import Deductions from './Deductions';
import NetSalary from './NetSalary';
import ReactModal from 'react-modal';
import ConfirmationModal from '../../../../UI/ConfirmationModal';
import { ConfirmationModalSchema } from './SalaryPreperationSchema';
import { useDispatch } from 'react-redux';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import { getApiErrorMessage } from '../../../../authentication/api/errorUtils';

ReactModal.setAppElement('#root');

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const formatMinutes = (minutes = 0) => {
	const value = Number(minutes) || 0;
	return `${String(Math.floor(value / 60)).padStart(2, '0')}:${String(value % 60).padStart(2, '0')}`;
};

const formatElapsedSeconds = (milliseconds = 0) => {
	return `${(milliseconds / 1000).toFixed(1)} seconds`;
};

const humanizeCode = (value = '') =>
	value
		.toLowerCase()
		.split('_')
		.map((part) => part.charAt(0).toUpperCase() + part.slice(1))
		.join(' ');

const OvertimeSummary = ({ overtime, isUpdating = false }) => {
	const [showDetails, setShowDetails] = useState(false);

	if (!overtime) return null;
	const policy = overtime.effectivePolicy;
	const totals = overtime.totals || {};

	return (
		<section className="mt-1 rounded-xl border border-zinc-300 bg-white/60 p-2 shadow-sm dark:border-zinc-700 dark:bg-zinc-800/60">
			<div className="mb-2 flex items-center justify-between gap-3">
				<div className="flex items-center gap-1">
					<button
						type="button"
						className="rounded p-1 text-blueAccent-600 transition hover:bg-blueAccent-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-1 focus-visible:outline-blueAccent-600 dark:text-blueAccent-300 dark:hover:bg-blueAccent-900/40"
						onClick={() => setShowDetails((visible) => !visible)}
						aria-expanded={showDetails}
						aria-controls="overtime-details"
						title={showDetails ? 'Hide overtime details' : 'Show overtime details'}
					>
						{showDetails ? <FaChevronUp aria-hidden="true" /> : <FaChevronDown aria-hidden="true" />}
						<span className="sr-only">{showDetails ? 'Hide' : 'Show'} overtime details</span>
					</button>
					<h3 className="text-sm font-semibold uppercase tracking-wide text-blueAccent-600 dark:text-blueAccent-300">
						Overtime
					</h3>
				</div>
			</div>
			<div className="grid grid-cols-2 gap-2 sm:max-w-md">
				<div>
					<p className="text-xs font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
						Net overtime duration
					</p>
					<p
						className="flex items-center gap-2 font-semibold text-green-700 dark:text-green-500"
						title={`${totals.netMinutes ?? 0} minutes`}
					>
						{formatMinutes(totals.netMinutes)}
						{isUpdating && <FaCircleNotch className="animate-spin text-xs text-blueAccent-500" />}
					</p>
				</div>
				<div>
					<p className="text-xs font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
						Overtime amount
					</p>
					<p className="flex items-center gap-2 font-semibold text-green-700 dark:text-green-500">
						{totals.amount ?? '0'}
						{isUpdating && <FaCircleNotch className="animate-spin text-xs text-blueAccent-500" />}
					</p>
				</div>
			</div>
			{showDetails && (
				<div id="overtime-details" className="mt-2 border-t border-zinc-200 pt-2 dark:border-zinc-700">
					<div className="mt-1">
						<div className="mb-2 flex flex-wrap items-start justify-between gap-x-4 gap-y-1 text-xs">
							<div>
								{policy && (
									<>
										<p>
											{policy.name} ({humanizeCode(policy.resolution)})
										</p>
										<p className="text-zinc-500 dark:text-zinc-400">
											Earnings basis: {humanizeCode(policy.earningsBasis)}
										</p>
									</>
								)}
							</div>
							{policy && (
								<p>
									Rounding: {policy.roundingIncrementMinutes} min, round up from{' '}
									{policy.roundUpFromMinutes} min
								</p>
							)}
						</div>
						<div className="mb-2 grid grid-cols-2 gap-2 sm:grid-cols-3">
							{[
								['Raw eligible', totals.rawEligibleMinutes],
								['Rounded gross', totals.roundedGrossMinutes],
								['Late deducted', totals.deductedLateMinutes],
							].map(([label, minutes]) => (
								<div key={label}>
									<p className="text-xs font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
										{label}
									</p>
									<p className="font-semibold" title={`${minutes ?? 0} minutes`}>
										{formatMinutes(minutes)}
									</p>
								</div>
							))}
						</div>
						<div className="overflow-x-auto rounded border border-zinc-300 dark:border-zinc-600">
							<table className="w-full min-w-[760px] border-collapse text-center text-xs">
								<caption className="sr-only">Overtime calculation by day category</caption>
								<thead className="bg-zinc-200 text-zinc-700 dark:bg-zinc-700 dark:text-zinc-100">
									<tr>
										{[
											'Category',
											'Eligible',
											'Raw',
											'Rounded',
											'Late',
											'Net',
											'Multiplier',
											'Rate',
											'Divisor',
											'Amount',
										].map((label) => (
											<th
												scope="col"
												key={label}
												className="border-b border-zinc-300 px-2 py-1.5 font-semibold dark:border-zinc-600"
											>
												{label}
											</th>
										))}
									</tr>
								</thead>
								<tbody className="divide-y divide-zinc-200 dark:divide-zinc-700">
									{(overtime.breakdown || []).map((row) => (
										<tr key={row.dayType} className="hover:bg-zinc-50 dark:hover:bg-zinc-800/70">
											<th
												scope="row"
												className="px-2 py-1.5 font-normal text-zinc-700 dark:text-zinc-200"
											>
												{humanizeCode(row.dayType)}
											</th>
											<td
												className="px-2 py-1.5"
												title={
													row.eligible === false
														? 'Not eligible under the effective policy'
														: ''
												}
											>
												{row.eligible === false ? 'No (policy)' : 'Yes'}
											</td>
											{[
												row.rawEligibleMinutes,
												row.roundedGrossMinutes,
												row.deductedLateMinutes,
												row.netMinutes,
											].map((minutes, index) => (
												<td
													key={index}
													className="px-2 py-1.5"
													title={`${minutes ?? 0} minutes`}
												>
													{formatMinutes(minutes)}
												</td>
											))}
											{[row.multiplier, row.eligibleSalaryRate, row.divisor, row.amount].map(
												(value, index) => (
													<td key={index} className="px-2 py-1.5 tabular-nums">
														{value ?? '0'}
													</td>
												)
											)}
										</tr>
									))}
								</tbody>
							</table>
						</div>
						{overtime.groupDiagnostics?.length > 0 && (
							<details className="mt-1">
								<summary className="cursor-pointer rounded font-medium focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blueAccent-600">
									Rounding group diagnostics
								</summary>
								<ul className="mt-2 space-y-1">
									{overtime.groupDiagnostics.map((row, index) => (
										<li key={`${row.attendanceId}-${row.workDate}-${index}`}>
											{row.workDate}, {humanizeCode(row.dayType)}: {row.rawEligibleMinutes} raw
											min to {row.roundedGrossMinutes} rounded min
										</li>
									))}
								</ul>
							</details>
						)}
					</div>
				</div>
			)}
		</section>
	);
};

const EditSalary = ({
	updateEmployeeId,
	globalCompany,
	values,
	handleChange,
	errors,
	isSubmitting,
	setFieldValue,
	setValues,
	handleReset,
	touched,
	isValid,
	handleSubmit,
	isAddingEmployeeSalaryPrepared,
	employeePersonalDetails,
}) => {
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

	const [showConfirmModal, setShowConfirmModal] = useState(false);
	const [bulkErrors, setBulkErrors] = useState([]);
	// Server defaults populate the form for saving, but only explicit user
	// overrides change the preview request. Hydration must not request it again.
	const [editedDefaultDeductions, setEditedDefaultDeductions] = useState({});
	const onDeductionChange = (field) => {
		setEditedDefaultDeductions((previous) => ({ ...previous, [field]: true }));
	};
	const latestSelectionKeyRef = useRef('');
	latestSelectionKeyRef.current = `${globalCompany?.id}-${updateEmployeeId}-${values.year}-${values.month}`;
	const previewInput = useMemo(
		() => ({
			company: globalCompany?.id,
			employee: updateEmployeeId,
			year: Number(values?.year),
			month: Number(values?.month),
			incentiveAmount: Number(values.employeeSalaryPrepared?.incentiveAmount || 0),
			advanceDeducted:
				!editedDefaultDeductions.advanceDeducted ||
				values.employeeSalaryPrepared?.advanceDeducted === null ||
				values.employeeSalaryPrepared?.advanceDeducted === ''
					? null
					: Number(values.employeeSalaryPrepared.advanceDeducted),
			vpfDeducted:
				!editedDefaultDeductions.vpfDeducted ||
				values.employeeSalaryPrepared?.vpfDeducted === null ||
				values.employeeSalaryPrepared?.vpfDeducted === ''
					? null
					: Number(values.employeeSalaryPrepared.vpfDeducted),
			tdsDeducted:
				!editedDefaultDeductions.tdsDeducted ||
				values.employeeSalaryPrepared?.tdsDeducted === null ||
				values.employeeSalaryPrepared?.tdsDeducted === ''
					? null
					: Number(values.employeeSalaryPrepared.tdsDeducted),
			othersDeducted: Number(values.employeeSalaryPrepared?.othersDeducted || 0),
			arrears: (values.earnedAmount || [])
				.filter((row) => Number(row.arearAmount || 0) > 0)
				.map((row) => ({
					earningsHead: row.earningsHead.id,
					arearAmount: Number(row.arearAmount),
				})),
		}),
		[
			globalCompany?.id,
			updateEmployeeId,
			values.year,
			values.month,
			values.employeeSalaryPrepared?.incentiveAmount,
			values.employeeSalaryPrepared?.advanceDeducted,
			values.employeeSalaryPrepared?.vpfDeducted,
			values.employeeSalaryPrepared?.tdsDeducted,
			values.employeeSalaryPrepared?.othersDeducted,
			editedDefaultDeductions,
			values.earnedAmount.map((row) => `${row.earningsHead.id}:${row.arearAmount}`).join(','),
		]
	);
	const previewInputSignature = JSON.stringify(previewInput);
	// Selection remounts this form, so its first preview is immediate. Only
	// subsequent edits are debounced.
	const [debouncedPreviewInput, setDebouncedPreviewInput] = useState(previewInput);

	useEffect(() => {
		const timeout = setTimeout(() => setDebouncedPreviewInput(previewInput), 250);
		return () => clearTimeout(timeout);
	}, [previewInputSignature]);

	const [
		employeeBulkSalaryPrepared,
		{
			isLoading: isBulkPreparingEmployeeSalaries,
			// isError: errorRegisteringRegular,
			isSuccess: isEmployeeBulkSalaryPrepareddSuccess,
		},
	] = useEmployeeBulkSalaryPreparedMutation();

	const {
		data: previewResponse,
		isLoading: isLoadingSalaryPreview,
		isFetching: isFetchingSalaryPreview,
		isSuccess: isSalaryPreviewSuccess,
		isError: isSalaryPreviewError,
		error: salaryPreviewError,
	} = useGetSalaryPreparationPreviewQuery(debouncedPreviewInput, {
		skip:
			!debouncedPreviewInput?.company ||
			!debouncedPreviewInput?.employee ||
			!Number.isInteger(debouncedPreviewInput?.year) ||
			!Number.isInteger(debouncedPreviewInput?.month) ||
			debouncedPreviewInput?.month < 1 ||
			debouncedPreviewInput?.month > 12,
		refetchOnMountOrArgChange: true,
	});
	// Retain this selection's last result while editing, but never display a
	// response belonging to a different employee, company, or month.
	const periodDate = `${values.year}-${String(values.month).padStart(2, '0')}-01`;
	const salaryPreview =
		previewResponse?.salary?.employee === updateEmployeeId &&
		previewResponse?.salary?.company === globalCompany.id &&
		previewResponse?.salary?.date === periodDate
			? previewResponse
			: undefined;
	const previewIsUpdating =
		previewInputSignature !== JSON.stringify(debouncedPreviewInput) ||
		isLoadingSalaryPreview ||
		isFetchingSalaryPreview;

	useEffect(() => {
		const previewRows = salaryPreview?.salary?.earnedAmounts;
		if (!previewRows || previewIsUpdating) return;
		setValues((current) => {
			const deductions = { ...current.employeeSalaryPrepared };
			let changed = false;
			for (const field of ['advanceDeducted', 'vpfDeducted', 'tdsDeducted']) {
				if (!editedDefaultDeductions[field] && deductions[field] !== salaryPreview.salary[field]) {
					deductions[field] = salaryPreview.salary[field];
					changed = true;
				}
			}
			const rowSignature = (rows) =>
				rows.map((row) => `${row.earningsHead.id}:${row.rate}:${row.earnedAmount}:${row.arearAmount}`).join(',');
			const earningsChanged = rowSignature(current.earnedAmount) !== rowSignature(previewRows);
			if (!changed && !earningsChanged) return current;
			return { ...current, employeeSalaryPrepared: deductions, earnedAmount: previewRows };
		}, false);
	}, [
		salaryPreview?.salary?.earnedAmounts,
		salaryPreview?.salary?.advanceDeducted,
		salaryPreview?.salary?.vpfDeducted,
		salaryPreview?.salary?.tdsDeducted,
		previewIsUpdating,
		editedDefaultDeductions,
		setValues,
	]);

	const bulkPrepareSalaries = async (formikBag) => {
		const requestSelectionKey = `${globalCompany.id}-${updateEmployeeId}-${values.year}-${values.month}`;
		const toSend = {
			company: globalCompany.id,
			month: Number(values.month),
			year: Number(values.year),
		};
		setBulkErrors([]);
		try {
			const startedAt = performance.now();
			const response = await employeeBulkSalaryPrepared(toSend).unwrap();
			const elapsedTime = formatElapsedSeconds(performance.now() - startedAt);
			setShowConfirmModal(false);
			if (latestSelectionKeyRef.current === requestSelectionKey) {
				setEditedDefaultDeductions({});
				setFieldValue('employeeSalaryPrepared.incentiveAmount', 0, false);
				setFieldValue('employeeSalaryPrepared.advanceDeducted', null, false);
				setFieldValue('employeeSalaryPrepared.vpfDeducted', null, false);
				setFieldValue('employeeSalaryPrepared.tdsDeducted', null, false);
				setFieldValue('employeeSalaryPrepared.othersDeducted', 0, false);
				setFieldValue('earnedAmount', [], false);
			}
			dispatch(
				alertActions.createAlert({
					message: `${response.preparedCount} salaries prepared for ${months[Number(values.month) - 1]} ${values.year} in ${elapsedTime}.`,
					type: 'Success',
					duration: 5000,
				})
			);
		} catch (err) {
			setShowConfirmModal(false);
			const rows = Array.isArray(err?.data?.errors) ? err.data.errors : [];
			const normalizedRows = rows.map((row) => {
				const employee = employeePersonalDetails?.find((item) => Number(item.id) === Number(row.employee));
				const detail = row.error || row;
				return {
					employee: employee
						? `${employee.name} (paycode ${employee.paycode || 'n/a'}, card ${employee.attendanceCardNo || 'n/a'}, employee ${row.employee})`
						: `Employee ${row.employee}`,
					message: getApiErrorMessage({ data: detail }),
				};
			});
			setBulkErrors(normalizedRows);
			dispatch(
				alertActions.createAlert({
					message:
						err?.data?.code === 'bulk_preflight_failed'
							? 'Bulk preflight failed. No salaries were written.'
							: getApiErrorMessage(err),
					type: 'Error',
					duration: 5000,
				})
			);
		}
	};
	if (isSalaryPreviewError && salaryPreviewError?.data?.code?.startsWith('missing_')) {
		return (
			<p className="my-2 text-sm text-red-600">
				{getApiErrorMessage(salaryPreviewError, 'Salary preview is unavailable')}
			</p>
		);
	} else {
		return (
			<div className="[container-name:salary-editor] [container-type:inline-size]">
				<div>
					{isSalaryPreviewError && (
						<p className="my-2 text-sm text-red-600">
							{getApiErrorMessage(salaryPreviewError, 'Salary preview is unavailable')}
						</p>
					)}
				</div>
				<section className="grid grid-cols-1 items-start gap-2 [@container_salary-editor_(min-width:560px)]:grid-cols-[minmax(0,1.5fr)_minmax(0,1fr)]">
					<div className="min-w-0 overflow-x-auto rounded-xl border border-zinc-300 bg-white/60 p-2 shadow-sm dark:border-zinc-700 dark:bg-zinc-800/60">
						<div className="mb-2 flex items-center justify-between gap-3">
							<h3 className="text-sm font-semibold uppercase tracking-wide text-blueAccent-600 dark:text-blueAccent-300">
								Earnings
							</h3>
						</div>
						<table className="w-full border-collapse text-right text-xs">
							<thead className="bg-[#5a3914]/80 text-xs uppercase tracking-wide text-white">
								<tr>
									<th className="px-3 py-1 text-left font-semibold">Head</th>
									<th className="px-3 py-1 font-semibold">Rate</th>
									<th className="w-20 px-2 py-1 font-semibold">Arrear</th>
									<th className="w-20 px-2 py-1 font-semibold">Earned</th>
								</tr>
							</thead>
							<tbody className="divide-y divide-zinc-200 dark:divide-zinc-700">
								{values?.earnedAmount?.map((earning, index) => {
									return (
										<tr key={index} className="hover:bg-zinc-50 dark:hover:bg-zinc-800/70">
											<td className="relative px-3 py-1 text-left font-normal text-zinc-600 dark:text-zinc-300">
												{earning.earningsHead.name}
											</td>
											<td className="relative px-3 py-1 font-normal tabular-nums">
												{earning.rate}
											</td>
											<td className="relative p-0 font-normal dark:bg-zinc-800/40">
												<Field
													className="custom-number-input focus:bg-blueAccent-50 h-8 w-20 min-w-0 max-w-full bg-transparent px-2 text-right outline-none transition dark:focus:bg-blueAccent-900/30"
													type="number"
													name={`earnedAmount.${index}.arearAmount`}
												/>
												<ErrorMessage
													name={`earnedAmount.${index}.arearAmount`}
													component="p"
													className="text-red-600"
												/>
											</td>
											<td className="relative px-2 py-1 font-normal tabular-nums text-teal-600 dark:text-teal-400">
												<span className="inline-flex items-center justify-end gap-2">
													{earning.earnedAmount}
													{previewIsUpdating && (
														<FaCircleNotch className="animate-spin text-xs text-blueAccent-500" />
													)}
												</span>
											</td>
										</tr>
									);
								})}
								{/* Calculate total rate */}
								<tr>
									<td className="relative px-3 py-1.5 text-left font-semibold">Total</td>
									<td className="relative px-3 py-1.5 font-semibold tabular-nums">
										{values.earnedAmount?.reduce((total, earning) => total + earning.rate, 0)}
									</td>
									<td className="relative px-2 py-2 font-semibold tabular-nums">
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
									<td className="relative px-2 py-1.5 font-semibold tabular-nums text-teal-600 dark:text-teal-400">
										<span className="inline-flex items-center justify-end gap-2">
											{values.earnedAmount?.reduce(
												(total, earning) => total + earning.earnedAmount,
												0
											)}
											{previewIsUpdating && (
												<FaCircleNotch className="animate-spin text-xs text-blueAccent-500" />
											)}
										</span>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
					<div className="min-w-0 overflow-x-auto rounded-xl border border-zinc-300 bg-white/60 p-2 shadow-sm dark:border-zinc-700 dark:bg-zinc-800/60">
						<div className="mb-2 flex items-center justify-between gap-3">
							<h3 className="text-sm font-semibold uppercase tracking-wide text-blueAccent-600 dark:text-blueAccent-300">
								Deductions
							</h3>
						</div>
						<Deductions
							salary={salaryPreview?.salary}
							isUpdating={previewIsUpdating}
							onDeductionChange={onDeductionChange}
						/>
					</div>
				</section>
				<OvertimeSummary overtime={salaryPreview?.overtime} isUpdating={previewIsUpdating} />
				<section className="mt-1 rounded-xl border border-zinc-300 bg-white/60 p-2 shadow-sm dark:border-zinc-700 dark:bg-zinc-800/60">
					<div className="grid gap-1 sm:grid-cols-2 sm:items-center">
						<div>
							<p className="text-xs font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
								Paid days
							</p>
							<p className="mt-0 font-bold tabular-nums text-teal-600 dark:text-teal-400">
								{salaryPreview?.salary?.paidDays ?? 'Waiting for preview'}
							</p>
						</div>
						<div>
							<label
								htmlFor={`employeeSalaryPrepared.incentiveAmount`}
								className="text-xs font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400"
							>
								Incentive
							</label>
							<Field
								className={classNames(
									errors.employeeSalaryPrepared?.incentiveAmount &&
										touched.employeeSalaryPrepared?.incentiveAmount
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input mt-1 h-7 w-full rounded border border-zinc-300 bg-transparent px-2 outline-none transition focus:border-blueAccent-500 dark:border-zinc-600 dark:bg-zinc-800/60'
								)}
								type="number"
								name={`employeeSalaryPrepared.incentiveAmount`}
							/>
							<div className="mt-0 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name={`employeeSalaryPrepared.incentiveAmount`} />
							</div>
						</div>
					</div>
				</section>
				<section className="mt-1">
					<NetSalary salary={salaryPreview?.salary} isUpdating={previewIsUpdating}>
						<div className="flex flex-col gap-2 sm:flex-row">
							<button
								className={classNames(
									isValid && !isSubmitting && !isBulkPreparingEmployeeSalaries
										? 'hover:bg-teal-600 dark:hover:bg-teal-600'
										: 'opacity-40',
									'h-9 rounded bg-teal-500 px-4 text-sm font-medium text-white dark:bg-teal-700'
								)}
								type="submit"
								disabled={
									!isValid ||
									!isSalaryPreviewSuccess ||
									!salaryPreview ||
									previewIsUpdating ||
									isSalaryPreviewError ||
									isSubmitting ||
									isAddingEmployeeSalaryPrepared ||
									isBulkPreparingEmployeeSalaries
								}
								onClick={handleSubmit}
							>
								Update
								{isSubmitting && (
									<FaCircleNotch className="my-auto ml-2 inline animate-spin text-base" />
								)}
							</button>
							<button
								className={classNames(
									isSubmitting || isAddingEmployeeSalaryPrepared || isBulkPreparingEmployeeSalaries
										? 'opacity-40'
										: 'hover:bg-blueAccent-500 dark:hover:bg-blueAccent-600',
									'h-9 rounded bg-blueAccent-500 px-4 text-sm font-medium text-white dark:bg-blueAccent-700'
								)}
								type="button"
								disabled={
									isSubmitting || isAddingEmployeeSalaryPrepared || isBulkPreparingEmployeeSalaries
								}
								onClick={() => setShowConfirmModal(true)}
							>
								Bulk Prepare Salaries
								{isBulkPreparingEmployeeSalaries && (
									<FaCircleNotch className="my-auto ml-2 inline animate-spin text-base" />
								)}
							</button>
						</div>
					</NetSalary>
				</section>
				{bulkErrors.length > 0 && (
					<section className="mt-4 rounded border border-red-600 p-3 text-sm text-red-700 dark:text-red-500">
						<p className="font-semibold">Bulk preflight failed. No salaries were written.</p>
						<ul className="mt-2 list-disc pl-5">
							{bulkErrors.map((row, index) => (
								<li key={`${row.employee}-${index}`}>
									{row.employee}: {row.message}
								</li>
							))}
						</ul>
					</section>
				)}
				<ReactModal
					className="items-left fixed inset-0 mx-2 my-auto flex h-fit flex-col gap-4 rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-lg"
					isOpen={showConfirmModal}
					onRequestClose={() => {
						if (!isBulkPreparingEmployeeSalaries) setShowConfirmModal(false);
					}}
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
