import { Children, cloneElement, forwardRef, isValidElement, useCallback, useEffect, useId, useRef, useState } from 'react';
import { FaCheck, FaChevronDown } from 'react-icons/fa';

const sizeClasses = {
	xs: 'h-7 px-2.5 pr-8 text-xs',
	sm: 'h-8 px-3 pr-9 text-sm',
	md: 'h-10 px-3.5 pr-10 text-sm',
	lg: 'h-12 px-4 pr-11 text-base',
};

const Dropdown = forwardRef(
	(
		{
			size = 'md',
			invalid = false,
			className = '',
			wrapperClassName = '',
			children,
			value,
			onChange,
			disabled = false,
			name,
			onBlur,
			'aria-label': ariaLabel,
			...props
		},
		ref
	) => {
		const options = Children.toArray(children).filter(isValidElement);
		const selectedIndex = Math.max(
			0,
			options.findIndex((option) => String(option.props.value) === String(value))
		);
		const selectedOption = options[selectedIndex];
		const [isOpen, setIsOpen] = useState(false);
		const [highlightedIndex, setHighlightedIndex] = useState(selectedIndex);
		const wrapperRef = useRef(null);
		const listboxId = useId();
		const closeDropdown = useCallback(() => {
			setIsOpen(false);
			setHighlightedIndex(selectedIndex);
		}, [selectedIndex]);

		useEffect(() => {
			setHighlightedIndex(selectedIndex);
		}, [selectedIndex]);

		useEffect(() => {
			const handlePointerDown = (event) => {
				if (!wrapperRef.current?.contains(event.target)) {
					closeDropdown();
				}
			};

			document.addEventListener('mousedown', handlePointerDown);
			return () => document.removeEventListener('mousedown', handlePointerDown);
		}, [closeDropdown]);

		const selectOption = (option, index) => {
			if (option.props.disabled) return;

			setHighlightedIndex(index);
			setIsOpen(false);
			onChange?.({ target: { name, value: option.props.value } });
		};

		const handleKeyDown = (event) => {
			if (disabled) return;

			if (event.key === 'Enter' || event.key === ' ') {
				event.preventDefault();
				if (isOpen) {
					selectOption(options[highlightedIndex], highlightedIndex);
				} else {
					setIsOpen(true);
				}
				return;
			}

			if (event.key === 'Escape') {
				closeDropdown();
				return;
			}

			if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
				event.preventDefault();
				setIsOpen(true);
				const direction = event.key === 'ArrowDown' ? 1 : -1;
				let nextIndex = highlightedIndex;

				do {
					nextIndex = (nextIndex + direction + options.length) % options.length;
				} while (options[nextIndex]?.props.disabled && nextIndex !== highlightedIndex);

				setHighlightedIndex(nextIndex);
			}
		};

		return (
			<div ref={wrapperRef} className={`group relative inline-flex min-w-[11rem] ${wrapperClassName}`}>
				{isOpen && (
					<div
						className="fixed inset-0 z-40"
						aria-hidden="true"
						onMouseDown={closeDropdown}
					/>
				)}
				<input type="hidden" name={name} value={value ?? ''} {...(props.required ? { required: true } : {})} />
				<button
					ref={ref}
					type="button"
					role="combobox"
					aria-label={ariaLabel}
					aria-controls={listboxId}
					aria-expanded={isOpen}
					aria-haspopup="listbox"
					aria-invalid={invalid || undefined}
					disabled={disabled}
					onBlur={onBlur}
					onClick={() => {
						if (isOpen) {
							closeDropdown();
						} else {
							setHighlightedIndex(selectedIndex);
							setIsOpen(true);
						}
					}}
					onKeyDown={handleKeyDown}
					className={`relative z-50 flex w-full items-center rounded-lg border bg-white/90 font-medium text-zinc-800 shadow-sm outline-none transition-all hover:border-zinc-400 focus:border-teal-600 focus:ring-2 focus:ring-teal-600/20 disabled:cursor-not-allowed disabled:opacity-60 dark:bg-zinc-800 dark:text-zinc-100 dark:hover:border-zinc-500 dark:focus:border-teal-500 dark:focus:ring-teal-500/20 ${invalid ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20 dark:border-red-400' : 'border-zinc-300 dark:border-zinc-600'} ${sizeClasses[size] || sizeClasses.md} ${className}`}
					{...props}
				>
					<span className="truncate">{selectedOption?.props.children}</span>
					<FaChevronDown className={`absolute right-3 h-3 w-3 text-zinc-400 transition-transform dark:text-zinc-500 ${isOpen ? 'rotate-180 text-teal-600 dark:text-teal-400' : ''}`} />
				</button>

				{isOpen && (
					<div
						id={listboxId}
						role="listbox"
						aria-label={ariaLabel}
						className="absolute left-0 right-0 top-[calc(100%+0.4rem)] z-50 max-h-60 overflow-x-hidden overflow-y-auto rounded-xl border border-zinc-200 bg-white p-1.5 shadow-xl shadow-zinc-900/10 ring-1 ring-black/5 dark:border-zinc-700 dark:bg-zinc-800 dark:shadow-black/30"
					>
						{options.map((option, index) => {
							const isSelected = String(option.props.value) === String(value);
							const isHighlighted = index === highlightedIndex;

							return cloneElement(option, {
								key: option.key ?? option.props.value,
								role: 'option',
								'aria-selected': isSelected,
								className: `flex w-full items-center justify-between rounded-lg px-3 py-2 text-left text-sm transition-colors ${option.props.disabled ? 'cursor-not-allowed opacity-40' : 'cursor-pointer'} ${isHighlighted && !option.props.disabled ? 'bg-teal-50 text-teal-800 dark:bg-teal-900/40 dark:text-teal-100' : 'text-zinc-700 dark:text-zinc-200'} ${option.props.className || ''}`,
								onMouseEnter: () => setHighlightedIndex(index),
								onMouseDown: (event) => event.preventDefault(),
								onClick: () => selectOption(option, index),
								children: (
									<>
										<span className="truncate">{option.props.children}</span>
										{isSelected && <FaCheck className="ml-3 h-3 w-3 shrink-0 text-teal-600 dark:text-teal-400" />}
									</>
								),
							});
						})}
					</div>
				)}
			</div>
		);
	}
);

Dropdown.displayName = 'Dropdown';

export default Dropdown;
