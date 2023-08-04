import { apiSlice } from "./apiSlice";

export const shiftEntryApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getShifts: builder.query({
            query: globalCompany => ({
                url: `/api/shift/${globalCompany.id}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 500,
            providesTags: ['Shifts']
        }),
        addShift: builder.mutation({
            query: shift => ({
                url: `/api/shift/${shift.company}`,
                method: 'POST',
                body: shift,
            }),
            invalidatesTags: ['Shifts']
        }),
        updateShift: builder.mutation({
            query: shift => ({
                url: `/api/shift/${shift.company}/${shift.id}`,
                method: 'PUT',
                body: shift,
            }),
            invalidatesTags: ['Shifts']
        }),
        deleteShift: builder.mutation({
            query: shift => ({
                url: `/api/shift/${shift.company}/${shift.id}`,
                method: 'DELETE',
            }),
            invalidatesTags: ['Shifts']
        }),
    })
})

export const {
    useGetShiftsQuery,
    useAddShiftMutation,
    useUpdateShiftMutation,
    useDeleteShiftMutation,
} = shiftEntryApiSlice