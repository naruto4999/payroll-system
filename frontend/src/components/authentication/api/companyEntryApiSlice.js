import { apiSlice } from './apiSlice';

export const companyEntryApiSlice = apiSlice.injectEndpoints({
	endpoints: (builder) => ({
		getCompanyDetails: builder.query({
			query: (id) => `/api/company-details/${id}`,
			keepUnusedDataFor: 5,
			providesTags: ['CompanyDetails'],
		}),
		updateCompanyDetails: builder.mutation({
			query: (body) => ({
				url: `/api/company-details/${body.company}`,
				method: 'PUT',
				body: body,
			}),
			invalidatesTags: ['CompanyDetails'],
		}),
		addCompanyDetails: builder.mutation({
			query: (details) => ({
				url: '/api/company-details',
				method: 'POST',
				body: details,
			}),
			invalidatesTags: ['CompanyDetails'],
		}),
	}),
});

export const { useGetCompanyDetailsQuery, useUpdateCompanyDetailsMutation, useAddCompanyDetailsMutation } =
	companyEntryApiSlice;
