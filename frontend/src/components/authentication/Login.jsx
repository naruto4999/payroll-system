import React, { useState, useEffect } from 'react';
import { authActions } from './store/slices/auth';
import { useDispatch, useSelector } from 'react-redux';
import jwt_decode from 'jwt-decode';
import { Link, useNavigate } from 'react-router-dom';

//After using createApi from Redux toolkit
import { useLoginMutation } from './api/loginApiSlice';

const LoginForm = () => {
	const navigate = useNavigate();
	const auth = useSelector((state) => state.auth);
	const [login, { isLoading }] = useLoginMutation(); //use the isLoading later
	const [userDetails, setUserDetails] = useState({
		// email: "",
		password: '',
		username: '',
	});
	const [errorMessage, setErrorMessage] = useState('');
	console.log(auth);
	useEffect(() => {
		if (auth.account != null) {
			navigate('/home/select-company');
		}
	}, []);

	console.log(userDetails);

	const changeHandler = (event) => {
		setUserDetails((prevState) => {
			return { ...prevState, [event.target.name]: event.target.value };
		});
	};
	const dispatch = useDispatch();

	const submitButtonClicked = async (e) => {
		setErrorMessage('');
		e.preventDefault();
		console.log(userDetails);
		try {
			const data = await login({
				// email: userDetails.email,
				password: userDetails.password,
				username: userDetails.username,
			}).unwrap();
			console.log(data);
			dispatch(
				authActions.setAuthTokens({
					token: data.access,
					refreshToken: data.refresh,
				})
			);
			let decoded = jwt_decode(data.access);
			console.log(decoded);
			const user = {
				id: decoded.user_id,
				role: decoded.role,
				username: decoded.username,
				is_admin: decoded.is_admin,
				subscription_end_date: decoded.subscription_end_date,
			};
			dispatch(authActions.setAccount(user));
			navigate('/home/select-company');
			setUserDetails({
				// email: "",
				password: '',
				username: '',
			});
		} catch (err) {
			console.log(err.status);

			console.log(err);
			if (err.status == 401) {
				if (err.data?.detail == 'No active account found with the given credentials') {
					setErrorMessage('Invalid username or password');
				} else if (err.data?.detail) {
					setErrorMessage(
						err.status == 401 && err?.data?.detail + ' \nOr email us at payper.webapp@gmail.com'
					);
				}
			}
		}
	};

	return (
		<main className="mx-auto h-screen max-w-md ">
			<section className="sticky top-0 z-10 p-2">
				<img
					src={`${import.meta.env.VITE_PUBLIC_URL}logo_dark.png`}
					alt="LOGO"
					className="mx-auto h-16 w-auto object-center"
				/>
			</section>

			<section id="login" className="flex h-[calc(100vh-80px)] flex-col md:justify-center">
				<div
					className="mt-2 box-border flex flex-col rounded-lg
                bg-zinc-50 bg-opacity-60 p-6 shadow-xl dark:bg-black dark:bg-opacity-50 md:mx-6 md:mt-0"
				>
					<h1 className="mb-8 text-center text-4xl font-medium text-gray-900 text-opacity-70 dark:text-slate-100 dark:text-opacity-70">
						Sign in
					</h1>
					<form
						action=""
						className="mx-6 flex flex-col justify-center gap-8 text-sm md:text-base"
						onSubmit={submitButtonClicked}
					>
						{/* using an empty space as a placeholder so when placeholder
                    dissapears if user enter something then the label stays on top
                    we are using 'placeholder-shown' pseudo class butt it's not available in taiwind */}
						<div className="relative">
							<input
								className="peer  w-full border-b-2 border-gray-800 border-opacity-25 bg-transparent p-1 outline-none transition focus:border-opacity-75 dark:border-slate-100 dark:border-opacity-25 md:p-2"
								type="text"
								id="username"
								name="username"
								placeholder=" "
								onChange={changeHandler}
							/>
							<label
								htmlFor="username"
								className="absolute left-0 top-1 cursor-text italic text-gray-900 text-opacity-70 transition-all peer-focus:-top-4 peer-focus:text-xs peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70"
							>
								Username
							</label>
						</div>

						<div className="relative">
							<input
								className="peer  w-full border-b-2 border-gray-800 border-opacity-25 bg-transparent p-1 outline-none transition focus:border-opacity-75 dark:border-slate-100 dark:border-opacity-25 md:p-2"
								type="password"
								id="password"
								name="password"
								placeholder=" "
								onChange={changeHandler}
							/>
							<label
								htmlFor="password"
								className="absolute left-0 top-1 cursor-text italic text-gray-900 text-opacity-70 transition-all peer-focus:-top-4 peer-focus:text-xs peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70"
							>
								Password
							</label>
							<div className="mt-1 font-semibold text-red-600">{errorMessage}</div>
						</div>
						<button className="my-2 w-full rounded-lg bg-teal-500 p-2 text-gray-900 text-opacity-70 hover:bg-teal-600 active:bg-teal-700 dark:bg-teal-700 dark:text-slate-100 dark:text-opacity-70 dark:hover:bg-teal-600 dark:active:bg-teal-500">
							Sign in
						</button>
					</form>
					<Link
						to="/forgot-password"
						className="my-5 text-center text-sm text-gray-900 text-opacity-70 transition-all hover:text-opacity-100 dark:text-white dark:text-opacity-70 dark:hover:text-opacity-100 md:text-base"
					>
						Forgot Pasword?
					</Link>

					<Link
						to="/register"
						className="bottom-0 text-center text-sm text-gray-900 text-opacity-70 transition-all hover:text-opacity-100 dark:text-white dark:text-opacity-70 dark:hover:text-opacity-100 md:text-base"
					>
						Don't have an account? Register Now
					</Link>
				</div>
			</section>
		</main>
	);
};

export default LoginForm;
