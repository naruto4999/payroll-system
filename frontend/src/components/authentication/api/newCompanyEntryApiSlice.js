import { apiSlice } from "./apiSlice";

export const newCompanyEntryApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getCompanies: builder.query({
            query: () => ({
                url: '/api/company',
                method: 'GET',
            }),
            keepUnusedDataFor: 500,
            providesTags: ['Companies']
        }),
        addCompanies: builder.mutation({
            query: company => ({
                url: "/api/company",
                method: 'POST',
                body: company,
            }),
            invalidatesTags: ['Companies']
        }),
        visibleCompany: builder.mutation({
            query: (body) => ({
                url:'/api/company-visible',
                method: 'PATCH',
                body: body,
            }),
            invalidatesTags: ['Companies']
        }),
        updateCompanies: builder.mutation({
            query: company => ({
                url:`/api/edit-company/${company.id}`,
                method: 'PUT',
                body: company,
            }),
            invalidatesTags: ['Companies']
        }),
        deleteCompany: builder.mutation({
            query: ({ id }) => ({
                url: `/api/edit-company/${id}`,
                method: 'DELETE',
            }),
            invalidatesTags: ['Companies']
        }),
        
    })
});

export const {
    useGetCompaniesQuery,
    useAddCompaniesMutation,
    useUpdateCompaniesMutation,
    useDeleteCompanyMutation,
    useVisibleCompanyMutation
} = newCompanyEntryApiSlice