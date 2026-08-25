import { Field, Formik, getIn, useFormikContext } from 'formik';
import { FaCircleNotch } from 'react-icons/fa6';
import Button from '../../../../UI/Button';
import Input from '../../../../UI/Input';
import { OvertimePolicySchema } from './OvertimePolicySchema';

const DAY_TYPES = [
	{ value: 'REGULAR', label: 'Regular days' },
	{ value: 'WEEKLY_OFF', label: 'Weekly off' },
	{ value: 'HOLIDAY', label: 'Holiday' },
];

const formatMultiplier = (value) => {
	const numericValue = Number(value);
	return Number.isFinite(numericValue) ? numericValue.toFixed(2) : value;
};

const serverMessage = (value) => {
	if (!value) return '';
	if (typeof value === 'string') return value;
	if (Array.isArray(value)) return value.map(serverMessage).filter(Boolean).join('; ');
	if (typeof value === 'object') return Object.values(value).map(serverMessage).filter(Boolean).join('; ');
	return String(value);
};

const FieldError = ({ name, serverError }) => {
	const { errors } = useFormikContext();
	const formError = getIn(errors, name);

	return (
		<p className="mt-1 min-h-[1rem] text-xs font-semibold text-red-600 dark:text-red-400">
			{serverMessage(formError)}
			{serverMessage(serverError)}
		</p>
	);
};

const initialValuesFor = (policy) => ({
	name: policy?.name || '',
	isActive: policy?.isActive ?? true,
	isDefault: policy?.isDefault ?? false,
	earningsBasis: policy?.earningsBasis || 'ALL_EARNINGS',
	selectedEarningHeadIds: (policy?.selectedEarningHeads || []).map((head) => String(head.id)),
	roundingIncrementMinutes: policy?.roundingIncrementMinutes ?? 30,
	roundUpFromMinutes: policy?.roundUpFromMinutes ?? 16,
	dayRules: DAY_TYPES.map((dayType) => {
		const rule = (policy?.dayRules || []).find((item) => item.dayType === dayType.value);
		return {
			enabled: Boolean(rule),
			dayType: dayType.value,
			multiplier: formatMultiplier(rule?.multiplier || '1'),
			lateDeductionPriority: rule?.lateDeductionPriority ?? '',
		};
	}),
});

