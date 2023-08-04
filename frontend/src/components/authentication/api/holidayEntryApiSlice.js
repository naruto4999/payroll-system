import { apiSlice } from "./apiSlice";

export const holidayEntryApiSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        getHolidays: builder.query({
            query: (globalCompany) => ({
                url: `/api/holiday/${globalCompany.id}`,
                method: "GET",
            }),
            keepUnusedDataFor: 500,
            providesTags: ["Holidays"],
        }),
        addHoliday: builder.mutation({
            query: (holiday) => ({
                url: `/api/holiday/${holiday.company}`,
                method: "POST",
                body: holiday,
            }),
            invalidatesTags: ["Holidays"],
        }),
        updateHoliday: builder.mutation({
            query: (holiday) => ({
                url: `/api/holiday/${holiday.company}/${holiday.id}`,
                method: "PUT",
                body: holiday,
            }),
            invalidatesTags: ["Holidays"],
        }),
        deleteHoliday: builder.mutation({
            query: (holiday) => ({
                url: `/api/holiday/${holiday.company}/${holiday.id}`,
                method: "DELETE",
            }),
            invalidatesTags: ["Holidays"],
        }),
    }),
});

export const {
    useGetHolidaysQuery,
    useAddHolidayMutation,
    useUpdateHolidayMutation,
    useDeleteHolidayMutation,
} = holidayEntryApiSlice;
