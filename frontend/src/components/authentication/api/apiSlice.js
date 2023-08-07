import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { authActions } from '../store/slices/auth';
import { useDispatch } from 'react-redux';
import { alertActions } from '../store/slices/alertSlice';

const baseQuery = fetchBaseQuery({
	baseUrl: 'http://127.0.0.1:8000/',
	prepareHeaders: (headers, { getState }) => {
		const token = getState().auth.token;
		if (token) {
			headers.set('authorization', 'Bearer ' + String(token));
			// if (!headers.has("content-type")) {
			//     console.log("hahahahahahahahhahah")
			//     headers.set("content-type", "application/json");
			//   }
			// headers.set("content-Type", "multipart/form-data")
			headers.set('ngrok-skip-browser-warning', '69420');
			// 'Content-Type': 'application/json',
		}

		return headers;
	},
});

const baseQueryWithReauth = async (args, api, extraOptions) => {
	// const dispatch = useDispatch();
	let result = await baseQuery(args, api, extraOptions);
	console.log(args);

	console.log(result);
	// if(result?.error?.status === 200) {
	//     dispatch(
	//         alertActions.createAlert({
	//           message: "We are off to a good start!",
	//           type: "success"
	//         })
	//       );
	// }

	if (result?.error?.status === 401) {
		console.log('sending refresh token');
		const refresh = api.getState().auth.refreshToken;
		console.log(refresh);

		//send refresh token to get new access token
		if (refresh != null) {
			let refreshResult = await baseQuery(
				{
					url: '/api/auth/refresh/',
					method: 'POST',
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
				console.log(api);
				api.dispatch(authActions.logout());
			}
		}
	}
	return result;
};

export const apiSlice = createApi({
	baseQuery: baseQueryWithReauth,
	tagTypes: [
		'Departments',
		'Companies',
		'CompanyDetails',
		'Regular',
		'SalaryGrades',
		'Categories',
		'Banks',
		'LeaveGrades',
		'Shifts',
		'Holidays',
		'EarningsHeads',
		'DeductionsHeads',
		'EmployeePersonalDetails',
		'EmployeeProfessionalDetails',
		'SingleEmployeeSalaryEarning',
		'EmployeeProfessionalDetails',
		'EmployeeSalaryDetails',
		'EmployeePfEsiDetails',
		'EmployeeFamilyNomineeDetails',
		'PfEsiSetup',
		'Calculations',
	],
	endpoints: (builder) => ({}),
});
