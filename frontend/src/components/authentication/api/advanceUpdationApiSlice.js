import { apiSlice } from './apiSlice';

export const advanceUpdationApiSlice = apiSlice.injectEndpoints({
	endpoints: (builder) => ({
		getEmployeeAdvancePayments: builder.query({
			query: (body) => ({
				url: `/api/employee-advance-payment/${body.company}/${body.employee}`,
				method: 'GET',
			}),
			keepUnusedDataFor: 500,
			providesTags: ['AdvancePayments'],
		}),

		addEmployeeAdvancePayments: builder.mutation({
			query: (body) => ({
				url: `/api/employee-advance-payment/${body.company}/${body.employee}`,
				method: 'POST',
				body: body,
			}),
			invalidatesTags: ['AdvancePayments'],
		}),
		updateEmployeeAdvancePayments: builder.mutation({
			query: (body) => ({
				url: `/api/employee-advance-payment-update/${body.company}/${body.employee}`,
				method: 'PUT',
				body: body,
			}),
			invalidatesTags: ['AdvancePayments'],
		}),
		deleteEmployeeAdvancePayments: builder.mutation({
			query: (params) => ({
				url: `/api/employee-advance-payment-delete/${params.company}/${
					params.employee
				}/${params.detailsToDelete.join(',')}`,
				method: 'DELETE',
			}),
			invalidatesTags: ['AdvancePayments'],
		}),
	}),
});

export const {
	useGetEmployeeAdvancePaymentsQuery,
	useAddEmployeeAdvancePaymentsMutation,
	useUpdateEmployeeAdvancePaymentsMutation,
	useDeleteEmployeeAdvancePaymentsMutation,
} = advanceUpdationApiSlice;