const EditOvertimePolicy = ({
	policy,
	companyId,
	defaultPolicy,
	earningsHeads,
	onSave,
	onCancel,
	isSaving,
	serverErrors,
}) => {
	const isSystem = Boolean(policy?.isSystem);

	const submit = async (values) => {
		if (!values.isDefault && policy?.isDefault) return;
		if (policy?.isActive && !values.isActive) {
			if (
				!window.confirm(
					`Deactivate "${values.name}"? It will not be available for new assignments. Existing assignments and historical salaries will not be changed.`
				)
			)
				return;
		}
		if (values.isDefault && !policy?.isDefault) {
			const previous = defaultPolicy?.name || 'the current policy';
			if (!window.confirm(`Make "${values.name}" the company default instead of "${previous}"?`)) return;
		}
		const selectedEarningHeadIds =
			values.earningsBasis === 'SELECTED_HEADS' ? values.selectedEarningHeadIds.map(Number) : [];
		const dayRules = values.dayRules
			.filter((rule) => rule.enabled)
			.map((rule) => ({
				dayType: rule.dayType,
				multiplier: rule.multiplier,
				lateDeductionPriority: Number(rule.lateDeductionPriority),
			}));
		const completeBody = isSystem
			? {
					roundingIncrementMinutes: Number(values.roundingIncrementMinutes),
					roundUpFromMinutes: Number(values.roundUpFromMinutes),
					...(values.isDefault && !policy.isDefault ? { isDefault: true } : {}),
				}
			: {
					name: values.name.trim(),
					isDefault: values.isDefault,
					isActive: values.isActive,
					earningsBasis: values.earningsBasis,
					roundingIncrementMinutes: Number(values.roundingIncrementMinutes),
					roundUpFromMinutes: Number(values.roundUpFromMinutes),
					selectedEarningHeadIds,
					dayRules,
				};

		let body = completeBody;
		if (policy) {
			const policyValues = {
				name: policy.name,
				isDefault: policy.isDefault,
				isActive: policy.isActive,
				earningsBasis: policy.earningsBasis,
				roundingIncrementMinutes: policy.roundingIncrementMinutes,
				roundUpFromMinutes: policy.roundUpFromMinutes,
				selectedEarningHeadIds: (policy.selectedEarningHeads || []).map((head) => head.id),
				dayRules: policy.dayRules || [],
			};
			body = Object.fromEntries(
				Object.entries(completeBody).filter(([key, value]) => {
					if (key === 'selectedEarningHeadIds') {
						return (
							JSON.stringify([...value].sort((a, b) => a - b)) !==
							JSON.stringify([...policyValues[key]].sort((a, b) => a - b))
						);
					}
					if (key === 'dayRules') {
						const normalize = (rules) =>
							[...rules]
								.map(({ dayType, multiplier, lateDeductionPriority }) => ({
									dayType,
									multiplier,
									lateDeductionPriority,
								}))
								.sort((a, b) => a.dayType.localeCompare(b.dayType));
						return JSON.stringify(normalize(value)) !== JSON.stringify(normalize(policyValues[key]));
					}
					return value !== policyValues[key];
				})
			);
		}
		await onSave({ companyId, body });
	};

	return (
		<div className="rounded-xl border border-zinc-300 bg-white/60 p-3 shadow-sm dark:border-zinc-700 dark:bg-zinc-800/70 sm:p-4">
			<div className="mb-3 flex items-start justify-between gap-3">
				<div>
					<p className="text-xs font-bold uppercase tracking-[0.18em] text-teal-700 dark:text-teal-400">
						{isSystem ? 'Protected system policy' : policy ? 'Edit custom policy' : 'New custom policy'}
					</p>
					<h2 className="mt-1 text-2xl font-semibold">{policy?.name || 'Create overtime policy'}</h2>
				</div>
				<Button variant="ghost" size="xs" onClick={onCancel}>
					Close
				</Button>
			</div>

			<Formik
				initialValues={initialValuesFor(policy)}
				validationSchema={OvertimePolicySchema}
				onSubmit={submit}
				enableReinitialize
			>
				{({ values, handleSubmit }) => (
					<form onSubmit={handleSubmit} className="space-y-2">
						<div className="grid gap-2 sm:grid-cols-2">
							<label className="block sm:col-span-2">
								<span className="text-sm font-medium">Policy name</span>
								<Field name="name" as={Input} size="sm" disabled={isSystem} className="mt-0.5" />
								<FieldError name="name" serverError={serverErrors?.name} />
							</label>

							<label className="block">
								<span className="text-sm font-medium">Rounding increment (minutes)</span>
								<Field
									name="roundingIncrementMinutes"
									as={Input}
									size="sm"
									type="number"
									min="1"
									step="1"
									className="mt-0.5"
								/>
								<FieldError
									name="roundingIncrementMinutes"
									serverError={serverErrors?.roundingIncrementMinutes}
								/>
							</label>
							<label className="block">
								<span className="text-sm font-medium">Round up from (minutes)</span>
								<Field
									name="roundUpFromMinutes"
									as={Input}
									size="sm"
									type="number"
									min="1"
									step="1"
									className="mt-0.5"
								/>
								<FieldError name="roundUpFromMinutes" serverError={serverErrors?.roundUpFromMinutes} />
							</label>
						</div>

						{isSystem ? (
							<div className="rounded-lg bg-blueAccent-100/60 p-4 text-sm dark:bg-blueAccent-900/30">
								<p>
									<span className="font-semibold">Code:</span> {policy.code}
								</p>
								<p className="mt-1">
									System definitions, categories, earnings basis, and active state are server-managed.
								</p>
							</div>
						) : (
							<>
								<div className="grid gap-3 sm:grid-cols-3">
									<label className="flex items-center gap-2 rounded-lg border border-zinc-300 p-2 dark:border-zinc-700">
										<Field type="checkbox" name="isActive" className="h-4 w-4 accent-teal-600" />{' '}
										Active
									</label>
									<label className="flex items-center gap-2 rounded-lg border border-zinc-300 p-2 dark:border-zinc-700">
										<Field
											type="checkbox"
											name="isDefault"
											disabled={policy?.isDefault}
											className="h-4 w-4 accent-teal-600"
										/>{' '}
										Company default
									</label>
								</div>
								<FieldError name="isActive" serverError={serverErrors?.isActive} />
								<FieldError name="isDefault" serverError={serverErrors?.isDefault} />

								<fieldset>
									<legend className="text-sm font-semibold">Eligible earnings</legend>
									<div className="mt-1 flex flex-wrap gap-3">
										<label className="flex items-center gap-2">
											<Field type="radio" name="earningsBasis" value="ALL_EARNINGS" /> All
											earnings
										</label>
										<label className="flex items-center gap-2">
											<Field type="radio" name="earningsBasis" value="SELECTED_HEADS" /> Selected
											heads
										</label>
									</div>
									{values.earningsBasis === 'SELECTED_HEADS' && (
										<div className="mt-1 grid gap-2 rounded-lg border border-zinc-300 p-2 dark:border-zinc-700 sm:grid-cols-2">
											{earningsHeads.length === 0 ? (
												<p className="text-sm text-amber-700 dark:text-amber-400">
													No earning heads are available for this company.
												</p>
											) : (
												earningsHeads.map((head) => (
													<label key={head.id} className="flex items-center gap-2 text-sm">
														<Field
															type="checkbox"
															name="selectedEarningHeadIds"
															value={String(head.id)}
														/>
														{head.name}
														{head.mandatoryEarning ? ' (mandatory)' : ''}
													</label>
												))
											)}
										</div>
									)}
									<FieldError
										name="selectedEarningHeadIds"
										serverError={serverErrors?.selectedEarningHeadIds}
									/>
								</fieldset>

								<fieldset>
									<legend className="text-sm font-semibold">Payable categories</legend>
									<p className="mt-1 text-xs text-zinc-600 dark:text-zinc-400">
										Leave every category off to create a no-payable-category policy.
									</p>
									<div className="mt-2 space-y-1.5">
										{values.dayRules.map((rule, index) => {
											const submittedIndex =
												values.dayRules.slice(0, index + 1).filter((item) => item.enabled)
													.length - 1;
											const ruleServerError = rule.enabled
												? serverErrors?.dayRules?.[submittedIndex]
												: null;
											return (
												<div
													key={rule.dayType}
													className="grid gap-2 rounded-lg border border-zinc-300 p-2 dark:border-zinc-700 sm:grid-cols-[1.2fr_1fr_1fr]"
												>
													<label className="flex items-center gap-2 font-medium">
														<Field
															type="checkbox"
															name={`dayRules.${index}.enabled`}
															className="h-4 w-4 accent-teal-600"
														/>
														{DAY_TYPES[index].label}
													</label>
													<label className="text-xs">
														Multiplier (OT Rate)
														<Field
															name={`dayRules.${index}.multiplier`}
															as={Input}
															size="sm"
															inputMode="decimal"
															disabled={!rule.enabled}
															className="mt-0.5"
														/>
														<FieldError
															name={`dayRules.${index}.multiplier`}
															serverError={ruleServerError?.multiplier}
														/>
													</label>
													<label className="text-xs">
														Late priority
														<Field
															name={`dayRules.${index}.lateDeductionPriority`}
															as={Input}
															size="sm"
															type="number"
															min="1"
															step="1"
															disabled={!rule.enabled}
															className="mt-0.5"
														/>
														<FieldError
															name={`dayRules.${index}.lateDeductionPriority`}
															serverError={ruleServerError?.lateDeductionPriority}
														/>
													</label>
												</div>
											);
										})}
									</div>
									<FieldError
										name="dayRules"
										serverError={
											typeof serverErrors?.dayRules === 'string' ? serverErrors.dayRules : null
										}
									/>
								</fieldset>
							</>
						)}

						{isSystem && !policy.isDefault && (
							<label className="flex items-center gap-2">
								<Field type="checkbox" name="isDefault" className="h-4 w-4 accent-teal-600" /> Make
								company default
							</label>
						)}
						{serverErrors && (
							<p className="dark:bg-red-950/40 rounded bg-red-100 p-3 text-sm text-red-700 dark:text-red-300">
								{serverMessage(serverErrors)}
							</p>
						)}

						<div className="flex flex-wrap gap-2 border-t border-zinc-300 pt-3 dark:border-zinc-700">
							<Button type="submit" disabled={isSaving} size="sm">
								{policy ? 'Save changes' : 'Create policy'}
								{isSaving && <FaCircleNotch className="ml-2 inline animate-spin" />}
							</Button>
							<Button variant="secondary" size="sm" onClick={onCancel} disabled={isSaving}>
								Cancel
							</Button>
						</div>
					</form>
				)}
			</Formik>
		</div>
	);
};

export default EditOvertimePolicy;
