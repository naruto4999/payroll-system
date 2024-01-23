import { apiSlice } from './apiSlice';

export const fullAndFinalApiSlice = apiSlice.injectEndpoints({
	endpoints: (builder) => ({
		earnedAmountWithPreparedSalary: builder.query({
			query: (body) => ({
				url: `/api/earned-amount-prepared-salary/${body.company}/${body.employee}`,
				method: 'GET',
			}),
			keepUnusedDataFor: 500,
			providesTags: ['EarnedAmountPreparedSalary'],
		}),
		getFullAndFinal: builder.query({
			query: (body) => ({
				url: `/api/get-full-and-final/${body.company}/${body.employee}`,
				method: 'GET',
			}),
			keepUnusedDataFor: 500,
			providesTags: ['FullAndFinal'],
		}),
		getElLeft: builder.query({
			query: (body) => ({
				url: `/api/el-left/${body.company}/${body.employee}`,
				method: 'GET',
			}),
			keepUnusedDataFor: 500,
			providesTags: ['ELLeft'],
		}),
		getYearlyBonusAmount: builder.query({
			query: (body) => ({
				url: `/api/bonus-amount/${body.company}/${body.employee}/${body.year}`,
				method: 'GET',
			}),
			keepUnusedDataFor: 500,
			providesTags: (result, error) => {
				console.log(result);
				return [{ type: 'EmoloyeeYearlyBonus', id: result.employee }];
			},
			// providesTags: ['EmoloyeeYearlyBonus'],
		}),
		addFullAndFinal: builder.mutation({
			query: (body) => ({
				url: `/api/full-and-final/${body.company}/${body.employee}`,
				method: 'POST',
				body: body,
			}),
			invalidatesTags: ['FullAndFinal'],
		}),
		generateFullAndFinalReport: builder.mutation({
			query: (body) => ({
				url: `/api/generate-full-and-final-report`,
				method: 'POST',
				body: body,
			}),
			// invalidatesTags: ['FullAndFinal'],
		}),
	}),
});

export const {
	useEarnedAmountWithPreparedSalaryQuery,
	useGetFullAndFinalQuery,
	useGetElLeftQuery,
	useGetYearlyBonusAmountQuery,
	useAddFullAndFinalMutation,
	useGenerateFullAndFinalReportMutation,
} = fullAndFinalApiSlice;
