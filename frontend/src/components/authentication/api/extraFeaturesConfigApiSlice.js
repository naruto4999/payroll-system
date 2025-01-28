import { apiSlice } from './apiSlice';

export const extraFeaturesConfigApiSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        getExtraFeaturesConfig: builder.query({
            query: (company) => ({
                url: `/api/extra-features-config/${company}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 600,
            providesTags: ['ExtraFeaturesConfig'],
        }),
        addExtraFeaturesConfig: builder.mutation({
            query: (body) => ({
                url: `/api/extra-features-config-create`,
                method: 'POST',
                body: body,
            }),
            invalidatesTags: ['ExtraFeaturesConfig'],
        }),
        updateExtraFeaturesConfig: builder.mutation({
            query: (body) => ({
                url: `/api/extra-features-config/${body.company}`,
                method: 'PUT',
                body: body,
            }),
            invalidatesTags: ['ExtraFeaturesConfig'],
        }),
    }),
});

export const {
    useGetExtraFeaturesConfigQuery,
    useAddExtraFeaturesConfigMutation,
    useUpdateExtraFeaturesConfigMutation,
} = extraFeaturesConfigApiSlice;
