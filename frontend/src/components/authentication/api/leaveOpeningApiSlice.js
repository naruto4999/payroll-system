import { apiSlice } from './apiSlice';

export const leaveOpeningApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    // getWeeklyOffHolidayOff: builder.query({
    // 	query: (globalCompany) => ({
    // 		url: `/api/weekly-off-holiday-off/${globalCompany}`,
    // 		method: 'GET',
    // 	}),
    // 	keepUnusedDataFor: 500,
    // 	providesTags: ['WeeklyOffHolidayOff'],
    // }),
    // addWeeklyOffHolidayOff: builder.mutation({
    // 	query: (body) => ({
    // 		url: `/api/weekly-off-holiday-off-create/${body.company}`,
    // 		method: 'POST',
    // 		body: body,
    // 	}),
    // 	invalidatesTags: ['WeeklyOffHolidayOff'],
    // }),
    addOrUpdateLeaveOpening: builder.mutation({
      query: (body) => ({
        url: `/api/leave-opening`,
        method: 'POST',
        body: body,
      }),
      invalidatesTags: [
        'AllEmployeeLeaveOpening'
      ],
    }),

  }),
});

export const {
  useAddOrUpdateLeaveOpeningMutation
} = leaveOpeningApiSlice;

