import { apiSlice } from './apiSlice';

export const timeUpdationApiSlice = apiSlice.injectEndpoints({
	endpoints: (builder) => ({
		getEmployeeAttendanceBetweenDates: builder.query({
			query: (body) => ({
				url: `/api/employee-attendance/${body.company}/${body.employee}/${body.fromDate}/${body.toDate}`,
				method: 'GET',
			}),
			keepUnusedDataFor: 1,
			providesTags: ['EmployeeAttendance'],
		}),
		addEmployeeAttendance: builder.mutation({
			query: (body) => ({
				url: `/api/employee-attendance/${body.company}/${body.employee}`,
				method: 'POST',
				body: body,
			}),
			invalidatesTags: ['EmployeeAttendance'],
		}),
		// updateShift: builder.mutation({
		// 	query: (shift) => ({
		// 		url: `/api/shift/${shift.company}/${shift.id}`,
		// 		method: 'PUT',
		// 		body: shift,
		// 	}),
		// 	invalidatesTags: ['Shifts'],
		// }),
		// deleteShift: builder.mutation({
		// 	query: (shift) => ({
		// 		url: `/api/shift/${shift.company}/${shift.id}`,
		// 		method: 'DELETE',
		// 	}),
		// 	invalidatesTags: ['Shifts'],
		// }),
	}),
});

export const {
	useAddEmployeeAttendanceMutation,
	useGetEmployeeAttendanceBetweenDatesQuery,
} = timeUpdationApiSlice;
