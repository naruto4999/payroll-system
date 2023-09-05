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
		getCurrentMonthAllEmployeeAttendance: builder.query({
			query: (body) => ({
				url: `/api/all-employee-attendance/${body.company}/${body.year}/${body.month}`,
				method: 'GET',
			}),
			keepUnusedDataFor: 1,
			providesTags: ['EmployeeAttendance'],
		}),
		getCurrentMonthAllEmployeeShifts: builder.query({
			query: (body) => ({
				url: `/api/all-employee-monthly-shifts/${body.company}/${body.year}/${body.month}`,
				method: 'GET',
			}),
			keepUnusedDataFor: 1,
			providesTags: ['EmployeeMonthlyShifts'],
		}),
		getAllEmployeeProfessionalDetail: builder.query({
			query: (body) => ({
				url: `/api/all-employee-professional-detail/${body.company}`,
				method: 'GET',
			}),
			keepUnusedDataFor: 1,
			providesTags: ['AllEmployeeProfessionalDetail'],
		}),
		getAllEmployeeSalaryDetail: builder.query({
			query: (body) => ({
				url: `/api/all-employee-salary-detail/${body.company}`,
				method: 'GET',
			}),
			keepUnusedDataFor: 1,
			providesTags: ['AllEmployeeSalaryDetail'],
		}),
		addEmployeeAttendance: builder.mutation({
			query: (body) => ({
				url: `/api/employee-attendance/${body.company}/${body.employee}`,
				method: 'POST',
				body: body,
			}),
			invalidatesTags: ['EmployeeAttendance'],
		}),
		updateEmployeeAttendance: builder.mutation({
			query: (body) => ({
				url: `/api/employee-attendance-update/${body.company}/${body.employee}`,
				method: 'PUT',
				body: body,
			}),
			invalidatesTags: ['EmployeeAttendance'],
		}),
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
	useUpdateEmployeeAttendanceMutation,
	useGetCurrentMonthAllEmployeeAttendanceQuery,
	useGetCurrentMonthAllEmployeeShiftsQuery,
	useGetAllEmployeeProfessionalDetailQuery,
	useGetAllEmployeeSalaryDetailQuery,
} = timeUpdationApiSlice;
