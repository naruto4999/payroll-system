import React, { useEffect, useRef } from 'react';
import {
	FiActivity,
	FiArrowRight,
	FiArrowUpRight,
	FiBarChart2,
	FiCheck,
	FiChevronRight,
	FiClock,
	FiLayers,
	FiLock,
	FiPlay,
	FiShield,
	FiTrendingUp,
	FiUsers,
	FiZap,
} from 'react-icons/fi';
import { Link } from 'react-router-dom';

const features = [
	{
		icon: FiUsers,
		title: 'People, neatly organized',
		description: 'Keep employee profiles, salary structures, departments, and documents in one dependable record.',
		className: 'lg:col-span-2',
	},
	{
		icon: FiClock,
		title: 'Attendance that connects',
		description: 'Bring shifts, attendance, leave, and overtime together before payroll begins.',
		className: '',
	},
	{
		icon: FiZap,
		title: 'Faster salary preparation',
		description: 'Move from checked inputs to prepared salaries with fewer repetitive steps.',
		className: '',
	},
	{
		icon: FiBarChart2,
		title: 'Reports ready when you are',
		description:
			'Review payroll, attendance, employee strength, and statutory details from a clear reporting layer.',
		className: 'lg:col-span-2',
	},
];

const workflow = [
	{
		number: '01',
		title: 'Set up your workplace',
		description: 'Add your company structure, salary rules, shifts, and employee records once.',
	},
	{
		number: '02',
		title: 'Review the month',
		description: 'Check attendance, leave, overtime, earnings, and deductions in a connected flow.',
	},
	{
		number: '03',
		title: 'Prepare with confidence',
		description: 'Generate salaries and reports from the same source of truth your team maintains.',
	},
];

