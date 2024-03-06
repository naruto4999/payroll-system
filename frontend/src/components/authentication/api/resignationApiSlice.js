import { apiSlice } from './apiSlice';

export const resignationApiSlice = apiSlice.injectEndpoints({
	endpoints: (builder) => ({
		// getWeeklyOffHolidayOff: builder.query({
		// 	query: (globalCompany) => ({
		// 		url: `/api/weekly-off-holiday-off/${globalCompany}`,
		// 		method: 'GET',
		// 	}),
		// 	keepUnusedDataFor: 500,
		// 	providesTags: ['WeeklyOffHolidayOff'],
		// }),
		// addWeeklyOffHolidayOff: builder.mutation({
		// 	query: (body) => ({
		// 		url: `/api/weekly-off-holiday-off-create/${body.company}`,
		// 		method: 'POST',
		// 		body: body,
		// 	}),
		// 	invalidatesTags: ['WeeklyOffHolidayOff'],
		// }),
		updateResignation: builder.mutation({
			query: (body) => ({
				url: `/api/resignation/${body.company}/${body.employee}`,
				method: 'PATCH',
				body: body,
			}),
			invalidatesTags: [
				'EmployeePersonalDetails',
				'EmployeeProfessionalDetails',
				'AllEmployeeMonthlyAttendanceDetails',
				'EarnedAmountPreparedSalary',
			],
		}),
		unresign: builder.mutation({
			query: (body) => ({
				url: `/api/unresign/${body.company}/${body.employee}`,
				method: 'PATCH',
				body: body,
			}),
			invalidatesTags: ['EmployeePersonalDetails', 'EmployeeProfessionalDetails'],
		}),
		getSingleEmployeeProfessionalDetailPrefetch: builder.query({
			query: (employee) => ({
				url: `/api/get-employee-professional-detail/${employee.company}/${employee.id}`,
				method: 'GET',
			}),
			keepUnusedDataFor: 600,
			providesTags: (result, error, id) => [{ type: 'EmployeeProfessionalDetails', id: id.id }],
		}),
	}),
});

export const {
	useUpdateResignationMutation,
	useUnresignMutation,
	useGetSingleEmployeeProfessionalDetailPrefetchQuery,
} = resignationApiSlice;
