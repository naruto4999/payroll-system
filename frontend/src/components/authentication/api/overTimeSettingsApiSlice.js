import { apiSlice } from './apiSlice';

export const resignationApiSlice = apiSlice.injectEndpoints({
	endpoints: (builder) => ({
		updateOverTimeSettings: builder.mutation({
			query: (body) => ({
				url: `/api/subuser-overtime-settings`,
				method: 'POST',
				body: body,
			}),
			invalidatesTags: ['OverTimeSettings'],
		}),
		// unresign: builder.mutation({
		// 	query: (body) => ({
		// 		url: `/api/unresign/${body.company}/${body.employee}`,
		// 		method: 'PATCH',
		// 		body: body,
		// 	}),
		// 	invalidatesTags: ['EmployeePersonalDetails', 'EmployeeProfessionalDetails'],
		// }),
		getOverTimeSettings: builder.query({
			query: (body) => ({
				url: `/api/get-subuser-overtime-settings/${body.company}/${body.year}/${body.month}`,
				method: 'GET',
			}),
			keepUnusedDataFor: 600,
			providesTags: ['OverTimeSettings'],
		}),
	}),
});

export const { useUpdateOverTimeSettingsMutation, useGetOverTimeSettingsQuery } = resignationApiSlice;
