import { apiSlice } from './apiSlice';

export const transferAttendanceApiSlice = apiSlice.injectEndpoints({
	endpoints: (builder) => ({
		// getSubUserMiscSettings: builder.query({
		// 	query: (company) => ({
		// 		url: `/api/sub-user-misc-settings/${company}`,
		// 		method: 'GET',
		// 	}),
		// 	keepUnusedDataFor: 600,
		// 	providesTags: ['SubUserMiscSettings'],
		// }),
		transferAttendance: builder.mutation({
			query: (body) => ({
				url: `/api/attendance-transfer-owner-to-regular`,
				method: 'POST',
				body: body,
			}),
			// invalidatesTags: ['SubUserMiscSettings'],
		}),
		// updateSubUserMiscSettings: builder.mutation({
		// 	query: (body) => ({
		// 		url: `/api/sub-user-misc-settings/${body.company}`,
		// 		method: 'PUT',
		// 		body: body,
		// 	}),
		// 	invalidatesTags: ['SubUserMiscSettings'],
		// }),
	}),
});

export const { useTransferAttendanceMutation } = transferAttendanceApiSlice;
