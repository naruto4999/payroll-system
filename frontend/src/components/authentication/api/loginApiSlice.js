import { apiSlice } from "./apiSlice";

export const loginApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        login: builder.mutation({
            query: credentials => ({
                url: "/api/auth/login/",
                method: 'POST',
                body: { ...credentials }
            })
        })
    })
})

export const {
    useLoginMutation
} = loginApiSlice