import { apiSlice } from "./apiSlice";

export const shiftEntryApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getShifts: builder.query({
            query: globalCompany => ({
                url: `/api/shift/${globalCompany.id}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 1,
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
        // deleteBank: builder.mutation({
        //     query: bank => ({
        //         url: `/api/bank/${bank.company}/${bank.id}`,
        //         method: 'DELETE',
        //     }),
        //     invalidatesTags: ['Shifts']
        // }),
    })
})

export const {
    useGetShiftsQuery,
    useAddShiftMutation,
    useUpdateShiftMutation,
} = shiftEntryApiSlice