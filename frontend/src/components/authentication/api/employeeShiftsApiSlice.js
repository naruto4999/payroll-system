import { apiSlice } from './apiSlice';

export const employeeShiftsApiSlice = apiSlice.injectEndpoints({
	endpoints: (builder) => ({
		getEmployeeShifts: builder.query({
			query: (params) => ({
				url: `/api/employee-shifts/${params.company}/${params.employee}/${params.year}`,
				method: 'GET',
			}),
			keepUnusedDataFor: 600,
			providesTags: ['EmployeeShifts'],
		}),
		addEmployeeShifts: builder.mutation({
			query: (body) => ({
				url: `/api/employee-shifts`,
				method: 'POST',
				body: body,
			}),
			// invalidatesTags: [''],
		}),
		updateEmployeeShifts: builder.mutation({
			query: (body) => ({
				url: `/api/employee-shifts-update/${body.company}/${body.employee}`,
				method: 'PUT',
				body: body,
			}),
			invalidatesTags: ['EmployeeShifts'],
		}),
		updatePermanentEmployeeShift: builder.mutation({
			query: (body) => ({
				url: `/api/employee-shift-permanent-update/${body.company}/${body.employee}`,
				method: 'PUT',
				body: body,
			}),
			invalidatesTags: ['EmployeeShifts'],
		}),
	}),
});

export const {
	useGetEmployeeShiftsQuery,
	useUpdateEmployeeShiftsMutation,
	useAddEmployeeShiftsMutation,
	useUpdatePermanentEmployeeShiftMutation,
} = employeeShiftsApiSlice;