const LandingPage = () => {
	const pageRef = useRef(null);

	useEffect(() => {
		const page = pageRef.current;
		if (!page) return undefined;

		const revealItems = page.querySelectorAll('[data-reveal]');
		const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

		if (reduceMotion || !('IntersectionObserver' in window)) {
			revealItems.forEach((item) => item.setAttribute('data-visible', 'true'));
			return undefined;
		}

		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (!entry.isIntersecting) return;
					entry.target.setAttribute('data-visible', 'true');
					observer.unobserve(entry.target);
				});
			},
			{ threshold: 0.14, rootMargin: '0px 0px -40px' }
		);

		revealItems.forEach((item) => observer.observe(item));
		return () => observer.disconnect();
	}, []);

	return (
		<main ref={pageRef} className="landing-page relative min-h-screen overflow-hidden bg-[#101817] text-white">
			<div
				aria-hidden="true"
				className="landing-orb pointer-events-none absolute -left-40 -top-40 h-[32rem] w-[32rem] rounded-full bg-teal-900/40 blur-3xl"
			/>
			<div
				aria-hidden="true"
				className="landing-orb landing-orb-delayed pointer-events-none absolute right-[-12rem] top-[38rem] h-[34rem] w-[34rem] rounded-full bg-blueAccent-900/20 blur-3xl"
			/>
			<div
				aria-hidden="true"
				className="pointer-events-none absolute right-[42%] top-24 h-72 w-72 rounded-full border-[38px] border-teal-400/[0.07]"
			/>

			<nav
				aria-label="Main navigation"
				className="relative z-30 border-b border-white/[0.06] bg-[#101817]/80 backdrop-blur-xl"
			>
				<div className="mx-auto flex w-full max-w-7xl items-center justify-between px-6 py-5 sm:px-10 lg:px-16">
					<Link
						to="/"
						aria-label="Payper home"
						className="inline-flex rounded-md focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-300 focus-visible:ring-offset-4 focus-visible:ring-offset-[#101817]"
					>
						<img
							src={`${import.meta.env.VITE_PUBLIC_URL}logo_text_dark.svg`}
							alt="Payper"
							className="h-auto w-36 brightness-0 invert sm:w-40"
						/>
					</Link>
					<div className="hidden items-center gap-8 text-sm text-slate-300 md:flex">
						<a
							href="#features"
							className="transition hover:text-white focus:outline-none focus-visible:text-teal-300"
						>
							Features
						</a>
						<a
							href="#workflow"
							className="transition hover:text-white focus:outline-none focus-visible:text-teal-300"
						>
							How it works
						</a>
						<a
							href="#security"
							className="transition hover:text-white focus:outline-none focus-visible:text-teal-300"
						>
							Security
						</a>
					</div>
					<div className="flex items-center gap-3 text-sm sm:gap-5">
						<Link
							to="/login"
							className="font-medium text-slate-300 transition hover:text-white focus:outline-none focus-visible:text-teal-300"
						>
							Sign in
						</Link>
						<Link
							to="/register"
							className="border-white/15 rounded-lg border px-3 py-2 font-semibold text-white transition hover:border-teal-300/50 hover:bg-white/5 focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-300 sm:px-4"
						>
							Create account
						</Link>
					</div>
				</div>
			</nav>

			<section className="relative z-10 mx-auto grid min-h-[calc(100vh-81px)] w-full max-w-7xl items-center gap-14 px-6 pb-20 pt-14 sm:px-10 lg:grid-cols-[0.9fr_1.1fr] lg:gap-20 lg:px-16 lg:pb-28 lg:pt-10">
				<div className="max-w-xl">
					<div className="landing-hero-item mb-7 inline-flex items-center gap-2 rounded-full border border-teal-300/20 bg-teal-300/5 px-3 py-1.5 text-xs font-medium text-teal-200">
						<span className="h-1.5 w-1.5 rounded-full bg-teal-300 shadow-[0_0_12px_4px_rgba(94,234,212,0.35)]" />
						Payroll, simplified
					</div>
					<h1 className="landing-hero-item landing-hero-delay-1 text-5xl font-semibold leading-[1.04] tracking-[-0.05em] sm:text-6xl lg:text-7xl">
						The calm way to <span className="text-teal-300">run payroll.</span>
					</h1>
					<p className="landing-hero-item landing-hero-delay-2 mt-7 max-w-lg text-base leading-7 text-slate-300 sm:text-lg">
						Manage your people, prepare accurate salaries, and keep every payroll detail in one clear
						workspace.
					</p>
					<div className="landing-hero-item landing-hero-delay-3 mt-9 flex flex-col gap-3 sm:flex-row">
						<Link
							to="/register"
							className="group inline-flex h-12 items-center justify-center gap-2 rounded-lg bg-teal-600 px-5 text-sm font-semibold text-white shadow-lg shadow-teal-700/20 transition hover:-translate-y-0.5 hover:bg-teal-500 focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-300 focus-visible:ring-offset-4 focus-visible:ring-offset-[#101817]"
						>
							Register to get started{' '}
							<FiArrowRight
								aria-hidden="true"
								className="transition-transform group-hover:translate-x-1"
							/>
						</Link>
						<Link
							to="/login"
							className="border-white/15 inline-flex h-12 items-center justify-center gap-2 rounded-lg border px-5 text-sm font-semibold text-slate-200 transition hover:border-white/30 hover:bg-white/5 focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-300"
						>
							<FiPlay aria-hidden="true" className="text-teal-300" /> Sign in to workspace
						</Link>
					</div>
					<div className="landing-hero-item landing-hero-delay-4 mt-10 flex flex-wrap gap-x-6 gap-y-3 text-xs text-slate-400">
						<span className="flex items-center gap-2">
							<FiCheck aria-hidden="true" className="text-teal-300" /> Built for modern teams
						</span>
						<span className="flex items-center gap-2">
							<FiLock aria-hidden="true" className="text-teal-300" /> Secure by design
						</span>
					</div>
				</div>

				<div className="landing-hero-item landing-hero-delay-2 relative mx-auto w-full max-w-xl lg:ml-auto">
					<div aria-hidden="true" className="absolute -inset-5 rounded-[2rem] bg-teal-400/10 blur-2xl" />
					<div className="landing-dashboard relative rounded-[1.5rem] border border-white/10 bg-white/[0.06] p-3 shadow-2xl shadow-black/30 backdrop-blur-xl sm:p-4">
						<div className="overflow-hidden rounded-xl border border-white/10 bg-[#182321]">
							<div className="flex items-center justify-between border-b border-white/10 px-4 py-3 sm:px-5">
								<div className="flex items-center gap-2">
									<span className="h-2 w-2 rounded-full bg-teal-300" />
									<span className="text-xs font-medium text-slate-300">Payroll overview</span>
								</div>
								<span className="rounded-md bg-teal-300/10 px-2 py-1 text-[10px] text-teal-300">
									This month
								</span>
							</div>
							<div className="grid gap-3 p-4 sm:grid-cols-2 sm:p-5">
								<div className="rounded-xl border border-white/10 bg-white/[0.04] p-4 sm:col-span-2">
									<div className="flex items-start justify-between">
										<div>
											<p className="text-xs text-slate-400">Total payroll</p>
											<p className="mt-2 text-2xl font-semibold tracking-tight">INR 4,82,600</p>
										</div>
										<span className="flex h-9 w-9 items-center justify-center rounded-lg bg-teal-300/10 text-teal-300">
											<FiTrendingUp aria-hidden="true" />
										</span>
									</div>
									<div className="mt-5 h-16 overflow-hidden">
										<svg
											viewBox="0 0 400 70"
											className="h-full w-full"
											preserveAspectRatio="none"
											aria-hidden="true"
										>
											<path
												className="landing-chart-line"
												d="M0 58 C35 52 40 61 74 44 S120 46 152 33 S208 42 240 22 S293 31 320 13 S364 22 400 4"
												fill="none"
												stroke="#5eead4"
												strokeWidth="3"
											/>
											<path
												d="M0 58 C35 52 40 61 74 44 S120 46 152 33 S208 42 240 22 S293 31 320 13 S364 22 400 4 V70 H0Z"
												fill="url(#payroll-area)"
												opacity=".3"
											/>
											<defs>
												<linearGradient id="payroll-area" x1="0" x2="0" y1="0" y2="1">
													<stop stopColor="#5eead4" />
													<stop offset="1" stopColor="#5eead4" stopOpacity="0" />
												</linearGradient>
											</defs>
										</svg>
									</div>
								</div>
								<div className="rounded-xl border border-white/10 bg-white/[0.04] p-4">
									<p className="text-xs text-slate-400">Employees</p>
									<p className="mt-2 text-xl font-semibold">124</p>
									<div className="mt-3 h-1.5 rounded-full bg-white/10">
										<div className="h-full w-3/4 rounded-full bg-blueAccent-400" />
									</div>
								</div>
								<div className="rounded-xl border border-white/10 bg-white/[0.04] p-4">
									<p className="text-xs text-slate-400">Next payday</p>
									<p className="mt-2 text-xl font-semibold">24 Jun</p>
									<p className="mt-3 text-xs text-teal-300">Ready to process</p>
								</div>
							</div>
						</div>
						<div className="flex items-center justify-between px-2 pt-3 text-[10px] text-slate-500">
							<span>One workspace for your whole team</span>
							<span>payper cloud</span>
						</div>
					</div>
					<div className="absolute -bottom-7 -left-4 hidden items-center gap-3 rounded-xl border border-white/10 bg-[#1b2927]/95 px-4 py-3 shadow-xl backdrop-blur sm:flex">
						<span className="flex h-9 w-9 items-center justify-center rounded-lg bg-teal-300/10 text-teal-300">
							<FiCheck aria-hidden="true" />
						</span>
						<div>
							<p className="text-xs font-medium">Payroll checked</p>
							<p className="mt-0.5 text-[10px] text-slate-400">All inputs are ready</p>
						</div>
					</div>
				</div>
			</section>

			<section
				aria-label="Payroll capabilities"
				className="relative z-10 border-y border-white/[0.06] bg-white/[0.02]"
			>
				<div
					data-reveal
					className="mx-auto grid max-w-7xl grid-cols-2 gap-y-8 px-6 py-9 sm:px-10 md:grid-cols-4 lg:px-16"
				>
					{[
						['Employee records', 'Connected'],
						['Attendance', 'In one flow'],
						['Salary preparation', 'Clear checks'],
						['Payroll reports', 'Ready to review'],
					].map(([label, value], index) => (
						<div key={label} className={`px-3 ${index > 0 ? 'md:border-l md:border-white/10' : ''}`}>
							<p className="text-sm font-semibold text-slate-100">{label}</p>
							<p className="mt-1 text-xs text-slate-500">{value}</p>
						</div>
					))}
				</div>
			</section>

			<section id="features" className="relative z-10 scroll-mt-20 px-6 py-24 sm:px-10 lg:px-16 lg:py-32">
				<div className="mx-auto max-w-7xl">
					<div data-reveal className="max-w-2xl">
						<p className="text-xs font-semibold uppercase tracking-[0.24em] text-teal-300">
							A clearer payroll cycle
						</p>
						<h2 className="mt-4 text-3xl font-semibold tracking-[-0.035em] sm:text-5xl">
							Everything important, without the noise.
						</h2>
						<p className="mt-5 max-w-xl leading-7 text-slate-400">
							Payper keeps the details connected, so your team can spend less time moving between
							spreadsheets and more time reviewing what matters.
						</p>
					</div>
					<div className="mt-14 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
						{features.map((feature, index) => {
							const Icon = feature.icon;
							return (
								<article
									key={feature.title}
									data-reveal
									data-delay={(index % 3) + 1}
									className={`group relative min-h-[16rem] overflow-hidden rounded-2xl border border-white/[0.08] bg-white/[0.035] p-6 transition duration-300 hover:-translate-y-1 hover:border-teal-300/20 hover:bg-white/[0.055] sm:p-8 ${feature.className}`}
								>
									<div
										aria-hidden="true"
										className="absolute -right-12 -top-12 h-36 w-36 rounded-full bg-teal-400/[0.04] blur-2xl transition group-hover:bg-teal-400/[0.09]"
									/>
									<span className="relative flex h-11 w-11 items-center justify-center rounded-xl border border-teal-300/10 bg-teal-300/[0.08] text-lg text-teal-300">
										<Icon aria-hidden="true" />
									</span>
									<h3 className="relative mt-8 text-xl font-semibold tracking-tight">
										{feature.title}
									</h3>
									<p className="relative mt-3 max-w-md text-sm leading-6 text-slate-400">
										{feature.description}
									</p>
									<FiArrowUpRight
										aria-hidden="true"
										className="absolute bottom-7 right-7 text-slate-600 transition group-hover:-translate-y-0.5 group-hover:translate-x-0.5 group-hover:text-teal-300"
									/>
								</article>
							);
						})}
					</div>
				</div>
			</section>

			<section
				id="workflow"
				className="relative z-10 scroll-mt-20 border-y border-white/[0.06] bg-[#13201e] px-6 py-24 sm:px-10 lg:px-16 lg:py-32"
			>
				<div
					aria-hidden="true"
					className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_75%_40%,rgba(45,212,191,0.08),transparent_30%)]"
				/>
				<div className="relative mx-auto grid max-w-7xl gap-14 lg:grid-cols-[0.8fr_1.2fr] lg:gap-24">
					<div data-reveal>
						<p className="text-xs font-semibold uppercase tracking-[0.24em] text-teal-300">
							From setup to payday
						</p>
						<h2 className="mt-4 text-3xl font-semibold tracking-[-0.035em] sm:text-5xl">
							A workflow your team can follow.
						</h2>
						<p className="mt-5 max-w-md leading-7 text-slate-400">
							Move through payroll in a natural order, with every step building on the last.
						</p>
						<Link
							to="/register"
							className="group mt-8 inline-flex items-center gap-2 text-sm font-semibold text-teal-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-300"
						>
							Set up your workspace{' '}
							<FiArrowRight
								aria-hidden="true"
								className="transition-transform group-hover:translate-x-1"
							/>
						</Link>
					</div>
					<div className="relative">
						<div
							aria-hidden="true"
							className="absolute bottom-8 left-[1.45rem] top-8 w-px bg-gradient-to-b from-teal-300/50 via-teal-300/20 to-transparent"
						/>
						{workflow.map((step, index) => (
							<div
								key={step.number}
								data-reveal
								data-delay={index + 1}
								className="relative flex gap-5 pb-10 last:pb-0 sm:gap-7"
							>
								<span className="relative z-10 flex h-12 w-12 shrink-0 items-center justify-center rounded-full border border-teal-300/20 bg-[#172725] text-xs font-semibold text-teal-300 shadow-[0_0_0_7px_rgba(19,32,30,1)]">
									{step.number}
								</span>
								<div className="rounded-2xl border border-white/[0.08] bg-white/[0.035] p-5 sm:p-6">
									<h3 className="text-lg font-semibold">{step.title}</h3>
									<p className="mt-2 text-sm leading-6 text-slate-400">{step.description}</p>
								</div>
							</div>
						))}
					</div>
				</div>
			</section>

			<section id="security" className="relative z-10 scroll-mt-20 px-6 py-24 sm:px-10 lg:px-16 lg:py-32">
				<div
					data-reveal
					className="mx-auto grid max-w-7xl overflow-hidden rounded-3xl border border-white/10 bg-white/[0.04] shadow-2xl shadow-black/20 lg:grid-cols-[1.1fr_0.9fr]"
				>
					<div className="p-7 sm:p-10 lg:p-14">
						<span className="flex h-12 w-12 items-center justify-center rounded-xl bg-blueAccent-500/10 text-xl text-blueAccent-300">
							<FiShield aria-hidden="true" />
						</span>
						<p className="mt-8 text-xs font-semibold uppercase tracking-[0.24em] text-blueAccent-300">
							Control comes first
						</p>
						<h2 className="mt-4 max-w-xl text-3xl font-semibold tracking-[-0.035em] sm:text-4xl">
							Payroll access that stays in the right hands.
						</h2>
						<p className="mt-5 max-w-xl leading-7 text-slate-400">
							Keep company data organized behind authenticated access, with separate controls for the
							people responsible for setup and payroll operations.
						</p>
					</div>
					<div className="grid border-t border-white/10 bg-[#182321] p-7 sm:grid-cols-2 sm:p-10 lg:grid-cols-1 lg:border-l lg:border-t-0">
						{[
							[FiLock, 'Protected workspace', 'Your payroll tools sit behind secure account access.'],
							[
								FiLayers,
								'Clear responsibilities',
								'Administrative and payroll workflows remain intentionally separated.',
							],
							[
								FiActivity,
								'One source of truth',
								'Connected records reduce duplicate updates across the payroll cycle.',
							],
						].map(([Icon, title, description]) => (
							<div
								key={title}
								className="flex gap-4 border-white/10 py-5 first:pt-0 last:pb-0 sm:px-4 sm:first:pl-0 lg:border-b lg:px-0 lg:last:border-b-0"
							>
								<Icon aria-hidden="true" className="mt-1 shrink-0 text-teal-300" />
								<div>
									<h3 className="text-sm font-semibold">{title}</h3>
									<p className="mt-1 text-xs leading-5 text-slate-400">{description}</p>
								</div>
							</div>
						))}
					</div>
				</div>
			</section>

			<section className="relative z-10 px-6 pb-24 sm:px-10 lg:px-16 lg:pb-32">
				<div
					data-reveal
					className="shadow-teal-950/30 relative mx-auto max-w-7xl overflow-hidden rounded-3xl bg-teal-600 px-7 py-14 text-center shadow-2xl sm:px-12 sm:py-16"
				>
					<div
						aria-hidden="true"
						className="absolute -left-20 -top-32 h-72 w-72 rounded-full border-[45px] border-white/[0.06]"
					/>
					<div
						aria-hidden="true"
						className="absolute -bottom-40 -right-20 h-80 w-80 rounded-full bg-[#101817]/20 blur-2xl"
					/>
					<div className="relative mx-auto max-w-2xl">
						<p className="text-xs font-semibold uppercase tracking-[0.24em] text-teal-100">
							A calmer payroll starts here
						</p>
						<h2 className="mt-4 text-3xl font-semibold tracking-[-0.035em] sm:text-5xl">
							Give your payroll process one clear home.
						</h2>
						<p className="mx-auto mt-5 max-w-xl leading-7 text-teal-50/80">
							Create your workspace and bring people, attendance, salaries, and reports into one connected
							flow.
						</p>
						<Link
							to="/register"
							className="group mt-8 inline-flex h-12 items-center justify-center gap-2 rounded-lg bg-white px-6 text-sm font-semibold text-[#102c2b] shadow-lg transition hover:-translate-y-0.5 hover:bg-teal-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-4 focus-visible:ring-offset-teal-600"
						>
							Create your account{' '}
							<FiChevronRight
								aria-hidden="true"
								className="transition-transform group-hover:translate-x-1"
							/>
						</Link>
					</div>
				</div>
			</section>

			<footer className="relative z-10 border-t border-white/[0.07] px-6 py-9 sm:px-10 lg:px-16">
				<div className="mx-auto flex max-w-7xl flex-col gap-6 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between">
					<Link
						to="/"
						aria-label="Payper home"
						className="w-fit rounded-md focus:outline-none focus-visible:ring-2 focus-visible:ring-teal-300"
					>
						<img
							src={`${import.meta.env.VITE_PUBLIC_URL}logo_text_dark.svg`}
							alt="Payper"
							className="h-auto w-28 opacity-80 brightness-0 invert"
						/>
					</Link>
					<p>Payroll made clear for growing teams.</p>
					<div className="flex gap-5">
						<Link to="/login" className="transition hover:text-white">
							Sign in
						</Link>
						<Link to="/register" className="transition hover:text-white">
							Create account
						</Link>
					</div>
				</div>
			</footer>
		</main>
	);
};

export default LandingPage;
