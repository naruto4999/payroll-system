import { apiSlice } from './apiSlice';

export const calculationsApiSlice = apiSlice.injectEndpoints({
	endpoints: (builder) => ({
		getCalculations: builder.query({
			query: (globalCompany) => ({
				url: `/api/calculations/${globalCompany}`,
				method: 'GET',
			}),
			keepUnusedDataFor: 600,
			providesTags: ['Calculations'],
		}),
		addCalculations: builder.mutation({
			query: (body) => ({
				url: `/api/calculations-create`,
				method: 'POST',
				body: body,
			}),
			invalidatesTags: ['Calculations'],
		}),
		updateCalculations: builder.mutation({
			query: (body) => ({
				url: `/api/calculations/${body.company}`,
				method: 'PUT',
				body: body,
			}),
			invalidatesTags: ['Calculations'],
		}),
	}),
});

export const {
	useGetCalculationsQuery,
	useAddCalculationsMutation,
	useUpdateCalculationsMutation,
} = calculationsApiSlice;
