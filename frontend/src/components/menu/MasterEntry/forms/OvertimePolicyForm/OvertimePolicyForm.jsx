import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useOutletContext } from 'react-router-dom';
import { FaCircleNotch, FaPen, FaPlus, FaRegTrashCan } from 'react-icons/fa6';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import { getApiErrorMessage } from '../../../../authentication/api/errorUtils';
import { useGetEarningsHeadsQuery } from '../../../../authentication/api/earningsHeadEntryApiSlice';
import Button from '../../../../UI/Button';
import Modal from '../../../../UI/Modal';
import {
	useCreateOvertimePolicyMutation,
	useDeleteOvertimePolicyMutation,
	useGetOvertimePoliciesQuery,
	useUpdateOvertimePolicyMutation,
} from '../../../../authentication/api/overtimePolicyApiSlice';
import EditOvertimePolicy from './EditOvertimePolicy';

const dayLabel = { REGULAR: 'Regular', WEEKLY_OFF: 'Weekly off', HOLIDAY: 'Holiday' };

const formatMultiplier = (value) => {
	const numericValue = Number(value);
	return Number.isFinite(numericValue) ? numericValue.toFixed(2) : value;
};

const categorySummary = (policy) =>
	policy.dayRules?.length
		? [...policy.dayRules]
				.sort((a, b) => a.lateDeductionPriority - b.lateDeductionPriority)
				.map((rule) => `${dayLabel[rule.dayType] || rule.dayType} x${formatMultiplier(rule.multiplier)}`)
				.join(', ')
		: 'No payable categories';

const policyRank = (policy) => {
	if (policy.isDefault) return 0;
	if (policy.isActive && policy.isSystem) return 1;
	if (policy.isActive) return 2;
	return 3;
};

