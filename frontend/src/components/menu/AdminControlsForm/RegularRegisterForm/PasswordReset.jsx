import React from 'react';
import { Field, ErrorMessage } from 'formik';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const PasswordReset = ({
	handleSubmit,
	handleChange,
	handleBlur,
	values,
	errors,
	isValid,
	touched,
	isSubmitting,
	setShowPasswordResetModal,
}) => {
	console.log(errors);
	return (
		<div className="text-gray-900 dark:text-slate-100">
			<h1 className="mb-2 text-2xl font-medium">Change Sub User Password</h1>
			<form action="" className="flex flex-col justify-center gap-2">
				<div>
					<label
						className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						htmlFor={'password'}
					>
						New Password
					</label>
					<Field
						className={classNames(
							errors.password && touched.password
								? // false
								  'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
								: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
							'block w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
						)}
						type="password"
						maxLength={30}
						name={'password'}
					/>
					<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
						<ErrorMessage name="password" />
					</div>
				</div>
				<div>
					<label
						className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						htmlFor={'confirmPassword'}
					>
						Confirm New Password
					</label>
					<Field
						className={classNames(
							errors.confirmPassword && touched.confirmPassword
								? // false
								  'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
								: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
							'block w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
						)}
						type="password"
						maxLength={30}
						name={'confirmPassword'}
					/>
					<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
						<ErrorMessage name="confirmPassword" />
					</div>
				</div>

				<section className="mt-4 mb-2 flex flex-row gap-4">
					<button
						className={classNames(
							isValid && !isSubmitting ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
							'w-24 rounded bg-teal-500 p-2 text-base font-medium dark:bg-teal-700'
						)}
						onClick={handleSubmit}
						type="submit"
						disabled={isSubmitting}
					>
						Confirm
					</button>
					<button
						className="w-20 rounded bg-zinc-400 p-2 text-base font-medium hover:bg-zinc-500 dark:bg-zinc-600 dark:hover:bg-zinc-700"
						type="button"
						onClick={() => {
							setShowPasswordResetModal(false);
						}}
					>
						Cancel
					</button>
				</section>
			</form>
		</div>
	);
};

export default PasswordReset;
