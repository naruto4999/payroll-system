import { apiSlice } from "./apiSlice";

export const deductionsHeadEntryApiSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        getDeductionsHeads: builder.query({
            query: (globalCompany) => ({
                url: `/api/deductions-head/${globalCompany.id}`,
                method: "GET",
            }),
            keepUnusedDataFor: 1,
            providesTags: ["DeductionsHeads"],
        }),
        addDeductionsHead: builder.mutation({
            query: (deductionsHead) => ({
                url: `/api/deductions-head/${deductionsHead.company}`,
                method: "POST",
                body: deductionsHead,
            }),
            invalidatesTags: ["DeductionsHeads"],
        }),
        updateDeductionsHead: builder.mutation({
            query: (deductionsHead) => ({
                url: `/api/deductions-head/${deductionsHead.company}/${deductionsHead.id}`,
                method: "PUT",
                body: deductionsHead,
            }),
            invalidatesTags: ["DeductionsHeads"],
        }),
        deleteDeductionsHead: builder.mutation({
            query: (deductionsHead) => ({
                url: `/api/deductions-head/${deductionsHead.company}/${deductionsHead.id}`,
                method: "DELETE",
            }),
            invalidatesTags: ["DeductionsHeads"],
        }),
    }),
});

export const {
    useGetDeductionsHeadsQuery,
    useAddDeductionsHeadMutation,
    useUpdateDeductionsHeadMutation,
    useDeleteDeductionsHeadMutation,
} = deductionsHeadEntryApiSlice;
