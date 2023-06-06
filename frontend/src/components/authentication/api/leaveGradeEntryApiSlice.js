import { apiSlice } from "./apiSlice";

export const leaveGradeEntryApiSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        getLeaveGrades: builder.query({
            query: (globalCompany) => ({
                url: `/api/leave-grade/${globalCompany.id}`,
                method: "GET",
            }),
            keepUnusedDataFor: 1,
            providesTags: ["LeaveGrades"],
        }),
        addLeaveGrade: builder.mutation({
            query: (leaveGrade) => ({
                url: `/api/leave-grade/${leaveGrade.company}`,
                method: "POST",
                body: leaveGrade,
            }),
            invalidatesTags: ["LeaveGrades"],
        }),
        updateLeaveGrade: builder.mutation({
            query: (leaveGrade) => ({
                url: `/api/leave-grade/${leaveGrade.company}/${leaveGrade.id}`,
                method: "PUT",
                body: leaveGrade,
            }),
            invalidatesTags: ["LeaveGrades"],
        }),
        deleteLeaveGrade: builder.mutation({
            query: (leaveGrade) => ({
                url: `/api/leave-grade/${leaveGrade.company}/${leaveGrade.id}`,
                method: "DELETE",
            }),
            invalidatesTags: ["LeaveGrades"],
        }),
    }),
});

export const {
    useGetLeaveGradesQuery,
    useAddLeaveGradeMutation,
    useUpdateLeaveGradeMutation,
    useDeleteLeaveGradeMutation,
} = leaveGradeEntryApiSlice;
