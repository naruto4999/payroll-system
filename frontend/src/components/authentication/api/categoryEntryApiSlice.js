import { apiSlice } from "./apiSlice";

export const categoryEntryApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getCategories: builder.query({
            query: globalCompany => ({
                url: `/api/category/${globalCompany.id}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 1,
            providesTags: ['Categories']
        }),
        addCategory: builder.mutation({
            query: category => ({
                url: `/api/category/${category.company}`,
                method: 'POST',
                body: category,
            }),
            invalidatesTags: ['Categories']
        }),
        updateCategory: builder.mutation({
            query: category => ({
                url: `/api/category/${category.company}/${category.id}`,
                method: 'PUT',
                body: category,
            }),
            invalidatesTags: ['Categories']
        }),
        deleteCategory: builder.mutation({
            query: category => ({
                url: `/api/category/${category.company}/${category.id}`,
                method: 'DELETE',
            }),
            invalidatesTags: ['Categories']
        }),
    })
})

export const {
    useGetCategoriesQuery,
    useAddCategoryMutation,
    useUpdateCategoryMutation,
    useDeleteCategoryMutation
} = categoryEntryApiSlice