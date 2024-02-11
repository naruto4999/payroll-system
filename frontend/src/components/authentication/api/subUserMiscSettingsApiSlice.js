import { apiSlice } from './apiSlice';

export const subUserMiscSettingsApiSlice = apiSlice.injectEndpoints({
	endpoints: (builder) => ({
		getSubUserMiscSettings: builder.query({
			query: (company) => ({
				url: `/api/sub-user-misc-settings/${company}`,
				method: 'GET',
			}),
			keepUnusedDataFor: 600,
			providesTags: ['SubUserMiscSettings'],
		}),
		addSubUserMiscSettings: builder.mutation({
			query: (body) => ({
				url: `/api/sub-user-misc-settings-create`,
				method: 'POST',
				body: body,
			}),
			invalidatesTags: ['SubUserMiscSettings'],
		}),
		updateSubUserMiscSettings: builder.mutation({
			query: (body) => ({
				url: `/api/sub-user-misc-settings/${body.company}`,
				method: 'PUT',
				body: body,
			}),
			invalidatesTags: ['SubUserMiscSettings'],
		}),
	}),
});

export const {
	useGetSubUserMiscSettingsQuery,
	useAddSubUserMiscSettingsMutation,
	useUpdateSubUserMiscSettingsMutation,
} = subUserMiscSettingsApiSlice;
