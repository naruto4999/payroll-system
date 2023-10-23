import { apiSlice } from './apiSlice';

export const salaryOvertimeSheetApiSlice = apiSlice.injectEndpoints({
	endpoints: (builder) => ({
		// getCompanyStatistics: builder.query({
		// 	query: (globalCompany) => ({
		// 		url: `/api/company-statistics/${globalCompany}`,
		// 		method: 'GET',
		// 	}),
		// 	keepUnusedDataFor: 500,
		// 	providesTags: ['CompanyStatistics'],
		// }),
		generateSalaryOvertimeSheet: builder.mutation({
			query: (body) => ({
				url: `/api/generate-salary-overtime-sheet`,
				method: 'POST',
				body: body,
			}),
		}),
		// updatedWeeklyOffHolidayOff: builder.mutation({
		// 	query: (body) => ({
		// 		url: `/api/weekly-off-holiday-off/${body.company}`,
		// 		method: 'PUT',
		// 		body: body,
		// 	}),
		// 	invalidatesTags: ['WeeklyOffHolidayOff'],
		// }),
	}),
});

export const { useGenerateSalaryOvertimeSheetMutation } = salaryOvertimeSheetApiSlice;