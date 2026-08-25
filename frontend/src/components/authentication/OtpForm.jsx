import { useEffect, useRef } from 'react';
import { FiArrowRight, FiKey } from 'react-icons/fi';
import Button from '../UI/Button';
import Input from '../UI/Input';

const OtpForm = ({ submitOtpButtonCliked, otpChangeHandler, setOtpFormPopover, otpMsg, sendOtpError, isLoading }) => {
	const inputRef = useRef(null);

	useEffect(() => {
		inputRef.current?.focus();
	}, []);

	return (
		<div>
			<p className="mb-2 text-xs font-semibold uppercase tracking-[0.2em] text-teal-400">Almost there</p>
			<h2 className="text-2xl font-semibold tracking-tight">Verify your email</h2>
			<p className="mt-2 text-sm leading-6 text-zinc-400">Enter the one-time code sent to your email address to finish creating your account.</p>

			<form className="mt-6 space-y-4" onSubmit={submitOtpButtonCliked}>
				<label htmlFor="otp" className="block text-xs font-medium text-zinc-300">Verification code</label>
				<Input ref={inputRef} id="otp" name="otp" type="text" inputMode="numeric" pattern="[0-9]*" onChange={otpChangeHandler} placeholder="Enter your code" autoComplete="one-time-code" startAdornment={<FiKey />} className="h-11 rounded-lg border-zinc-700 bg-zinc-800 text-zinc-100 placeholder:text-zinc-500 focus:border-teal-500 focus:ring-4 focus:ring-teal-500/10" />
				{sendOtpError && <p role="alert" className="text-xs leading-5 text-red-400">{otpMsg}</p>}
				<div className="flex gap-3 pt-2">
					<Button type="submit" disabled={isLoading} className="group h-11 flex-1 rounded-lg bg-teal-700 px-4 text-sm font-semibold text-white transition hover:bg-teal-800 disabled:cursor-not-allowed disabled:opacity-60">
						{isLoading ? 'Verifying...' : 'Verify code'} {!isLoading && <FiArrowRight className="transition-transform group-hover:translate-x-1" />}
					</Button>
					<Button type="button" variant="ghost" onClick={() => setOtpFormPopover(false)} className="h-11 rounded-lg border border-zinc-700 px-4 text-sm font-medium text-zinc-300 transition hover:border-zinc-500 hover:text-white">Cancel</Button>
				</div>
			</form>
		</div>
	);
};

export default OtpForm;
