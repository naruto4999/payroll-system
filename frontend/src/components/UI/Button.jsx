import { forwardRef } from 'react';

const variantClasses = {
	primary: 'bg-teal-600 text-white hover:bg-teal-700 dark:bg-teal-700 dark:hover:bg-teal-600',
	secondary:
		'bg-zinc-300 text-zinc-900 hover:bg-zinc-400 dark:bg-zinc-700 dark:text-zinc-100 dark:hover:bg-zinc-600',
	accent: 'bg-blueAccent-600 text-white hover:bg-blueAccent-700',
	success: 'bg-emerald-600 text-white hover:bg-emerald-700 dark:bg-emerald-700 dark:hover:bg-emerald-600',
	danger: 'bg-red-600 text-white hover:bg-red-700 dark:bg-red-700 dark:hover:bg-red-600',
	warning: 'bg-amber-500 text-white hover:bg-amber-600 dark:bg-amber-600 dark:hover:bg-amber-500',
	ghost: 'text-zinc-700 hover:bg-zinc-200 dark:text-zinc-200 dark:hover:bg-zinc-700',
};

const sizeClasses = {
	xxs: 'px-1.5 py-0.5 text-[0.65rem]',
	xs: 'px-2 py-1 text-xs',
	sm: 'px-3 py-1.5 text-sm',
	md: 'px-4 py-2 text-base',
	lg: 'px-5 py-2.5 text-lg',
	xl: 'px-6 py-3 text-xl',
};

const Button = forwardRef(
	({ variant = 'primary', size = 'md', className = '', type = 'button', children, ...props }, ref) => (
		<button
			ref={ref}
			type={type}
			className={`inline-flex items-center justify-center gap-2 rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 dark:focus-visible:ring-offset-zinc-800 ${variantClasses[variant] || variantClasses.primary} ${sizeClasses[size] || sizeClasses.md} ${className}`}
			{...props}
		>
			{children}
		</button>
	)
);

Button.displayName = 'Button';

export default Button;
