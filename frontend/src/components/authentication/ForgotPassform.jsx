import React, { useEffect, useState } from 'react';
import { FiArrowRight, FiMail, FiShield } from 'react-icons/fi';
import { useSelector } from 'react-redux';
import { Link, useNavigate } from 'react-router-dom';
import Button from '../UI/Button';
import Input from '../UI/Input';
import { useForgotPasswordMutation } from './api/forgotPassFormApiSlice';

const ForgotPassform = () => {
	const navigate = useNavigate();
	const auth = useSelector((state) => state.auth);
	const [forgotPassword, { isLoading, isSuccess, isError }] = useForgotPasswordMutation();
	const [username, setUsername] = useState('');
	const [msg, setMsg] = useState('');
	const frontend_url = `${import.meta.env.VITE_FRONTEND_URL}`;

	useEffect(() => {
		if (auth.account != null) navigate('/home');
	}, [auth.account, navigate]);

	const submitButtonClicked = async (e) => {
		e.preventDefault();
		setMsg('');
		try {
			const data = await forgotPassword({ username, frontend_url }).unwrap();
			setMsg(data.detail || 'If an account exists, a reset link is on its way.');
			setUsername('');
		} catch (err) {
			setMsg(err.data?.username || err.data?.detail || 'Unable to send the reset email. Please try again.');
		}
	};

	return (
		<main className="relative flex min-h-screen overflow-hidden bg-brand-light text-zinc-900 dark:bg-brand-canvas dark:text-white">
			<div className="pointer-events-none absolute -left-32 -top-32 h-80 w-80 rounded-full bg-teal-200/40 blur-3xl dark:bg-teal-900/30" />
			<div className="pointer-events-none absolute -bottom-40 right-0 h-96 w-96 rounded-full bg-blueAccent-100/60 blur-3xl dark:bg-blueAccent-900/20" />

			<section className="relative hidden w-[46%] flex-col justify-between overflow-hidden bg-brand-ink p-12 text-white lg:flex xl:p-16">
				<div className="absolute -right-24 top-16 h-72 w-72 rounded-full border-[36px] border-teal-400/10" />
				<div className="absolute -bottom-40 -left-32 h-96 w-96 rounded-full border-[52px] border-teal-300/10" />
				<Link to="/" className="relative z-10 inline-flex"><img src={`${import.meta.env.VITE_PUBLIC_URL}logo_text_dark.svg`} alt="Payper" className="h-auto w-44 brightness-0 invert" /></Link>
				<div className="relative z-10 max-w-md pb-8">
					<p className="mb-5 text-sm font-medium uppercase tracking-[0.24em] text-teal-300">Account recovery</p>
					<h1 className="text-5xl font-semibold leading-[1.08] tracking-[-0.04em] xl:text-6xl">Back in control, in a few clicks.</h1>
					<p className="mt-6 max-w-sm text-base leading-7 text-slate-300">We’ll help you get back into your payroll workspace securely and without the hassle.</p>
					<div className="mt-10 flex items-center gap-3 text-sm text-slate-300"><span className="flex h-9 w-9 items-center justify-center rounded-full bg-white/10 text-teal-300"><FiShield /></span>Private, secure password recovery</div>
				</div>
				<p className="relative z-10 text-xs text-slate-400">A Smart Payroll System on Cloud</p>
			</section>

			<section className="relative flex w-full items-center justify-center px-5 py-10 sm:px-8 lg:w-[54%] lg:px-12">
				<div className="w-full max-w-md">
					<div className="mb-8 flex justify-center lg:hidden"><Link to="/" className="inline-flex"><img src={`${import.meta.env.VITE_PUBLIC_URL}logo_text_dark.svg`} alt="Payper" className="h-auto w-36 brightness-0 invert" /></Link></div>
					<div className="rounded-[2rem] border border-white/80 bg-white/75 p-6 shadow-brand-card backdrop-blur-xl dark:border-white/10 dark:bg-zinc-900/70 sm:p-10">
						<div className="mb-8"><p className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-teal-700 dark:text-teal-400">Forgot your password?</p><h2 className="text-3xl font-semibold tracking-tight text-zinc-900 dark:text-white">Reset your password</h2><p className="mt-2 text-sm leading-6 text-zinc-500 dark:text-zinc-400">Enter your username and we’ll send you a secure reset link.</p></div>
						<form className="space-y-4" onSubmit={submitButtonClicked}>
							<div><label htmlFor="username" className="mb-1.5 block text-xs font-medium text-zinc-700 dark:text-zinc-300">Username</label><Input id="username" name="username" type="text" value={username} onChange={(event) => setUsername(event.target.value)} placeholder="Enter your username" autoComplete="username" required size="sm" startAdornment={<FiMail />} className="h-11 rounded-lg border-zinc-700 bg-zinc-800 px-10 text-zinc-100 placeholder:text-zinc-500 focus:border-teal-500 focus:ring-4 focus:ring-teal-500/10" /></div>
							{msg && <p role={isError ? 'alert' : undefined} className={`pt-1 text-xs leading-5 ${isError ? 'text-red-500 dark:text-red-400' : 'text-emerald-600 dark:text-emerald-400'}`}>{msg}</p>}
							<Button type="submit" disabled={isLoading} className="group h-12 w-full rounded-lg bg-teal-700 px-5 text-sm font-semibold shadow-lg shadow-teal-700/20 transition hover:bg-teal-800 focus:outline-none focus:ring-4 focus:ring-teal-600/20 disabled:cursor-not-allowed disabled:opacity-60">{isLoading ? 'Sending reset link...' : 'Send reset link'} {!isLoading && <FiArrowRight className="transition-transform group-hover:translate-x-1" />}</Button>
						</form>
						{isSuccess && <p className="mt-5 text-center text-xs text-zinc-500 dark:text-zinc-400">Check your inbox and follow the link to continue.</p>}
						<div className="mt-7 flex justify-center gap-4 text-sm"><Link to="/login" className="font-semibold text-teal-700 hover:text-teal-900 dark:text-teal-400 dark:hover:text-teal-300">Back to sign in</Link><span className="text-zinc-300 dark:text-zinc-700">|</span><Link to="/register" className="text-zinc-500 hover:text-zinc-800 dark:text-zinc-400 dark:hover:text-zinc-200">Create account</Link></div>
					</div>
					<p className="mt-6 text-center text-xs text-zinc-400 dark:text-zinc-500">Your data is protected with secure authentication.</p>
				</div>
			</section>
		</main>
	);
};

export default ForgotPassform;
