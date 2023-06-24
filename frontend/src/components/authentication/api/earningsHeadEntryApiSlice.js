import { apiSlice } from "./apiSlice";

export const earningsHeadEntryApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getEarningsHeads: builder.query({
            query: globalCompany => ({
                url: `/api/earnings-head/${globalCompany.id}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 1,
            providesTags: ['EarningsHead']
        }),
        addEarningsHead: builder.mutation({
            query: earningsHead => ({
                url: `/api/earnings-head/${earningsHead.company}`,
                method: 'POST',
                body: earningsHead,
            }),
            invalidatesTags: ['EarningsHead']
        }),
        updateEarningsHead: builder.mutation({
            query: earningsHead => ({
                url: `/api/earnings-head/${earningsHead.company}/${earningsHead.id}`,
                method: 'PUT',
                body: earningsHead,
            }),
            invalidatesTags: ['EarningsHead']
        }),
        deleteEarningsHead: builder.mutation({
            query: earningsHead => ({
                url: `/api/earnings-head/${earningsHead.company}/${earningsHead.id}`,
                method: 'DELETE',
            }),
            invalidatesTags: ['EarningsHead']
        }),
    })
})

export const {
    useGetEarningsHeadsQuery,
    useAddEarningsHeadMutation,
    useUpdateEarningsHeadMutation,
    useDeleteEarningsHeadMutation,
} = earningsHeadEntryApiSlice