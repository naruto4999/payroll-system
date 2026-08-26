import React, { useEffect, useState } from 'react';
import { FiArrowRight, FiEye, FiEyeOff, FiLock, FiUser } from 'react-icons/fi';
import { useDispatch, useSelector } from 'react-redux';
import { Link, useNavigate } from 'react-router-dom';
import jwt_decode from 'jwt-decode';
import Button from '../UI/Button';
import Input from '../UI/Input';
import { authActions } from './store/slices/auth';
import { useLoginMutation } from './api/loginApiSlice';

const LoginForm = () => {
	const navigate = useNavigate();
	const dispatch = useDispatch();
	const auth = useSelector((state) => state.auth);
	const [login, { isLoading }] = useLoginMutation();
	const [showPassword, setShowPassword] = useState(false);
	const [userDetails, setUserDetails] = useState({ password: '', username: '' });
	const [errorMessage, setErrorMessage] = useState('');

	useEffect(() => {
		if (auth.account != null) {
			navigate('/home/select-company');
		}
	}, [auth.account, navigate]);

	const changeHandler = (event) => {
		setUserDetails((prevState) => ({ ...prevState, [event.target.name]: event.target.value }));
	};

	const submitButtonClicked = async (e) => {
		e.preventDefault();
		setErrorMessage('');

		try {
			const data = await login(userDetails).unwrap();
			dispatch(
				authActions.setAuthTokens({
					token: data.access,
					refreshToken: data.refresh,
				})
			);

			const decoded = jwt_decode(data.access);
			dispatch(
				authActions.setAccount({
					id: decoded.user_id,
					role: decoded.role,
					username: decoded.username,
					is_admin: decoded.is_admin,
					subscription_end_date: decoded.subscription_end_date,
				})
			);
			navigate('/home/select-company');
			setUserDetails({ password: '', username: '' });
		} catch (err) {
			if (err.status === 401) {
				if (err.data?.detail === 'No active account found with the given credentials') {
					setErrorMessage('Invalid username or password');
				} else if (err.data?.detail) {
					setErrorMessage(`${err.data.detail} Or email us at payper.webapp@gmail.com`);
				}
			} else {
				setErrorMessage('Unable to sign in right now. Please try again.');
			}
		}
	};

	return (
		<main className="relative flex min-h-screen overflow-hidden bg-brand-light text-zinc-900 dark:bg-brand-canvas dark:text-white">
			<div className="pointer-events-none absolute -left-32 -top-32 h-80 w-80 rounded-full bg-teal-200/40 blur-3xl dark:bg-teal-900/30" />
			<div className="pointer-events-none absolute -bottom-40 right-0 h-96 w-96 rounded-full bg-blueAccent-100/60 blur-3xl dark:bg-blueAccent-900/20" />

			<section className="relative hidden w-[46%] flex-col justify-between overflow-hidden bg-brand-ink p-12 text-white lg:flex xl:p-16">
				<div className="absolute -right-24 top-16 h-72 w-72 rounded-full border-[36px] border-teal-400/10" />
				<div className="absolute -bottom-40 -left-32 h-96 w-96 rounded-full border-[52px] border-teal-300/10" />
				<Link to="/" className="relative z-10 inline-flex items-center">
					<img
						src={`${import.meta.env.VITE_PUBLIC_URL}logo_text_dark.svg`}
						alt="Payper"
						className="h-auto w-44 brightness-0 invert"
					/>
				</Link>
				<div className="relative z-10 max-w-md pb-8">
					<p className="mb-5 text-sm font-medium uppercase tracking-[0.24em] text-teal-300">Payroll, simplified</p>
					<h1 className="text-5xl font-semibold leading-[1.08] tracking-[-0.04em] xl:text-6xl">
						Make every payday feel effortless.
					</h1>
					<p className="mt-6 max-w-sm text-base leading-7 text-slate-300">
						A smarter way to manage your people, payroll, and the details that keep your business moving.
					</p>
					<div className="mt-10 flex items-center gap-3 text-sm text-slate-300">
						<span className="flex h-9 w-9 items-center justify-center rounded-full bg-white/10 text-teal-300">
							<FiLock />
						</span>
						Secure access to your payroll workspace
					</div>
				</div>
				<p className="relative z-10 text-xs text-slate-400">A Smart Payroll System on Cloud</p>
			</section>

			<section className="relative flex w-full items-center justify-center px-5 py-10 sm:px-8 lg:w-[54%] lg:px-12">
				<div className="w-full max-w-md">
					<div className="mb-8 flex justify-center lg:hidden">
						<Link to="/" className="inline-flex items-center">
							<img
								src={`${import.meta.env.VITE_PUBLIC_URL}logo_text_dark.svg`}
								alt="Payper"
								className="h-auto w-36 brightness-0 invert"
							/>
						</Link>
					</div>

					<div className="rounded-[2rem] border border-white/80 bg-white/75 p-6 shadow-brand-card backdrop-blur-xl dark:border-white/10 dark:bg-zinc-900/70 sm:p-10">
							<div className="mb-7">
							<p className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-teal-700 dark:text-teal-400">Welcome back</p>
							<h2 className="text-3xl font-semibold tracking-tight text-zinc-900 dark:text-white">Sign in to payper</h2>
							<p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">Continue to your payroll workspace.</p>
						</div>

						<form className="space-y-4" onSubmit={submitButtonClicked}>
							<div>
								<label htmlFor="username" className="mb-1.5 block text-xs font-medium text-zinc-700 dark:text-zinc-300">Username</label>
								<Input
									type="text"
									id="username"
									name="username"
									value={userDetails.username}
									onChange={changeHandler}
									placeholder="Enter your username"
									autoComplete="username"
									required
									size="sm"
									startAdornment={<FiUser />}
									className="h-11 rounded-lg border-zinc-700 bg-zinc-800 px-10 text-zinc-100 placeholder:text-zinc-500 focus:border-teal-500 focus:ring-4 focus:ring-teal-500/10"
								/>
							</div>

							<div>
								<div className="mb-2 flex items-center justify-between">
									<label htmlFor="password" className="text-xs font-medium text-zinc-700 dark:text-zinc-300">Password</label>
									<Link to="/forgot-password" className="text-xs font-medium text-teal-700 transition hover:text-teal-900 dark:text-teal-400 dark:hover:text-teal-300">Forgot password?</Link>
								</div>
								<Input
									type={showPassword ? 'text' : 'password'}
									id="password"
									name="password"
									value={userDetails.password}
									onChange={changeHandler}
									placeholder="Enter your password"
									autoComplete="current-password"
									required
									size="sm"
									startAdornment={<FiLock />}
									endAdornment={
										<button
											type="button"
											onClick={() => setShowPassword((visible) => !visible)}
											aria-label={showPassword ? 'Hide password' : 'Show password'}
											className="transition hover:text-zinc-200"
										>
											{showPassword ? <FiEyeOff /> : <FiEye />}
										</button>
									}
									className="h-11 rounded-lg border-zinc-700 bg-zinc-800 pl-10 pr-11 text-zinc-100 placeholder:text-zinc-500 focus:border-teal-500 focus:ring-4 focus:ring-teal-500/10"
								/>
							</div>

							{errorMessage && <p role="alert" className="pt-1 text-xs leading-5 text-red-500 dark:text-red-400">{errorMessage}</p>}

							<Button type="submit" disabled={isLoading} className="group h-12 w-full rounded-lg bg-teal-700 px-5 text-sm font-semibold text-white shadow-lg shadow-teal-700/20 transition hover:bg-teal-800 hover:shadow-teal-700/30 focus:outline-none focus:ring-4 focus:ring-teal-600/20 disabled:cursor-not-allowed disabled:opacity-60">
								{isLoading ? 'Signing in...' : 'Sign in'}
								{!isLoading && <FiArrowRight className="transition-transform group-hover:translate-x-1" />}
							</Button>
						</form>

						<p className="mt-8 text-center text-sm text-zinc-500 dark:text-zinc-400">
							Don't have an account?{' '}
							<Link to="/register" className="font-semibold text-teal-700 hover:text-teal-900 dark:text-teal-400 dark:hover:text-teal-300">Register now</Link>
						</p>
					</div>
					<p className="mt-6 text-center text-xs text-zinc-400 dark:text-zinc-500">Your data is protected with secure authentication.</p>
				</div>
			</section>
		</main>
	);
};

export default LoginForm;
