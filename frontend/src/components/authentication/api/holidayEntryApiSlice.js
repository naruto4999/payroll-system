import { apiSlice } from "./apiSlice";

export const holidayEntryApiSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        getHolidays: builder.query({
            query: (globalCompany) => ({
                url: `/api/holiday/${globalCompany.id}`,
                method: "GET",
            }),
            keepUnusedDataFor: 1,
            providesTags: ["Holidays"],
        }),
        // addLeaveGrade: builder.mutation({
        //     query: (leaveGrade) => ({
        //         url: `/api/leave-grade/${leaveGrade.company}`,
        //         method: "POST",
        //         body: leaveGrade,
        //     }),
        //     invalidatesTags: ["Holidays"],
        // }),
        // updateLeaveGrade: builder.mutation({
        //     query: (leaveGrade) => ({
        //         url: `/api/leave-grade/${leaveGrade.company}/${leaveGrade.id}`,
        //         method: "PUT",
        //         body: leaveGrade,
        //     }),
        //     invalidatesTags: ["Holidays"],
        // }),
        // deleteLeaveGrade: builder.mutation({
        //     query: (leaveGrade) => ({
        //         url: `/api/leave-grade/${leaveGrade.company}/${leaveGrade.id}`,
        //         method: "DELETE",
        //     }),
        //     invalidatesTags: ["Holidays"],
        // }),
    }),
});

export const {
    useGetHolidaysQuery,
} = holidayEntryApiSlice;
