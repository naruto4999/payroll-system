import React, { useState, useEffect } from 'react';
import { authActions } from './store/slices/auth';
import { useDispatch, useSelector } from 'react-redux';
import jwt_decode from 'jwt-decode';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { FaCircleNotch } from 'react-icons/fa';
//After using createApi from Redux toolkit
import { useConfirmPasswordMutation } from './api/confirmPassFormApiSlice';
import { Formik } from 'formik';
import { passConfirm } from './AuthSchema';

const classNames = (...classes) => {
    return classes.filter(Boolean).join(' ');
};
const currentDomain = window.location.hostname;
const currentPort = window.location.port;
const frontend_url = 'http://' + currentDomain + ':' + currentPort;

const PassConfirmForm = (props) => {
    const navigate = useNavigate();
    const auth = useSelector((state) => state.auth);
    const [confirmPassword, { isLoading, isSuccess, isError }] = useConfirmPasswordMutation(); //use the isLoading later
    // const [newPass, setNewPass] = useState({
    //     newPassword1: "",
    //     newPassword2: "",
    // });
    const [msg, setMsg] = useState('');
    const { uid } = useParams();
    const { token } = useParams();
    // console.log(newPass);

    useEffect(() => {
        if (auth.account != null) {
            navigate('/home');
        }
    }, []);
    // const changeHandler = (event) => {
    //     setNewPass((prevState) => {
    //         return { ...prevState, [event.target.name]: event.target.value };
    //     });
    // };
    const dispatch = useDispatch();

    const submitButtonClicked = async (values, formikBag) => {
        // e.preventDefault();
        // console.log(username);

        console.log(uid);
        const details = {
            newPassword1: values.newPassword1,
            newPassword2: values.newPassword2,
            uidb64: uid,
            token: token,
        };
        console.log(details);
        try {
            const data = await confirmPassword(details).unwrap();
            console.log(data);
            setMsg(data.detail);
        } catch (err) {
            console.log(err);
            setMsg(err.data.detail);
        }
        formikBag.resetForm();
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

            <section id="forgot-password" className="flex w-full flex-col md:justify-center">
                <div
                    className="mt-2 box-border flex flex-col rounded-lg
                bg-zinc-50 bg-opacity-60 p-6 shadow-xl dark:bg-black dark:bg-opacity-50 md:mx-6 md:mt-0"
                >
                    <h1 className="mb-8 text-center text-4xl font-medium text-gray-900 text-opacity-70 dark:text-slate-100 dark:text-opacity-70">
                        Set New Password
                    </h1>

                    {/* formik Implimentation */}
                    <Formik
                        initialValues={{
                            newPassword1: '',
                            newPassword2: '',
                        }}
                        validationSchema={passConfirm}
                        onSubmit={submitButtonClicked}
                    >
                        {({ handleSubmit, handleChange, handleBlur, values, errors, touched }) => (
                            <form
                                action=""
                                className="mx-6 flex flex-col justify-center gap-4 text-sm md:text-base"
                            // onSubmit={handleSubmit}
                            >
                                {/* using an empty space as a placeholder so when placeholder
                    dissapears if user enter something then the label stays on top
                    we are using 'placeholder-shown' pseudo class butt it's not available in taiwind */}
                                <div className="relative">
                                    <input
                                        className="peer  w-full border-b-2 border-gray-800 border-opacity-25 bg-transparent p-1 outline-none transition focus:border-opacity-75 dark:border-slate-100 dark:border-opacity-25 md:p-2"
                                        type="password"
                                        id="newPassword1"
                                        name="newPassword1"
                                        placeholder=" "
                                        onChange={handleChange}
                                        onBlur={handleBlur}
                                        value={values.name}
                                    />
                                    <label
                                        htmlFor="newPassword1"
                                        className="absolute left-0 top-1 cursor-text italic text-gray-900 text-opacity-70 transition-all peer-focus:-top-4 peer-focus:text-xs peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70"
                                    >
                                        New Password
                                    </label>
                                    {errors.newPassword1 && touched.newPassword1 && (
                                        <div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
                                            {errors.newPassword1}
                                        </div>
                                    )}
                                </div>

                                <div className="relative">
                                    <input
                                        className="peer  w-full border-b-2 border-gray-800 border-opacity-25 bg-transparent p-1 outline-none transition focus:border-opacity-75 dark:border-slate-100 dark:border-opacity-25 md:p-2"
                                        type="password"
                                        id="newPassword2"
                                        name="newPassword2"
                                        placeholder=" "
                                        onChange={handleChange}
                                        onBlur={handleBlur}
                                        value={values.name}
                                    />
                                    <label
                                        htmlFor="newPassword2"
                                        className="absolute left-0 top-1 cursor-text italic text-gray-900 text-opacity-70 transition-all peer-focus:-top-4 peer-focus:text-xs peer-[&:not(:placeholder-shown)]:-top-4 peer-[&:not(:placeholder-shown)]:text-xs dark:text-white dark:text-opacity-70"
                                    >
                                        Confirm New Password
                                    </label>
                                    {errors.newPassword2 && touched.newPassword2 && (
                                        <div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
                                            {errors.newPassword2}
                                        </div>
                                    )}
                                </div>
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
                                {console.log(errors)}
                                <button
                                    type="submit"
                                    onClick={handleSubmit}
                                    className="my-2 w-full rounded-lg bg-teal-500 p-2 text-gray-900 text-opacity-70 hover:bg-teal-600 active:bg-teal-700 dark:bg-teal-700 dark:text-slate-100 dark:text-opacity-70 dark:hover:bg-teal-600 dark:active:bg-teal-500"
                                >
                                    Reset
                                </button>
                            </form>
                        )}
                    </Formik>
                </div>
                <div
                    className={classNames(
                        isLoading ? '' : 'hidden',
                        'z-50 mx-auto mt-2 flex h-fit w-fit items-center rounded bg-indigo-600 p-2 font-medium'
                    )}
                >
                    <FaCircleNotch className="mr-2 animate-spin text-white" />
                    Processing...
                </div>
            </section>
        </main>
    );
};

export default PassConfirmForm;
