import { apiSlice } from './apiSlice';

export const salaryOvertimeSheetApiSlice = apiSlice.injectEndpoints({
	endpoints: (builder) => ({
		getPreparedSalaries: builder.query({
			query: (body) => ({
				url: `/api/prepared-salaries/${body.company}/${body.year}/${body.month}`,
				method: 'GET',
			}),
			keepUnusedDataFor: 500,
			providesTags: ['PreparedSalaries'],
		}),
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

export const { useGenerateSalaryOvertimeSheetMutation, useGetPreparedSalariesQuery } = salaryOvertimeSheetApiSlice;
