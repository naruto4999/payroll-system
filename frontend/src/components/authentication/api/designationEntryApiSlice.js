import { apiSlice } from "./apiSlice";

export const designationEntryApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getDesignations: builder.query({
            query: globalCompany => ({
                url: `/api/designation/${globalCompany.id}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 1,
            providesTags: ['Designations']
        }),
        addDesignation: builder.mutation({
            query: designation => ({
                url: `/api/designation/${designation.company}`,
                method: 'POST',
                body: designation,
            }),
            invalidatesTags: ['Designations']
        }),
        updateDesignation: builder.mutation({
            query: designation => ({
                url: `/api/designation/${designation.company}/${designation.id}`,
                method: 'PUT',
                body: designation,
            }),
            invalidatesTags: ['Designations']
        }),
        deleteDesignation: builder.mutation({
            query: designation => ({
                url: `/api/designation/${designation.company}/${designation.id}`,
                method: 'DELETE',
            }),
            invalidatesTags: ['Designations']
        }),
    })
})

export const {
    useGetDesignationsQuery,
    useAddDesignationMutation,
    useUpdateDesignationMutation,
    useDeleteDesignationMutation,
} = designationEntryApiSlice