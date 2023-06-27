import { apiSlice } from "./apiSlice";

export const earningsHeadEntryApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getEarningsHeads: builder.query({
            query: globalCompany => ({
                url: `/api/earnings-head/${globalCompany.id}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 1,
            providesTags: ['EarningsHeads']
        }),
        addEarningsHead: builder.mutation({
            query: earningsHead => ({
                url: `/api/earnings-head/${earningsHead.company}`,
                method: 'POST',
                body: earningsHead,
            }),
            invalidatesTags: ['EarningsHeads']
        }),
        updateEarningsHead: builder.mutation({
            query: earningsHead => ({
                url: `/api/earnings-head/${earningsHead.company}/${earningsHead.id}`,
                method: 'PUT',
                body: earningsHead,
            }),
            invalidatesTags: ['EarningsHeads']
        }),
        deleteEarningsHead: builder.mutation({
            query: earningsHead => ({
                url: `/api/earnings-head/${earningsHead.company}/${earningsHead.id}`,
                method: 'DELETE',
            }),
            invalidatesTags: ['EarningsHeads']
        }),
    })
})

export const {
    useGetEarningsHeadsQuery,
    useAddEarningsHeadMutation,
    useUpdateEarningsHeadMutation,
    useDeleteEarningsHeadMutation,
} = earningsHeadEntryApiSlice