const variantClasses = {
	primary:
		'group-hover:border-teal-500 peer-checked:border-teal-600 peer-checked:bg-teal-600 dark:group-hover:border-teal-500 dark:peer-checked:border-teal-500 dark:peer-checked:bg-teal-700',
	secondary:
		'group-hover:border-zinc-500 peer-checked:border-zinc-600 peer-checked:bg-zinc-600 dark:group-hover:border-zinc-400 dark:peer-checked:border-zinc-500 dark:peer-checked:bg-zinc-500',
	accent:
		'group-hover:border-blueAccent-500 peer-checked:border-blueAccent-600 peer-checked:bg-blueAccent-600 dark:group-hover:border-blueAccent-400 dark:peer-checked:border-blueAccent-600 dark:peer-checked:bg-blueAccent-600',
	success:
		'group-hover:border-emerald-500 peer-checked:border-emerald-600 peer-checked:bg-emerald-600 dark:group-hover:border-emerald-500 dark:peer-checked:border-emerald-700 dark:peer-checked:bg-emerald-700',
	danger:
		'group-hover:border-red-500 peer-checked:border-red-600 peer-checked:bg-red-600 dark:group-hover:border-red-500 dark:peer-checked:border-red-700 dark:peer-checked:bg-red-700',
	warning:
		'group-hover:border-amber-500 peer-checked:border-amber-500 peer-checked:bg-amber-500 dark:group-hover:border-amber-400 dark:peer-checked:border-amber-600 dark:peer-checked:bg-amber-600',
	ghost:
		'group-hover:border-zinc-500 peer-checked:border-zinc-600 peer-checked:bg-zinc-600 dark:group-hover:border-zinc-400 dark:peer-checked:border-zinc-500 dark:peer-checked:bg-zinc-500',
};

const Checkbox = ({
	name,
	value,
	checked,
	onChange,
	onBlur,
	disabled = false,
	id,
	'aria-label': ariaLabel,
	children,
	variant = 'primary',
	className = '',
}) => (
	<label
		className={`group inline-flex items-center gap-3 ${
			disabled ? 'cursor-not-allowed opacity-60' : 'cursor-pointer'
		} ${className}`}
	>
		<input
			id={id}
			name={name}
			value={value}
			type="checkbox"
			checked={checked}
			onChange={onChange}
			onBlur={onBlur}
			disabled={disabled}
			aria-label={ariaLabel}
			className="peer sr-only"
		/>
		<span
			aria-hidden="true"
			className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-md border-2 border-zinc-300 bg-white text-white shadow-sm transition duration-200 peer-checked:shadow-md peer-checked:[&>svg]:scale-100 peer-checked:[&>svg]:opacity-100 peer-focus-visible:ring-4 peer-focus-visible:ring-blueAccent-100 peer-disabled:cursor-not-allowed dark:border-zinc-600 dark:bg-zinc-800 dark:peer-focus-visible:ring-blueAccent-900 ${variantClasses[variant] || variantClasses.primary}`}
		>
			<svg
				viewBox="0 0 16 16"
				fill="none"
				className="h-3.5 w-3.5 scale-50 opacity-0 transition-all duration-200"
			>
				<path
					d="m3.25 8.25 3 3L12.75 4.75"
					stroke="currentColor"
					strokeWidth="2.4"
					strokeLinecap="round"
					strokeLinejoin="round"
				/>
			</svg>
		</span>
		{children && <span className="min-w-0">{children}</span>}
	</label>
);

export default Checkbox;
