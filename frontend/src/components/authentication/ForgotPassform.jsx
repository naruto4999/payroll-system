import React, { useState, useEffect } from 'react';
import { authActions } from './store/slices/auth';
import { useDispatch, useSelector } from 'react-redux';
import jwt_decode from 'jwt-decode';
import { Link, useNavigate } from 'react-router-dom';
import { FaCircleNotch } from 'react-icons/fa';
//After using createApi from Redux toolkit
import { useForgotPasswordMutation } from './api/forgotPassFormApiSlice';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};
const currentDomain = window.location.hostname;
const currentPort = window.location.port;
const frontend_url = `${import.meta.env.VITE_FRONTEND_URL}`;
const ForgotPassform = () => {
	const navigate = useNavigate();
	const auth = useSelector((state) => state.auth);
	const [forgotPassword, { isLoading, isSuccess, isError }] = useForgotPasswordMutation(); //use the isLoading later
	const [username, setUsername] = useState('');
	const [msg, setMsg] = useState('');

	useEffect(() => {
		if (auth.account != null) {
			navigate('/home');
		}
	}, []);

	console.log(isError);
	console.log(isSuccess);
	console.log(msg);
	const changeHandler = (event) => {
		// setUserDetails((prevState) => {
		//     return { ...prevState, [event.target.name]: event.target.value };
		// });
		setUsername(event.target.value);
	};
	const dispatch = useDispatch();

	const submitButtonClicked = async (e) => {
		e.preventDefault();
		console.log(username);
		try {
			const data = await forgotPassword({
				username,
				frontend_url,
			}).unwrap();
			console.log(data);
			setMsg(data.detail);
			// dispatch(
			//     authActions.setAuthTokens({
			//         token: data.access,
			//         refreshToken: data.refresh,
			//     })
			// );
			// let decoded = jwt_decode(data.access);
			// const user = {
			//     id: decoded.user_id,
			//     // email: decoded.email,
			//     username: decoded.username,
			// };
			// dispatch(authActions.setAccount(user));
			// navigate("/home");
			setUsername('');
		} catch (err) {
			// console.log(err.data.username);
			setMsg(err.data.username);
		}
	};

	return (
		<main className="mx-auto h-screen max-w-md ">
			<section className="sticky top-0 z-10 p-2">
				<img src="../../../public/logo_dark.png" alt="LOGO" className="mx-auto h-16 w-auto object-center" />
			</section>

			<section id="forgot-password" className="flex h-[calc(100vh-80px)] flex-col md:justify-center">
				<div
					className="mt-2 box-border flex flex-col rounded-lg
                bg-zinc-50 bg-opacity-60 p-6 shadow-xl dark:bg-black dark:bg-opacity-50 md:mx-6 md:mt-0"
				>
					<h1 className="mb-8 text-center text-4xl font-medium text-gray-900 text-opacity-70 dark:text-slate-100 dark:text-opacity-70">
						Forgot Password?
					</h1>
					<form
						action=""
						className="mx-6 flex flex-col justify-center gap-4 text-sm md:text-base"
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
							{isError || isSuccess ? (
								<p
									className={classNames(
										isError
											? 'text-red-500 dark:text-red-700'
											: 'text-green-500 dark:text-green-700',
										'mt-1 text-sm font-bold'
									)}
								>
									{msg}
								</p>
							) : (
								''
							)}
						</div>

						<button className="my-2 w-full rounded-lg bg-teal-500 p-2 text-gray-900 text-opacity-70 hover:bg-teal-600 active:bg-teal-700 dark:bg-teal-700 dark:text-slate-100 dark:text-opacity-70 dark:hover:bg-teal-600 dark:active:bg-teal-500">
							Send Email
						</button>
					</form>

					<Link
						to="/register"
						className="bottom-0 my-5 text-center text-sm text-gray-900 text-opacity-70 transition-all hover:text-opacity-100 dark:text-white dark:text-opacity-70 dark:hover:text-opacity-100 md:text-base"
					>
						Don't have an account? Register Now
					</Link>
					<Link
						to="/login"
						className="bottom-0 text-center text-sm text-gray-900 text-opacity-70 transition-all hover:text-opacity-100 dark:text-white dark:text-opacity-70 md:text-base"
					>
						Already have an account? Sign in
					</Link>
				</div>
				<div
					className={classNames(
						isLoading ? '' : 'hidden',
						'z-50 mx-auto mt-2 flex h-fit w-fit items-center rounded bg-indigo-600 p-2 font-medium'
					)}
				>
					<FaCircleNotch className="mr-2 animate-spin text-white" />
					Processing...
				</div>
			</section>
		</main>
	);
};

export default ForgotPassform;
