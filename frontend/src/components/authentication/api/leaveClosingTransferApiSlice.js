import { apiSlice } from './apiSlice';

export const leaveClosingTransferApiSlice = apiSlice.injectEndpoints({
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
    transferLeaveClosing: builder.mutation({
      query: (body) => ({
        url: `/api/leave-closing-transfer`,
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
  useTransferLeaveClosingMutation
} = leaveClosingTransferApiSlice;


