import { apiSlice } from "./apiSlice";

export const weeklyOffHolidayOffApiSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        getWeeklyOffHolidayOff: builder.query({
            query: (globalCompany) => ({
                url: `/api/weekly-off-holiday-off/${globalCompany}`,
                method: "GET",
            }),
            keepUnusedDataFor: 500,
            providesTags: ["WeeklyOffHolidayOff"],
        }),
        addWeeklyOffHolidayOff: builder.mutation({
            query: body => ({
                url: `/api/weekly-off-holiday-off-create/${body.company}`,
                method: 'POST',
                body: body,
            }),
            invalidatesTags: ['WeeklyOffHolidayOff']
        }),
        updatedWeeklyOffHolidayOff: builder.mutation({
            query: body => ({
                url: `/api/weekly-off-holiday-off/${body.company}`,
                method: 'PUT',
                body: body,
            }),
            invalidatesTags: ['WeeklyOffHolidayOff']
        }),
    }),
});

export const { useGetWeeklyOffHolidayOffQuery, useAddWeeklyOffHolidayOffMutation, useUpdatedWeeklyOffHolidayOffMutation } = weeklyOffHolidayOffApiSlice;