const OvertimePolicyForm = () => {
	const dispatch = useDispatch();
	const globalCompany = useSelector((state) => state.globalCompany);
	const [, setShowLoadingBar] = useOutletContext();
	const companyId = globalCompany?.id;
	const [editor, setEditor] = useState(null);
	const [serverErrors, setServerErrors] = useState(null);
	const [pendingPolicyId, setPendingPolicyId] = useState(null);
	const [actionError, setActionError] = useState('');

	const {
		currentData: policies = [],
		isLoading,
		isFetching,
		isError,
		error,
		refetch,
	} = useGetOvertimePoliciesQuery(companyId, { skip: !companyId });
	const { currentData: earningsHeads = [], isFetching: isFetchingHeads } = useGetEarningsHeadsQuery(globalCompany, {
		skip: !companyId,
	});
	const [createPolicy, { isLoading: isCreating }] = useCreateOvertimePolicyMutation();
	const [updatePolicy, { isLoading: isUpdating }] = useUpdateOvertimePolicyMutation();
	const [deletePolicy, { isLoading: isDeleting }] = useDeleteOvertimePolicyMutation();

	useEffect(() => {
		setEditor(null);
		setServerErrors(null);
		setActionError('');
		setPendingPolicyId(null);
	}, [companyId]);

	useEffect(() => {
		setShowLoadingBar(isLoading || isFetching || isFetchingHeads || isCreating || isUpdating || isDeleting);
	}, [isLoading, isFetching, isFetchingHeads, isCreating, isUpdating, isDeleting, setShowLoadingBar]);

	const sortedPolicies = [...policies].sort(
		(a, b) => policyRank(a) - policyRank(b) || a.name.localeCompare(b.name) || a.id - b.id
	);
	const defaultPolicy = policies.find((policy) => policy.isDefault);
	const mutationPending = isCreating || isUpdating || isDeleting;

	const notify = (message) => dispatch(alertActions.createAlert({ message, type: 'Success', duration: 3000 }));

	const savePolicy = async ({ companyId: editorCompanyId, body }) => {
		if (!companyId || editorCompanyId !== companyId) {
			setEditor(null);
			setServerErrors({ detail: 'The selected company changed. Reopen the policy before saving.' });
			return;
		}
		try {
			if (editor.policy) {
				await updatePolicy({ companyId, policyId: editor.policy.id, body }).unwrap();
				notify('Overtime policy updated');
			} else {
				await createPolicy({ companyId, body }).unwrap();
				notify('Overtime policy created');
			}
			setEditor(null);
			setServerErrors(null);
		} catch (requestError) {
			if (requestError.status === 404) setEditor(null);
			setServerErrors(requestError.data || { detail: getApiErrorMessage(requestError) });
			if (requestError.status === 400 || requestError.status === 404) refetch();
		}
	};

	const runAction = async (policy, body, successMessage) => {
		setPendingPolicyId(policy.id);
		setActionError('');
		try {
			await updatePolicy({ companyId, policyId: policy.id, body }).unwrap();
			notify(successMessage);
		} catch (requestError) {
			setActionError(getApiErrorMessage(requestError));
			if (requestError.status === 400 || requestError.status === 404) refetch();
		} finally {
			setPendingPolicyId(null);
		}
	};

	const makeDefault = (policy) => {
		if (!policy.isActive || policy.isDefault || mutationPending) return;
		if (
			window.confirm(
				`Make "${policy.name}" the company default instead of "${defaultPolicy?.name || 'the current default'}"?`
			)
		) {
			runAction(policy, { isDefault: true }, `${policy.name} is now the company default`);
		}
	};

	const toggleActive = (policy) => {
		if (policy.isSystem || policy.isDefault || mutationPending) return;
		if (policy.isActive) {
			const confirmed = window.confirm(
				`Deactivate "${policy.name}"? It will not be available for new employee assignments. Existing assignments and historical salaries will not be changed.`
			);
			if (!confirmed) return;
		}
		runAction(
			policy,
			{ isActive: !policy.isActive },
			`${policy.name} ${policy.isActive ? 'deactivated' : 'activated'}`
		);
	};

	const removePolicy = async (policy) => {
		if (policy.isSystem || policy.isDefault || mutationPending) return;
		if (
			!window.confirm(
				`Permanently delete "${policy.name}"? Deactivation is safer for policies with historical use.`
			)
		)
			return;
		setPendingPolicyId(policy.id);
		setActionError('');
		try {
			await deletePolicy({ companyId, policyId: policy.id }).unwrap();
			notify('Overtime policy deleted');
		} catch (requestError) {
			setActionError(getApiErrorMessage(requestError));
			if (requestError.status === 400 || requestError.status === 404) refetch();
		} finally {
			setPendingPolicyId(null);
		}
	};

	if (!companyId) {
		return (
			<section className="flex flex-col items-center">
				<h4 className="text-x mt-10 font-bold text-redAccent-500 dark:text-redAccent-600">
					Please Select a Company First
				</h4>
			</section>
		);
	}

	return (
		<section className="mx-4 mt-3 pb-10 sm:mx-6">
			<header className="mb-5 flex flex-wrap items-end justify-between gap-4 border-b border-zinc-300 pb-4 dark:border-zinc-700">
				<div>
					<p className="text-xs font-bold uppercase tracking-[0.2em] text-teal-700 dark:text-teal-400">
						Setup Entry
					</p>
					<h1 className="mt-1 text-3xl font-semibold">Overtime Policies</h1>
					<p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
						Company scope:{' '}
						<span className="font-semibold text-zinc-900 dark:text-zinc-100">{globalCompany.name}</span>
					</p>
				</div>
				<Button
					size="sm"
					disabled={mutationPending}
					onClick={() => {
						setEditor({ companyId, policy: null });
						setServerErrors(null);
					}}
				>
					<FaPlus /> New policy
				</Button>
			</header>

			{actionError && (
				<div className="dark:bg-red-950/40 mb-4 rounded border border-red-300 bg-red-50 p-3 text-sm text-red-700 dark:border-red-900 dark:text-red-300">
					{actionError}
				</div>
			)}

			{editor && editor.companyId === companyId && (
				<Modal
					isOpen
					onClose={() => {
						if (isCreating || isUpdating) return;
						setEditor(null);
						setServerErrors(null);
					}}
					closeOnOverlayClick={!isCreating && !isUpdating}
				>
					<EditOvertimePolicy
						policy={editor.policy}
						companyId={editor.companyId}
						defaultPolicy={defaultPolicy}
						earningsHeads={earningsHeads}
						onSave={savePolicy}
						onCancel={() => {
							setEditor(null);
							setServerErrors(null);
						}}
						isSaving={isCreating || isUpdating}
						serverErrors={serverErrors}
					/>
				</Modal>
			)}

			{isLoading ? (
				<div className="flex items-center justify-center gap-2 py-16 text-zinc-600 dark:text-zinc-300">
					<FaCircleNotch className="animate-spin" /> Loading policies...
				</div>
			) : isError ? (
				<div className="dark:bg-red-950/40 rounded border border-red-300 bg-red-50 p-5 dark:border-red-900">
					<p className="font-semibold text-red-700 dark:text-red-300">
						{error?.status === 403
							? 'Overtime policy management is available only to OWNER accounts.'
							: getApiErrorMessage(error, 'Unable to load overtime policies.')}
					</p>
					<Button
						variant="secondary"
						size="xs"
						onClick={refetch}
						className="mt-3 bg-zinc-700 text-white hover:bg-zinc-800 dark:bg-zinc-700 dark:hover:bg-zinc-600"
					>
						Try again
					</Button>
				</div>
			) : sortedPolicies.length === 0 ? (
				<div className="rounded-xl border border-dashed border-zinc-400 px-5 py-12 text-center dark:border-zinc-600">
					<p className="text-lg font-medium">No overtime policies found</p>
					<p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
						Create a custom policy for this company.
					</p>
				</div>
			) : (
				<div className="grid gap-4 lg:grid-cols-2 2xl:grid-cols-3">
					{sortedPolicies.map((policy) => {
						const rowPending = pendingPolicyId === policy.id;
						return (
							<article
								key={policy.id}
								className={`rounded-xl border p-4 shadow-sm ${policy.isDefault ? 'dark:bg-teal-950/20 border-teal-500 bg-teal-50/10' : 'border-zinc-300 bg-white/60 dark:border-zinc-700 dark:bg-zinc-800/60'}`}
							>
								<div className="flex items-start justify-between gap-3">
									<div>
										<h2 className="text-lg font-semibold">{policy.name}</h2>
										<p className="mt-1 break-all text-xs text-zinc-500">{policy.code}</p>
									</div>
									{rowPending && <FaCircleNotch className="mt-1 animate-spin text-teal-600" />}
								</div>
								<div className="mt-3 flex flex-wrap gap-2 text-xs font-semibold">
									<span className="dark:bg-blue-950 rounded-full bg-blue-100 px-2 py-1 text-blue-800 dark:text-blue-300">
										{policy.isSystem ? 'System' : 'Custom'}
									</span>
									{policy.isDefault && (
										<span className="dark:bg-teal-950 rounded-full bg-teal-100 px-2 py-1 text-teal-800 dark:text-teal-300">
											Default
										</span>
									)}
									<span
										className={`rounded-full px-2 py-1 ${policy.isActive ? 'dark:bg-emerald-950 bg-emerald-100 text-emerald-800 dark:text-emerald-300' : 'bg-zinc-200 text-zinc-700 dark:bg-zinc-700 dark:text-zinc-300'}`}
									>
										{policy.isActive ? 'Active' : 'Inactive'}
									</span>
								</div>
								<dl className="mt-4 space-y-2 text-sm">
									<div>
										<dt className="font-medium text-zinc-500 dark:text-zinc-400">Earnings basis</dt>
										<dd>
											{policy.earningsBasis === 'SELECTED_HEADS'
												? `Selected heads (${policy.selectedEarningHeads?.length || 0})`
												: 'All earnings'}
										</dd>
									</div>
									<div>
										<dt className="font-medium text-zinc-500 dark:text-zinc-400">Categories</dt>
										<dd>{categorySummary(policy)}</dd>
									</div>
									<div>
										<dt className="font-medium text-zinc-500 dark:text-zinc-400">Rounding</dt>
										<dd>
											{policy.roundingIncrementMinutes} minute increment, up from{' '}
											{policy.roundUpFromMinutes}
										</dd>
									</div>
								</dl>
								<div className="mt-4 flex flex-wrap gap-2 border-t border-zinc-300 pt-3 text-sm dark:border-zinc-700">
									<Button
										variant="accent"
										size="xs"
										disabled={mutationPending}
										onClick={() => {
											setEditor({ companyId, policy });
											setServerErrors(null);
										}}
									>
										<FaPen /> {policy.isSystem ? 'Rounding' : 'Edit'}
									</Button>
									{!policy.isDefault && policy.isActive && (
										<Button
											variant="success"
											size="xs"
											disabled={mutationPending}
											onClick={() => makeDefault(policy)}
										>
											Make default
										</Button>
									)}
									{!policy.isSystem && !policy.isDefault && (
										<Button
											variant="secondary"
											size="xs"
											disabled={mutationPending}
											onClick={() => toggleActive(policy)}
											className="bg-zinc-600 text-white hover:bg-zinc-700 dark:bg-zinc-600 dark:hover:bg-zinc-700"
										>
											{policy.isActive ? 'Deactivate' : 'Activate'}
										</Button>
									)}
									{!policy.isSystem && !policy.isDefault && (
										<Button
											variant="danger"
											size="xs"
											disabled={mutationPending}
											onClick={() => removePolicy(policy)}
										>
											<FaRegTrashCan /> Delete
										</Button>
									)}
								</div>
							</article>
						);
					})}
				</div>
			)}
		</section>
	);
};

export default OvertimePolicyForm;
