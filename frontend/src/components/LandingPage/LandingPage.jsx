import React from 'react';
import { FiArrowRight, FiCheck, FiLock, FiPlay, FiTrendingUp } from 'react-icons/fi';
import { Link } from 'react-router-dom';

const LandingPage = () => {
	return (
		<main className="relative min-h-screen overflow-hidden bg-[#101817] text-white">
			<div className="pointer-events-none absolute -left-40 -top-40 h-[32rem] w-[32rem] rounded-full bg-teal-900/40 blur-3xl" />
			<div className="pointer-events-none absolute -bottom-56 right-0 h-[34rem] w-[34rem] rounded-full bg-blueAccent-900/20 blur-3xl" />
			<div className="pointer-events-none absolute right-[42%] top-24 h-72 w-72 rounded-full border-[38px] border-teal-400/10" />

			<nav className="relative z-10 mx-auto flex w-full max-w-7xl items-center justify-between px-6 py-6 sm:px-10 lg:px-16">
				<Link to="/" className="inline-flex items-center">
					<img src={`${import.meta.env.VITE_PUBLIC_URL}logo_text_dark.svg`} alt="Payper" className="h-auto w-36 brightness-0 invert sm:w-40" />
				</Link>
				<div className="flex items-center gap-5 text-sm">
					<Link to="/login" className="font-medium text-slate-300 transition hover:text-white">Sign in</Link>
					<Link to="/register" className="rounded-lg border border-white/15 px-4 py-2 font-semibold text-white transition hover:border-teal-300/50 hover:bg-white/5">Create account</Link>
				</div>
			</nav>

			<section className="relative z-10 mx-auto grid min-h-[calc(100vh-88px)] w-full max-w-7xl items-center gap-14 px-6 pb-16 pt-8 sm:px-10 lg:grid-cols-[0.9fr_1.1fr] lg:gap-20 lg:px-16 lg:pb-24 lg:pt-0">
				<div className="max-w-xl">
					<div className="mb-7 inline-flex items-center gap-2 rounded-full border border-teal-300/20 bg-teal-300/5 px-3 py-1.5 text-xs font-medium text-teal-200">
						<span className="h-1.5 w-1.5 rounded-full bg-teal-300 shadow-[0_0_12px_4px_rgba(94,234,212,0.35)]" />
						Payroll, simplified
					</div>
					<h1 className="text-5xl font-semibold leading-[1.04] tracking-[-0.05em] sm:text-6xl lg:text-7xl">The calm way to run payroll.</h1>
					<p className="mt-7 max-w-lg text-base leading-7 text-slate-300 sm:text-lg">Manage your people, generate accurate salaries, and keep every payroll detail in one clear workspace.</p>
					<div className="mt-9 flex flex-col gap-3 sm:flex-row">
						<Link to="/register" className="group inline-flex h-12 items-center justify-center gap-2 rounded-lg bg-teal-600 px-5 text-sm font-semibold text-white shadow-lg shadow-teal-700/20 transition hover:bg-teal-500">Start for free <FiArrowRight className="transition-transform group-hover:translate-x-1" /></Link>
						<Link to="/login" className="inline-flex h-12 items-center justify-center gap-2 rounded-lg border border-white/15 px-5 text-sm font-semibold text-slate-200 transition hover:border-white/30 hover:bg-white/5"><FiPlay className="text-teal-300" /> Sign in to workspace</Link>
					</div>
					<div className="mt-10 flex flex-wrap gap-x-6 gap-y-3 text-xs text-slate-400">
						<span className="flex items-center gap-2"><FiCheck className="text-teal-300" /> Built for modern teams</span>
						<span className="flex items-center gap-2"><FiLock className="text-teal-300" /> Secure by design</span>
					</div>
				</div>

				<div className="relative mx-auto w-full max-w-xl lg:ml-auto">
					<div className="absolute -inset-5 rounded-[2rem] bg-teal-400/10 blur-2xl" />
					<div className="relative rounded-[1.5rem] border border-white/10 bg-white/[0.06] p-3 shadow-2xl backdrop-blur-xl sm:p-4">
						<div className="overflow-hidden rounded-xl border border-white/10 bg-[#182321]">
							<div className="flex items-center justify-between border-b border-white/10 px-4 py-3 sm:px-5">
								<div className="flex items-center gap-2"><span className="h-2 w-2 rounded-full bg-teal-300" /><span className="text-xs font-medium text-slate-300">Payroll overview</span></div>
								<span className="rounded-md bg-teal-300/10 px-2 py-1 text-[10px] text-teal-300">This month</span>
							</div>
							<div className="grid gap-3 p-4 sm:grid-cols-2 sm:p-5">
								<div className="rounded-xl border border-white/10 bg-white/[0.04] p-4 sm:col-span-2"><div className="flex items-start justify-between"><div><p className="text-xs text-slate-400">Total payroll</p><p className="mt-2 text-2xl font-semibold tracking-tight">$48,260.00</p></div><span className="flex h-9 w-9 items-center justify-center rounded-lg bg-teal-300/10 text-teal-300"><FiTrendingUp /></span></div><div className="mt-5 h-16 overflow-hidden"><svg viewBox="0 0 400 70" className="h-full w-full" preserveAspectRatio="none"><path d="M0 58 C35 52 40 61 74 44 S120 46 152 33 S208 42 240 22 S293 31 320 13 S364 22 400 4" fill="none" stroke="#5eead4" strokeWidth="3" /><path d="M0 58 C35 52 40 61 74 44 S120 46 152 33 S208 42 240 22 S293 31 320 13 S364 22 400 4 V70 H0Z" fill="url(#area)" opacity=".3" /><defs><linearGradient id="area" x1="0" x2="0" y1="0" y2="1"><stop stopColor="#5eead4" /><stop offset="1" stopColor="#5eead4" stopOpacity="0" /></linearGradient></defs></svg></div></div>
								<div className="rounded-xl border border-white/10 bg-white/[0.04] p-4"><p className="text-xs text-slate-400">Employees</p><p className="mt-2 text-xl font-semibold">124</p><div className="mt-3 h-1.5 rounded-full bg-white/10"><div className="h-full w-3/4 rounded-full bg-blueAccent-400" /></div></div>
								<div className="rounded-xl border border-white/10 bg-white/[0.04] p-4"><p className="text-xs text-slate-400">Next payday</p><p className="mt-2 text-xl font-semibold">24 Jun</p><p className="mt-3 text-xs text-teal-300">Ready to process</p></div>
							</div>
						</div>
						<div className="flex items-center justify-between px-2 pt-3 text-[10px] text-slate-500"><span>One workspace for your whole team</span><span>payper cloud</span></div>
					</div>
				</div>
			</section>
		</main>
	);
};

export default LandingPage;
