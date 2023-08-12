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
		// addPfEsiSetup: builder.mutation({
		// 	query: (body) => ({
		// 		url: `/api/pf-esi-setup-create`,
		// 		method: 'POST',
		// 		body: body,
		// 	}),
		// 	invalidatesTags: ['PfEsiSetup'],
		// }),
		updateEmployeeShifts: builder.mutation({
			query: (body) => ({
				url: `/api/employee-shifts-update/${body.company}/${body.employee}`,
				method: 'PUT',
				body: body,
			}),
			invalidatesTags: ['EmployeeShifts'],
		}),
	}),
});

export const { useGetEmployeeShiftsQuery, useUpdateEmployeeShiftsMutation } =
	employeeShiftsApiSlice;
