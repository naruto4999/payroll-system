import { apiSlice } from './apiSlice';

export const bonusCalculationApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    addOrUpdateBonusCalculation: builder.mutation({
      query: (body) => ({
        url: `/api/bonus-calculation/${body.company}`,
        method: 'POST',
        body: body,
      }),
      invalidatesTags: ['BonusCalculations', 'BonusPercentage', 'EmoloyeeYearlyBonus'],
    }),
    getBonusCalculations: builder.query({
      query: (body) => ({
        url: `/api/get-bonus-calculation/${body.company}/${body.startDate}/${body.endDate}`,
        method: 'GET',
      }),
      keepUnusedDataFor: 500,
      providesTags: ['BonusCalculations'],
    }),
    getBonusPercentage: builder.query({
      query: (company) => ({
        url: `/api/get-bonus-percentage/${company}`,
        method: 'GET',
      }),
      keepUnusedDataFor: 500,
      providesTags: ['BonusPercentage'],
    }),
  }),
});

export const { useAddOrUpdateBonusCalculationMutation, useGetBonusCalculationsQuery, useGetBonusPercentageQuery } =
  bonusCalculationApiSlice;
