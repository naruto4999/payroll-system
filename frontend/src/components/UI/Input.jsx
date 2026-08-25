import { forwardRef } from 'react';

const sizeClasses = {
	xs: 'h-7 px-2 text-xs',
	sm: 'h-8 px-2 text-sm',
	md: 'h-10 px-2.5 text-sm',
	lg: 'h-12 px-3 text-base',
};

const Input = forwardRef(
	(
		{
			field,
			form: _form,
			meta,
			size = 'md',
			invalid,
			className = '',
			wrapperClassName = '',
			startAdornment,
			endAdornment,
			...props
		},
		ref
	) => {
		const isInvalid = invalid ?? Boolean(meta?.touched && meta?.error);

		return (
			<div className={`group relative w-full ${wrapperClassName}`}>
				{startAdornment && <span className="pointer-events-none absolute inset-y-0 left-3 flex items-center text-zinc-400 transition-colors group-focus-within:text-teal-600">{startAdornment}</span>}
				<input
					ref={ref}
					{...field}
					{...props}
					aria-invalid={isInvalid || undefined}
					className={`w-full rounded border bg-white/70 text-zinc-900 outline-none transition-colors placeholder:text-zinc-500 focus:border-teal-600 focus:ring-1 focus:ring-teal-600 disabled:cursor-not-allowed disabled:opacity-60 dark:border-zinc-600 dark:bg-zinc-900/60 dark:text-zinc-100 dark:placeholder:text-zinc-500 ${startAdornment ? 'pl-9' : ''} ${endAdornment ? 'pr-9' : ''} ${isInvalid ? 'border-red-500 focus:border-red-500 focus:ring-red-500 dark:border-red-400' : 'border-zinc-400'} ${sizeClasses[size] || sizeClasses.md} ${className}`}
				/>
				{endAdornment && <span className="absolute inset-y-0 right-3 flex items-center text-zinc-400">{endAdornment}</span>}
			</div>
		);
	}
);

Input.displayName = 'Input';

export default Input;
