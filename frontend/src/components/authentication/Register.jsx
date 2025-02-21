import React, { useState } from 'react';
import authSlice from './store/slices/auth';
import { useDispatch } from 'react-redux';
import { Link } from 'react-router-dom';
import { FaCircleNotch } from 'react-icons/fa';
import { useRegisterMutation, useSendOtpMutation } from './api/registerApiSlice';
import { Formik } from 'formik';
import { registerSchema } from './AuthSchema';
import { useRef } from 'react';
import ReactModal from 'react-modal';
import OtpForm from './OtpForm';
import { confirmPassFormApiSlice } from './api/confirmPassFormApiSlice';

const classNames = (...classes) => {
    return classes.filter(Boolean).join(' ');
};
const RegisterForm = () => {
    const [register, { isLoading, isError, isSuccess }] = useRegisterMutation(); //use the isLoading later
    const [sendOtp, { isLoading: isLoadingOtp, isError: sendOtpError, isSuccess: sendOtpSuccess }] =
        useSendOtpMutation(); //use the isLoading later
    const [msg, setMsg] = useState('');
    const [otpMsg, setOtpMsg] = useState('');
    const formRef = useRef(null);
    const [otpFormPopover, setOtpFormPopover] = useState(false);
    const [otp, setOtp] = useState('');
    console.log(otp);
    const [userDetails, setUserDetails] = useState(null);

    // const changeHandler = (event) => {
    //     setUserDetails((prevState) => {
    //         return { ...prevState, [event.target.name]: event.target.value };
    //     });
    // };
    console.log(userDetails);
    const otpChangeHandler = (event) => {
        setOtp(event.target.value);
    };

    const submitButtonClicked = async (values, formikBag) => {
        setOtpMsg('');

        // console.log(formikBag.resetForm)

        try {
            const data = await register({
                email: values.email,
                password: values.password,
                username: values.username,
                phone_no: values.phone_no,
            }).unwrap();
            console.log(data);
            setOtpFormPopover(true);
            setMsg(data.detail);
        } catch (err) {
            console.log(err);
            if (err.hasOwnProperty('data')) {
                if (err.data.hasOwnProperty('username')) {
                    setMsg(err.data.username);
                } else if (err.data.hasOwnProperty('email')) {
                    setMsg(err.data.email);
                } else if (err.data.hasOwnProperty('phone_no')) {
                    setMsg(err.data.phone_no);
                } else if (err.data.hasOwnProperty('password')) {
                    setMsg('Ensure password is at least 8 characters long.');
                }
            } else {
                setMsg('Server Down');
            }
        }
        setUserDetails(values);
    };
    console.log(msg);
    const submitOtpButtonCliked = async (e) => {
        e.preventDefault();
        console.log(otp);
        // console.log(userDetails);
        const credentials = { ...userDetails, otp: otp };
        console.log(credentials);
        try {
            const data = await sendOtp(credentials).unwrap();
            console.log(data);
            setMsg(data.detail);

            setUserDetails(null);
            setOtpFormPopover(false);
        } catch (err) {
            console.log(err);
            setOtpMsg(err.data.detail);
        }
    };

    return (
        <main className="mx-auto flex min-h-screen max-w-md flex-col items-center justify-center">
            <section className="top-0 z-10 flex w-full justify-center p-2">
                <div className="relative h-[172px] w-full">
                    <Link to="/">
                        <img
                            src={`${import.meta.env.VITE_PUBLIC_URL}logo_full_dark.svg`}
                            alt="LOGO"
                            className=" absolute inset-0 mx-auto h-36 w-auto object-center transition-all duration-700 ease-in-out hover:h-[154px]"
                        />
                    </Link>

                    <p className="absolute bottom-0 mx-auto w-full text-center font-sans text-sm italic text-slate-400">
                        A Smart Payroll System on Cloud
                    </p>
                </div>
            </section>

            <section id="login" className="flex w-full flex-col md:justify-center">
                <div
                    className="box-border flex flex-col rounded-lg bg-zinc-50
                bg-opacity-70 p-6 shadow-xl dark:bg-black dark:bg-opacity-50 md:mx-6"
                >
                    <h1 className="mb-8 text-center text-4xl text-gray-900 text-opacity-70 dark:text-slate-100 dark:text-opacity-70">
                        Register
                    </h1>

                    {/* formik implementation */}
                    <Formik
                        initialValues={{
                            email: '',
                            password: '',
                            passConfirm: '',
                            username: '',
                            phone_no: '',
                        }}
                        validationSchema={registerSchema}
                        onSubmit={submitButtonClicked}
                    >
                        {({ handleSubmit, handleChange, handleBlur, values, errors, touched, isValid }) => (
                            <form
                                action=""
                                className="mx-6 flex flex-col justify-center gap-8 text-sm md:text-base"
                                onSubmit={handleSubmit}
                                ref={formRef}
                            >
                                {/* using an empty space as a placeholder so when placeholder
                    dissapears if user enter something then the label stays on top
                    we are using 'placeholder-shown' pseudo class butt it's not available in taiwind */}
                                <div className="relative">
                                    <input
                                        className="peer  w-full border-b-2 border-gray-800 border-opacity-25 bg-transparent p-1 outline-none transition focus:border-opacity-75 dark:border-slate-100 dark:border-opacity-25 md:p-2"
                                        type="text"
                                        id="username"
                                        name="username"
                                        placeholder=" "
                                        onChange={handleChange}
                                        onBlur={handleBlur}
                                        value={values.name}
                                    />
                                    <label
                                        htmlFor="username"
                                        className="absolute left-0 top-1 cursor-text italic text-gray-900 text-opacity-70 transition-all peer-focus:-top-4 peer-focus:text-xs peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70"
                                    >
                                        Username
                                    </label>
                                    {errors.username && touched.username && (
                                        <div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
                                            {errors.username}
                                        </div>
                                    )}
                                </div>

                                <div className="relative">
                                    <input
                                        className="peer  w-full border-b-2 border-gray-800 border-opacity-25 bg-transparent p-1 outline-none transition focus:border-opacity-75 dark:border-slate-100 dark:border-opacity-25 md:p-2"
                                        type="email"
                                        id="email"
                                        name="email"
                                        placeholder=" "
                                        onChange={handleChange}
                                        onBlur={handleBlur}
                                        value={values.name}
                                    />
                                    <label
                                        htmlFor="email"
                                        className="absolute left-0 top-1 cursor-text italic text-gray-900 text-opacity-70 transition-all peer-focus:-top-4 peer-focus:text-xs peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70"
                                    >
                                        Email
                                    </label>
                                    {errors.email && touched.email && (
                                        <div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
                                            {errors.email}
                                        </div>
                                    )}
                                </div>

                                <div className="relative">
                                    <input
                                        className="peer  w-full border-b-2 border-gray-800 border-opacity-25 bg-transparent p-1 outline-none transition focus:border-opacity-75 dark:border-slate-100 dark:border-opacity-25 md:p-2"
                                        type="tel"
                                        id="phone_no"
                                        name="phone_no"
                                        placeholder=" "
                                        onChange={handleChange}
                                        onBlur={handleBlur}
                                        value={values.name}
                                        maxLength={10}
                                    />
                                    <label
                                        htmlFor="phone_no"
                                        className="absolute left-0 top-1 cursor-text italic text-gray-900 text-opacity-70 transition-all peer-focus:-top-4 peer-focus:text-xs peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70"
                                    >
                                        Phone Number
                                    </label>
                                    {errors.phone_no && touched.phone_no && (
                                        <div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
                                            {errors.phone_no}
                                        </div>
                                    )}
                                </div>

                                <div className="relative">
                                    <input
                                        className="peer  w-full border-b-2 border-gray-800 border-opacity-25 bg-transparent p-1 outline-none transition focus:border-opacity-75 dark:border-slate-100 dark:border-opacity-25 md:p-2"
                                        type="password"
                                        id="password"
                                        name="password"
                                        placeholder=" "
                                        onChange={handleChange}
                                        onBlur={handleBlur}
                                        value={values.name}
                                    />
                                    <label
                                        htmlFor="password"
                                        className="absolute left-0 top-1 cursor-text italic text-gray-900 text-opacity-70 transition-all peer-focus:-top-4 peer-focus:text-xs peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70"
                                    >
                                        Password
                                    </label>
                                    {errors.password && touched.password && (
                                        <div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
                                            {errors.password}
                                        </div>
                                    )}
                                </div>

                                <div className="relative">
                                    <input
                                        className="peer  w-full border-b-2 border-gray-800 border-opacity-25 bg-transparent p-1 outline-none transition focus:border-opacity-75 dark:border-slate-100 dark:border-opacity-25 md:p-2"
                                        type="password"
                                        id="passConfirm"
                                        name="passConfirm"
                                        placeholder=" "
                                        onChange={handleChange}
                                        onBlur={handleBlur}
                                        value={values.name}
                                    />
                                    <label
                                        htmlFor="passConfirm"
                                        className="absolute left-0 top-1 cursor-text italic text-gray-900 text-opacity-70 transition-all peer-focus:-top-4 peer-focus:text-xs peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70"
                                    >
                                        Confirm Password
                                    </label>
                                    {errors.passConfirm && touched.passConfirm && (
                                        <div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
                                            {errors.passConfirm}
                                        </div>
                                    )}
                                </div>
                                {/* {errors.name && <div>{errors.name}</div>} */}
                                {/* <div className="text-red-500 dark:text-red-700 mt-1 text-sm font-bold">{errors}</div> */}
                                {console.log(values)}
                                {isError || isSuccess ? (
                                    <p
                                        className={classNames(
                                            isError
                                                ? 'text-red-500 dark:text-red-700'
                                                : 'text-green-500 dark:text-green-700',
                                            'mt-1 text-sm font-bold'
                                        )}
                                    >
                                        {msg}
                                    </p>
                                ) : (
                                    ''
                                )}
                                <button
                                    type="submit"
                                    className={classNames(
                                        isValid ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
                                        'my-2 w-full  rounded-lg bg-teal-500 p-2 text-gray-900 text-opacity-70 active:bg-teal-700 dark:bg-teal-700 dark:text-slate-100 dark:text-opacity-70 dark:active:bg-teal-500'
                                    )}
                                    disabled={!isValid}
                                // className={classNames(isValid ? "dark:hover:bg-teal-600  hover:bg-teal-600" : "opacity-40", "dark:bg-teal-700 rounded w-20 p-2 text-base font-medium bg-teal-500")}
                                >
                                    Register
                                </button>
                            </form>
                        )}
                    </Formik>

                    <Link
                        to="/login"
                        className="bottom-0 my-5 text-center text-sm text-gray-900 text-opacity-70 transition-all hover:text-opacity-100 dark:text-white dark:text-opacity-70 md:text-base"
                    >
                        Already have an account? Sign in
                    </Link>

                    <div
                        className={classNames(
                            isLoading ? '' : 'hidden',
                            'z-50 mx-auto mt-2 flex h-fit w-fit items-center rounded bg-indigo-600 p-2 font-medium'
                        )}
                    >
                        <FaCircleNotch className="mr-2 animate-spin text-white" />
                        Processing...
                    </div>

                    {/* OTP popup */}
                    <ReactModal
                        className="items-left fixed inset-0 mx-2 my-auto flex h-fit flex-col gap-4 rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-lg"
                        isOpen={otpFormPopover}
                        onRequestClose={() => setOtpFormPopover(false)}
                        style={{
                            overlay: {
                                backgroundColor: 'rgba(0, 0, 0, 0.75)',
                            },
                        }}
                    >
                        {/* <Formik
                            initialValues={{ newDepartment: "" }}
                            validationSchema={addDepartmentSchema}
                            onSubmit={addButtonClicked}
                            component={(props) => (
                                <AddDepartment
                                    {...props}
                                    setAddDepartmentPopover={
                                        setAddDepartmentPopover
                                    }
                                />
                            )}
                        /> */}
                        <OtpForm
                            setOtpFormPopover={setOtpFormPopover}
                            submitOtpButtonCliked={submitOtpButtonCliked}
                            otpChangeHandler={otpChangeHandler}
                            otpMsg={otpMsg}
                            sendOtpError={sendOtpError}
                        />
                    </ReactModal>
                </div>
            </section>
        </main>
    );
};

export default RegisterForm;
