import { apiSlice } from './apiSlice';

const policyMutationTags = (companyId, policyId) => [
	{ type: 'OvertimePolicies', id: `${companyId}-LIST` },
	...(policyId ? [{ type: 'OvertimePolicies', id: `${companyId}-${policyId}` }] : []),
	'SalaryOvertimePreview',
	'EmployeeSalaryDetails',
	'AllEmployeeSalaryDetail',
];

export const overtimePolicyApiSlice = apiSlice.injectEndpoints({
	endpoints: (builder) => ({
		getOvertimePolicies: builder.query({
			query: (companyId) => ({
				url: `/api/overtime-policy/${companyId}`,
				method: 'GET',
			}),
			providesTags: (result, error, companyId) => [
				{ type: 'OvertimePolicies', id: `${companyId}-LIST` },
				...(result || []).map((policy) => ({
					type: 'OvertimePolicies',
					id: `${companyId}-${policy.id}`,
				})),
			],
		}),
		getOvertimePolicy: builder.query({
			query: ({ companyId, policyId }) => ({
				url: `/api/overtime-policy/${companyId}/${policyId}`,
				method: 'GET',
			}),
			providesTags: (result, error, { companyId, policyId }) => [
				{ type: 'OvertimePolicies', id: `${companyId}-${policyId}` },
			],
		}),
		createOvertimePolicy: builder.mutation({
			query: ({ companyId, body }) => ({
				url: `/api/overtime-policy/${companyId}`,
				method: 'POST',
				body,
			}),
			invalidatesTags: (result, error, { companyId }) => policyMutationTags(companyId, result?.id),
		}),
		updateOvertimePolicy: builder.mutation({
			query: ({ companyId, policyId, body }) => ({
				url: `/api/overtime-policy/${companyId}/${policyId}`,
				method: 'PATCH',
				body,
			}),
			invalidatesTags: (result, error, { companyId, policyId }) =>
				policyMutationTags(companyId, policyId),
		}),
		deleteOvertimePolicy: builder.mutation({
			query: ({ companyId, policyId }) => ({
				url: `/api/overtime-policy/${companyId}/${policyId}`,
				method: 'DELETE',
			}),
			invalidatesTags: (result, error, { companyId, policyId }) =>
				policyMutationTags(companyId, policyId),
		}),
	}),
});

export const {
	useGetOvertimePoliciesQuery,
	useGetOvertimePolicyQuery,
	useCreateOvertimePolicyMutation,
	useUpdateOvertimePolicyMutation,
	useDeleteOvertimePolicyMutation,
} = overtimePolicyApiSlice;
