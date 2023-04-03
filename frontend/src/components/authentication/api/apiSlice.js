import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { authActions } from "../store/slices/auth";

const baseQuery = fetchBaseQuery({
    baseUrl: "http://127.0.0.1:8000",
    prepareHeaders: (headers, { getState }) => {
        const token = getState().auth.token;
        if (token) {
            headers.set("authorization", "Bearer " + String(token));
            headers.set("content-Type", "application/json")
            headers.set("ngrok-skip-browser-warning", "69420")
            // 'Content-Type': 'application/json',
        }
        return headers;
    },
});

const baseQueryWithReauth = async (args, api, extraOptions) => {
    let result = await baseQuery(args, api, extraOptions);

    console.log(result);

    if (result?.error?.status === 401) {
        console.log("sending refresh token");
        const refresh = api.getState().auth.refreshToken;
        console.log(refresh);

        //send refresh token to get new access token
        if (refresh != null) {
            let refreshResult = await baseQuery(
                {
                    url: "/api/auth/refresh/",
                    method: "POST",
                    body: { refresh: refresh },
                },
                api,
                extraOptions
            );
            console.log(refreshResult);
            if (refreshResult?.data) {
                //store the new token into redux store
                api.dispatch(
                    authActions.setAuthTokens({
                        token: refreshResult.data.access,
                        refreshToken: refreshResult.data.refresh,
                    })
                );
                //retry the original query with new access token
                result = await baseQuery(args, api, extraOptions);
            } else {
                api.dispatch(logout());
            }
        }
    }
    return result;
};

export const apiSlice = createApi({
    baseQuery: baseQueryWithReauth,
    tagTypes: ["Departments", "Companies", "CompanyDetails"],
    endpoints: (builder) => ({}),
});
