import { apiSlice } from "./apiSlice";

export const bankEntryApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getBanks: builder.query({
            query: globalCompany => ({
                url: `/api/bank/${globalCompany.id}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 1,
            providesTags: ['Banks']
        }),
        addBank: builder.mutation({
            query: bank => ({
                url: `/api/bank/${bank.company}`,
                method: 'POST',
                body: bank,
            }),
            invalidatesTags: ['Banks']
        }),
        updateBank: builder.mutation({
            query: bank => ({
                url: `/api/bank/${bank.company}/${bank.id}`,
                method: 'PUT',
                body: bank,
            }),
            invalidatesTags: ['Banks']
        }),
        deleteBank: builder.mutation({
            query: bank => ({
                url: `/api/bank/${bank.company}/${bank.id}`,
                method: 'DELETE',
            }),
            invalidatesTags: ['Banks']
        }),
    })
})

export const {
    useGetBanksQuery,
    useAddBankMutation,
    useUpdateBankMutation,
    useDeleteBankMutation
} = bankEntryApiSlice