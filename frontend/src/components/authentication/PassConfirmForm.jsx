import React, { useEffect, useState } from 'react';
import { FiArrowRight, FiEye, FiEyeOff, FiLock, FiShield } from 'react-icons/fi';
import { Formik } from 'formik';
import { useSelector } from 'react-redux';
import { Link, useNavigate, useParams } from 'react-router-dom';
import Input from '../UI/Input';
import { passConfirm } from './AuthSchema';
import { useConfirmPasswordMutation } from './api/confirmPassFormApiSlice';

const FieldError = ({ error, touched }) =>
	(error && touched ? <p className="mt-1 text-xs leading-5 text-red-500 dark:text-red-400">{error}</p> : null);

const PassConfirmForm = () => {
	const navigate = useNavigate();
	const auth = useSelector((state) => state.auth);
	const [confirmPassword, { isLoading, isSuccess, isError }] = useConfirmPasswordMutation();
	const { uid, token } = useParams();
	const [msg, setMsg] = useState('');
	const [showPassword, setShowPassword] = useState(false);
	const [showConfirmPassword, setShowConfirmPassword] = useState(false);

	useEffect(() => {
		if (auth.account != null) navigate('/home');
	}, [auth.account, navigate]);

	const submitButtonClicked = async (values, formikBag) => {
		setMsg('');
		try {
			const data = await confirmPassword({
				newPassword1: values.newPassword1,
				newPassword2: values.newPassword2,
				uidb64: uid,
				token,
			}).unwrap();
			setMsg(data.detail || 'Your password has been reset successfully.');
			formikBag.resetForm();
		} catch (err) {
			setMsg(err.data?.detail || 'This reset link is invalid or has expired.');
		}
	};

	const inputClass = 'h-11 rounded-lg border-zinc-700 bg-zinc-800 text-zinc-100 placeholder:text-zinc-500 focus:border-teal-500 focus:ring-4 focus:ring-teal-500/10';

	return (
		<main className="relative flex min-h-screen overflow-hidden bg-[#f5f8f7] text-zinc-900 dark:bg-[#101817] dark:text-white">
			<div className="pointer-events-none absolute -left-32 -top-32 h-80 w-80 rounded-full bg-teal-200/40 blur-3xl dark:bg-teal-900/30" />
			<div className="pointer-events-none absolute -bottom-40 right-0 h-96 w-96 rounded-full bg-blueAccent-100/60 blur-3xl dark:bg-blueAccent-900/20" />

			<section className="relative hidden w-[46%] flex-col justify-between overflow-hidden bg-[#102c2b] p-12 text-white lg:flex xl:p-16">
				<div className="absolute -right-24 top-16 h-72 w-72 rounded-full border-[36px] border-teal-400/10" />
				<div className="absolute -bottom-40 -left-32 h-96 w-96 rounded-full border-[52px] border-teal-300/10" />
				<Link to="/" className="relative z-10 inline-flex"><img src={`${import.meta.env.VITE_PUBLIC_URL}logo_text_dark.svg`} alt="Payper" className="h-auto w-44 brightness-0 invert" /></Link>
				<div className="relative z-10 max-w-md pb-8"><p className="mb-5 text-sm font-medium uppercase tracking-[0.24em] text-teal-300">Secure reset</p><h1 className="text-5xl font-semibold leading-[1.08] tracking-[-0.04em] xl:text-6xl">A fresh start for your account.</h1><p className="mt-6 max-w-sm text-base leading-7 text-slate-300">Choose a strong password and get back to the work that matters.</p><div className="mt-10 flex items-center gap-3 text-sm text-slate-300"><span className="flex h-9 w-9 items-center justify-center rounded-full bg-white/10 text-teal-300"><FiShield /></span>Secure, private account recovery</div></div>
				<p className="relative z-10 text-xs text-slate-400">A Smart Payroll System on Cloud</p>
			</section>

			<section className="relative flex w-full items-center justify-center px-5 py-10 sm:px-8 lg:w-[54%] lg:px-12">
				<div className="w-full max-w-md">
					<div className="mb-8 flex justify-center lg:hidden"><Link to="/" className="inline-flex"><img src={`${import.meta.env.VITE_PUBLIC_URL}logo_text_dark.svg`} alt="Payper" className="h-auto w-36 brightness-0 invert" /></Link></div>
					<div className="rounded-[2rem] border border-white/80 bg-white/75 p-6 shadow-[0_24px_80px_-32px_rgba(16,44,43,0.45)] backdrop-blur-xl dark:border-white/10 dark:bg-zinc-900/70 sm:p-10">
						<div className="mb-8"><p className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-teal-700 dark:text-teal-400">Almost done</p><h2 className="text-3xl font-semibold tracking-tight text-zinc-900 dark:text-white">Set a new password</h2><p className="mt-2 text-sm leading-6 text-zinc-500 dark:text-zinc-400">Use at least 8 characters, including a number and a special symbol.</p></div>
						<Formik initialValues={{ newPassword1: '', newPassword2: '' }} validationSchema={passConfirm} onSubmit={submitButtonClicked}>
							{({ handleSubmit, handleChange, handleBlur, values, errors, touched, isValid }) => (
								<form className="space-y-4" onSubmit={handleSubmit}>
									<div><label htmlFor="newPassword1" className="mb-1.5 block text-xs font-medium text-zinc-700 dark:text-zinc-300">New password</label><Input id="newPassword1" name="newPassword1" type={showPassword ? 'text' : 'password'} value={values.newPassword1} onChange={handleChange} onBlur={handleBlur} placeholder="Create a new password" autoComplete="new-password" size="sm" startAdornment={<FiLock />} endAdornment={<button type="button" onClick={() => setShowPassword((visible) => !visible)} aria-label={showPassword ? 'Hide password' : 'Show password'} className="transition hover:text-zinc-200">{showPassword ? <FiEyeOff /> : <FiEye />}</button>} className={inputClass + ' pr-11'} /><FieldError error={errors.newPassword1} touched={touched.newPassword1} /></div>
									<div><label htmlFor="newPassword2" className="mb-1.5 block text-xs font-medium text-zinc-700 dark:text-zinc-300">Confirm new password</label><Input id="newPassword2" name="newPassword2" type={showConfirmPassword ? 'text' : 'password'} value={values.newPassword2} onChange={handleChange} onBlur={handleBlur} placeholder="Repeat your new password" autoComplete="new-password" size="sm" startAdornment={<FiLock />} endAdornment={<button type="button" onClick={() => setShowConfirmPassword((visible) => !visible)} aria-label={showConfirmPassword ? 'Hide password' : 'Show password'} className="transition hover:text-zinc-200">{showConfirmPassword ? <FiEyeOff /> : <FiEye />}</button>} className={inputClass + ' pr-11'} /><FieldError error={errors.newPassword2} touched={touched.newPassword2} /></div>
									{msg && <p role={isError ? 'alert' : undefined} className={`pt-1 text-xs leading-5 ${isError ? 'text-red-500 dark:text-red-400' : 'text-emerald-600 dark:text-emerald-400'}`}>{msg}</p>}
									<button type="submit" disabled={!isValid || isLoading} className="group mt-2 flex h-12 w-full items-center justify-center gap-2 rounded-lg bg-teal-700 px-5 text-sm font-semibold text-white shadow-lg shadow-teal-700/20 transition hover:bg-teal-800 focus:outline-none focus:ring-4 focus:ring-teal-600/20 disabled:cursor-not-allowed disabled:opacity-60">{isLoading ? 'Resetting password...' : 'Reset password'} {!isLoading && <FiArrowRight className="transition-transform group-hover:translate-x-1" />}</button>
								</form>
							)}
						</Formik>
						{isSuccess && <div className="mt-6 text-center"><Link to="/login" className="text-sm font-semibold text-teal-700 hover:text-teal-900 dark:text-teal-400 dark:hover:text-teal-300">Return to sign in</Link></div>}
					</div>
					<p className="mt-6 text-center text-xs text-zinc-400 dark:text-zinc-500">Your data is protected with secure authentication.</p>
				</div>
			</section>
		</main>
	);
};

export default PassConfirmForm;
