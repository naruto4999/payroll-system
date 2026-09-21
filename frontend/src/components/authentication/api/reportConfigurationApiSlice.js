import { apiSlice } from './apiSlice';

export const reportConfigurationApiSlice = apiSlice.injectEndpoints({
	endpoints: (builder) => ({
		getReportConfigurations: builder.query({
			query: (companyId) => `/api/company-report-configuration/${companyId}`,
			providesTags: (result, error, companyId) => [{ type: 'ReportConfigurations', id: companyId }],
		}),
		createReportConfiguration: builder.mutation({
			query: ({ companyId, body }) => ({
				url: `/api/company-report-configuration/${companyId}`,
				method: 'POST',
				body,
			}),
			invalidatesTags: (result, error, { companyId }) => [{ type: 'ReportConfigurations', id: companyId }],
		}),
		updateReportConfiguration: builder.mutation({
			query: ({ companyId, configurationId, body }) => ({
				url: `/api/company-report-configuration/${companyId}/${configurationId}`,
				method: 'PATCH',
				body,
			}),
			invalidatesTags: (result, error, { companyId }) => [{ type: 'ReportConfigurations', id: companyId }],
		}),
	}),
});

export const {
	useGetReportConfigurationsQuery,
	useCreateReportConfigurationMutation,
	useUpdateReportConfigurationMutation,
} = reportConfigurationApiSlice;
