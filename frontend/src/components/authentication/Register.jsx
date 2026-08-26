import React, { useState } from 'react';
import { FiArrowRight, FiCheck, FiEye, FiEyeOff, FiLock, FiMail, FiPhone, FiUser } from 'react-icons/fi';
import { Formik } from 'formik';
import { Link } from 'react-router-dom';
import Button from '../UI/Button';
import Input from '../UI/Input';
import Modal from '../UI/Modal';
import { registerSchema } from './AuthSchema';
import OtpForm from './OtpForm';
import { useRegisterMutation, useSendOtpMutation } from './api/registerApiSlice';
import { getApiErrorMessage } from './api/errorUtils';

const FieldError = ({ error, touched }) =>
	(error && touched ? <p className="mt-1 text-xs leading-5 text-red-500 dark:text-red-400">{error}</p> : null);

const RegisterForm = () => {
	const [register, { isLoading, isError }] = useRegisterMutation();
	const [sendOtp, { isLoading: isLoadingOtp, isError: sendOtpError }] = useSendOtpMutation();
	const [msg, setMsg] = useState('');
	const [otpMsg, setOtpMsg] = useState('');
	const [otpFormPopover, setOtpFormPopover] = useState(false);
	const [otp, setOtp] = useState('');
	const [userDetails, setUserDetails] = useState(null);
	const [showPassword, setShowPassword] = useState(false);
	const [showConfirmPassword, setShowConfirmPassword] = useState(false);

	const submitButtonClicked = async (values) => {
		setMsg('');
		setOtpMsg('');
		try {
			const data = await register({
				email: values.email,
				password: values.password,
				username: values.username,
				phone_no: values.phone_no,
			}).unwrap();
			setUserDetails(values);
			setMsg(data.detail || 'Verification code sent.');
			setOtpFormPopover(true);
		} catch (err) {
			setMsg(getApiErrorMessage(err, 'Unable to create your account right now. Please try again.'));
		}
	};

	const submitOtpButtonCliked = async (e) => {
		e.preventDefault();
		setOtpMsg('');
		try {
			const data = await sendOtp({ ...userDetails, otp }).unwrap();
			setMsg(data.detail || 'Account created successfully.');
			setUserDetails(null);
			setOtpFormPopover(false);
		} catch (err) {
			setOtpMsg(getApiErrorMessage(err, 'That code is invalid. Please try again.'));
		}
	};

	const inputClass = 'h-11 rounded-lg border-zinc-700 bg-zinc-800 text-zinc-100 placeholder:text-zinc-500 focus:border-teal-500 focus:ring-4 focus:ring-teal-500/10';

	return (
		<main className="relative flex min-h-screen overflow-hidden bg-brand-light text-zinc-900 dark:bg-brand-canvas dark:text-white">
			<div className="pointer-events-none absolute -left-32 -top-32 h-80 w-80 rounded-full bg-teal-200/40 blur-3xl dark:bg-teal-900/30" />
			<div className="pointer-events-none absolute -bottom-40 right-0 h-96 w-96 rounded-full bg-blueAccent-100/60 blur-3xl dark:bg-blueAccent-900/20" />

			<section className="relative hidden w-[46%] flex-col justify-between overflow-hidden bg-brand-ink p-12 text-white lg:flex xl:p-16">
				<div className="absolute -right-24 top-16 h-72 w-72 rounded-full border-[36px] border-teal-400/10" />
				<div className="absolute -bottom-40 -left-32 h-96 w-96 rounded-full border-[52px] border-teal-300/10" />
				<Link to="/" className="relative z-10 inline-flex items-center">
					<img src={`${import.meta.env.VITE_PUBLIC_URL}logo_text_dark.svg`} alt="Payper" className="h-auto w-44 brightness-0 invert" />
				</Link>
				<div className="relative z-10 max-w-md pb-8">
					<p className="mb-5 text-sm font-medium uppercase tracking-[0.24em] text-teal-300">A better way to work</p>
					<h1 className="text-5xl font-semibold leading-[1.08] tracking-[-0.04em] xl:text-6xl">Bring your whole team into focus.</h1>
					<p className="mt-6 max-w-sm text-base leading-7 text-slate-300">Set up your payroll workspace once, then spend less time chasing details and more time growing your business.</p>
					<ul className="mt-9 space-y-4 text-sm text-slate-300">
						{['One secure workspace', 'Simple employee management', 'Payroll reports on demand'].map((item) => (
							<li key={item} className="flex items-center gap-3"><span className="flex h-6 w-6 items-center justify-center rounded-full bg-teal-400/15 text-teal-300"><FiCheck /></span>{item}</li>
						))}
					</ul>
				</div>
				<p className="relative z-10 text-xs text-slate-400">A Smart Payroll System on Cloud</p>
			</section>

			<section className="relative flex w-full items-center justify-center px-5 py-8 sm:px-8 lg:w-[54%] lg:px-12">
				<div className="w-full max-w-md">
					<div className="mb-7 flex justify-center lg:hidden">
						<Link to="/" className="inline-flex"><img src={`${import.meta.env.VITE_PUBLIC_URL}logo_text_dark.svg`} alt="Payper" className="h-auto w-36 brightness-0 invert" /></Link>
					</div>

					<div className="rounded-[2rem] border border-white/80 bg-white/75 p-6 shadow-brand-card backdrop-blur-xl dark:border-white/10 dark:bg-zinc-900/70 sm:p-8">
						<div className="mb-6">
							<p className="mb-2 text-xs font-semibold uppercase tracking-[0.2em] text-teal-700 dark:text-teal-400">Get started</p>
							<h2 className="text-3xl font-semibold tracking-tight text-zinc-900 dark:text-white">Create your account</h2>
							<p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">Your payroll workspace starts here.</p>
						</div>

						<Formik initialValues={{ email: '', password: '', passConfirm: '', username: '', phone_no: '' }} validationSchema={registerSchema} onSubmit={submitButtonClicked}>
							{({ handleSubmit, handleChange, handleBlur, values, errors, touched, isValid }) => (
								<form className="space-y-3.5" onSubmit={handleSubmit}>
									<div>
										<label htmlFor="username" className="mb-1.5 block text-xs font-medium text-zinc-700 dark:text-zinc-300">Username</label>
										<Input id="username" name="username" value={values.username} onChange={handleChange} onBlur={handleBlur} placeholder="Choose a username" autoComplete="username" size="sm" startAdornment={<FiUser />} className={inputClass} />
										<FieldError error={errors.username} touched={touched.username} />
									</div>
									<div>
										<label htmlFor="email" className="mb-1.5 block text-xs font-medium text-zinc-700 dark:text-zinc-300">Email address</label>
										<Input id="email" name="email" type="email" value={values.email} onChange={handleChange} onBlur={handleBlur} placeholder="you@company.com" autoComplete="email" size="sm" startAdornment={<FiMail />} className={inputClass} />
										<FieldError error={errors.email} touched={touched.email} />
									</div>
									<div>
										<label htmlFor="phone_no" className="mb-1.5 block text-xs font-medium text-zinc-700 dark:text-zinc-300">Phone number</label>
										<Input id="phone_no" name="phone_no" type="tel" value={values.phone_no} onChange={handleChange} onBlur={handleBlur} placeholder="10-digit phone number" autoComplete="tel" maxLength={10} size="sm" startAdornment={<FiPhone />} className={inputClass} />
										<FieldError error={errors.phone_no} touched={touched.phone_no} />
									</div>
									<div>
										<label htmlFor="password" className="mb-1.5 block text-xs font-medium text-zinc-700 dark:text-zinc-300">Password</label>
										<Input id="password" name="password" type={showPassword ? 'text' : 'password'} value={values.password} onChange={handleChange} onBlur={handleBlur} placeholder="Create a secure password" autoComplete="new-password" size="sm" startAdornment={<FiLock />} endAdornment={<button type="button" onClick={() => setShowPassword((visible) => !visible)} aria-label={showPassword ? 'Hide password' : 'Show password'} className="transition hover:text-zinc-200">{showPassword ? <FiEyeOff /> : <FiEye />}</button>} className={inputClass + ' pr-11'} />
										<FieldError error={errors.password} touched={touched.password} />
									</div>
									<div>
										<label htmlFor="passConfirm" className="mb-1.5 block text-xs font-medium text-zinc-700 dark:text-zinc-300">Confirm password</label>
										<Input id="passConfirm" name="passConfirm" type={showConfirmPassword ? 'text' : 'password'} value={values.passConfirm} onChange={handleChange} onBlur={handleBlur} placeholder="Repeat your password" autoComplete="new-password" size="sm" startAdornment={<FiLock />} endAdornment={<button type="button" onClick={() => setShowConfirmPassword((visible) => !visible)} aria-label={showConfirmPassword ? 'Hide password' : 'Show password'} className="transition hover:text-zinc-200">{showConfirmPassword ? <FiEyeOff /> : <FiEye />}</button>} className={inputClass + ' pr-11'} />
										<FieldError error={errors.passConfirm} touched={touched.passConfirm} />
									</div>

									{(msg || isError) && <p role="alert" className={`pt-1 text-xs leading-5 ${isError ? 'text-red-500 dark:text-red-400' : 'text-emerald-600 dark:text-emerald-400'}`}>{msg}</p>}
									<Button type="submit" disabled={!isValid || isLoading} className="group mt-2 h-12 w-full rounded-lg bg-teal-700 px-5 text-sm font-semibold text-white shadow-lg shadow-teal-700/20 transition hover:bg-teal-800 focus:outline-none focus:ring-4 focus:ring-teal-600/20 disabled:cursor-not-allowed disabled:opacity-50">
										{isLoading ? 'Creating account...' : 'Create account'} {!isLoading && <FiArrowRight className="transition-transform group-hover:translate-x-1" />}
									</Button>
								</form>
							)}
						</Formik>

						<p className="mt-6 text-center text-sm text-zinc-500 dark:text-zinc-400">Already have an account? <Link to="/login" className="font-semibold text-teal-700 hover:text-teal-900 dark:text-teal-400 dark:hover:text-teal-300">Sign in</Link></p>
					</div>
					<p className="mt-5 text-center text-xs text-zinc-400 dark:text-zinc-500">Your data is protected with secure authentication.</p>
				</div>
			</section>

			<Modal isOpen={otpFormPopover} onClose={() => setOtpFormPopover(false)} maxWidth="md" className="border border-white/10 bg-zinc-900 p-6 text-white">
				<OtpForm setOtpFormPopover={setOtpFormPopover} submitOtpButtonCliked={submitOtpButtonCliked} otpChangeHandler={(event) => setOtp(event.target.value)} otpMsg={otpMsg} sendOtpError={sendOtpError} isLoading={isLoadingOtp} />
			</Modal>
		</main>
	);
};

export default RegisterForm;
