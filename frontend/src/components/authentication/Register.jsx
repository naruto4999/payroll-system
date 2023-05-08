import React, { useState } from "react";
import authSlice from "./store/slices/auth";
import { useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import { FaCircleNotch } from "react-icons/fa";
import {
    useRegisterMutation,
    useSendOtpMutation,
} from "./api/registerApiSlice";
import { Formik } from "formik";
import { registerSchema } from "./AuthSchema";
import { useRef } from "react";
import ReactModal from "react-modal";
import OtpForm from "./OtpForm";
import { confirmPassFormApiSlice } from "./api/confirmPassFormApiSlice";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};
const RegisterForm = () => {
    const [register, { isLoading, isError, isSuccess }] = useRegisterMutation(); //use the isLoading later
    const [
        sendOtp,
        {
            isLoading: isLoadingOtp,
            isError: sendOtpError,
            isSuccess: sendOtpSuccess,
        },
    ] = useSendOtpMutation(); //use the isLoading later
    const [msg, setMsg] = useState("");
    const [otpMsg, setOtpMsg] = useState("");
    const formRef = useRef(null);
    const [otpFormPopover, setOtpFormPopover] = useState(false);
    const [otp, setOtp] = useState("");
    console.log(otp)
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
        setOtpMsg("");

        // console.log(formikBag.resetForm)

        try {
            const data = await register({
                email: values.email,
                password: values.password,
                username: values.username,
                phone_no: values.phone_no,
            }).unwrap();
            // formikBag.resetForm({
            //     values: {
            //         // the type of `values` inferred to be Blog
            //         email: "",
            //         password: "",
            //         passConfirm: "",
            //         username: "",
            //         phone_no: "",
            //     },
            // });
            // formRef.current.reset();
            // formRef.current.reset();
            console.log(data);
            setOtpFormPopover(true);
            setMsg(data.detail);
        } catch (err) {
            console.log(err);
            if (err.hasOwnProperty("data")) {
                if (err.data.hasOwnProperty("username")) {
                    setMsg(err.data.username);
                } else if (err.data.hasOwnProperty("email")) {
                    setMsg(err.data.email);
                } else if (err.data.hasOwnProperty("phone_no")) {
                    setMsg(err.data.phone_no);
                } else if (err.data.hasOwnProperty("password")) {
                    setMsg("Ensure password is at least 8 characters long.");
                }
            } else {
                setMsg("Server Down");
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
        <main className="mx-auto max-w-md h-screen ">
            <section className="top-0 z-10 sticky p-2">
                <img
                    src="../../../public/logo_dark.png"
                    alt="LOGO"
                    className="w-auto h-16 object-center mx-auto"
                />
            </section>

            <section
                id="login"
                className="flex flex-col h-[calc(100vh-80px)] md:justify-center"
            >
                <div
                    className="box-border shadow-xl rounded-lg p-6 bg-zinc-50
                bg-opacity-70 dark:bg-black dark:bg-opacity-50 flex flex-col md:mx-6"
                >
                    <h1 className="text-gray-900 text-opacity-70 dark:text-opacity-70 dark:text-slate-100 text-4xl text-center mb-8">
                        Register
                    </h1>

                    {/* formik implementation */}
                    <Formik
                        initialValues={{
                            email: "",
                            password: "",
                            passConfirm: "",
                            username: "",
                            phone_no: "",
                        }}
                        validationSchema={registerSchema}
                        onSubmit={submitButtonClicked}
                    >
                        {({
                            handleSubmit,
                            handleChange,
                            handleBlur,
                            values,
                            errors,
                            touched,
                            isValid
                        }) => (
                            <form
                                action=""
                                className="flex flex-col mx-6 md:text-base text-sm gap-8 justify-center"
                                onSubmit={handleSubmit}
                                ref={formRef}
                            >
                                {/* using an empty space as a placeholder so when placeholder
                    dissapears if user enter something then the label stays on top
                    we are using 'placeholder-shown' pseudo class butt it's not available in taiwind */}
                                <div className="relative">
                                    <input
                                        className="bg-transparent  border-b-2 border-gray-800 border-opacity-25 dark:border-opacity-25 dark:border-slate-100 md:p-2 p-1 outline-none focus:border-opacity-75 transition w-full peer"
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
                                        className="text-gray-900 text-opacity-70 dark:text-white dark:text-opacity-70 absolute left-0 top-1 cursor-text peer-focus:text-xs peer-focus:-top-4 peer-[&:not(:placeholder-shown)]:text-xs peer-[&:not(:placeholder-shown)]:-top-4 transition-all italic"
                                    >
                                        Username
                                    </label>
                                    {errors.username && touched.username && (
                                        <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                            {errors.username}
                                        </div>
                                    )}
                                </div>

                                <div className="relative">
                                    <input
                                        className="bg-transparent  border-b-2 border-gray-800 border-opacity-25 dark:border-opacity-25 dark:border-slate-100 md:p-2 p-1 outline-none focus:border-opacity-75 transition w-full peer"
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
                                        className="text-gray-900 text-opacity-70 dark:text-white dark:text-opacity-70 absolute left-0 top-1 cursor-text peer-focus:text-xs peer-focus:-top-4 peer-[&:not(:placeholder-shown)]:text-xs peer-[&:not(:placeholder-shown)]:-top-4 transition-all italic"
                                    >
                                        Email
                                    </label>
                                    {errors.email && touched.email && (
                                        <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                            {errors.email}
                                        </div>
                                    )}
                                </div>

                                <div className="relative">
                                    <input
                                        className="bg-transparent  border-b-2 border-gray-800 border-opacity-25 dark:border-opacity-25 dark:border-slate-100 md:p-2 p-1 outline-none focus:border-opacity-75 transition w-full peer"
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
                                        className="text-gray-900 text-opacity-70 dark:text-white dark:text-opacity-70 absolute left-0 top-1 cursor-text peer-focus:text-xs peer-focus:-top-4 peer-[&:not(:placeholder-shown)]:text-xs peer-[&:not(:placeholder-shown)]:-top-4 transition-all italic"
                                    >
                                        Phone Number
                                    </label>
                                    {errors.phone_no && touched.phone_no && (
                                        <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                            {errors.phone_no}
                                        </div>
                                    )}
                                </div>

                                <div className="relative">
                                    <input
                                        className="bg-transparent  border-b-2 border-gray-800 border-opacity-25 dark:border-opacity-25 dark:border-slate-100 md:p-2 p-1 outline-none focus:border-opacity-75 transition w-full peer"
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
                                        className="text-gray-900 text-opacity-70 dark:text-white dark:text-opacity-70 absolute left-0 top-1 cursor-text peer-focus:text-xs peer-focus:-top-4 peer-[&:not(:placeholder-shown)]:text-xs peer-[&:not(:placeholder-shown)]:-top-4 transition-all italic"
                                    >
                                        Password
                                    </label>
                                    {errors.password && touched.password && (
                                        <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                            {errors.password}
                                        </div>
                                    )}
                                </div>

                                <div className="relative">
                                    <input
                                        className="bg-transparent  border-b-2 border-gray-800 border-opacity-25 dark:border-opacity-25 dark:border-slate-100 md:p-2 p-1 outline-none focus:border-opacity-75 transition w-full peer"
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
                                        className="text-gray-900 text-opacity-70 dark:text-white dark:text-opacity-70 absolute left-0 top-1 cursor-text peer-focus:text-xs peer-focus:-top-4 peer-[&:not(:placeholder-shown)]:text-xs peer-[&:not(:placeholder-shown)]:-top-4 transition-all italic"
                                    >
                                        Confirm Password
                                    </label>
                                    {errors.passConfirm &&
                                        touched.passConfirm && (
                                            <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
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
                                                ? "text-red-500 dark:text-red-700"
                                                : "text-green-500 dark:text-green-700",
                                            "mt-1 text-sm font-bold"
                                        )}
                                    >
                                        {msg}
                                    </p>
                                ) : (
                                    ""
                                )}
                                <button
                                    type="submit"
                                    className={classNames(isValid ? "dark:hover:bg-teal-600  hover:bg-teal-600" : "opacity-40","w-full bg-teal-500  active:bg-teal-700 dark:bg-teal-700 dark:active:bg-teal-500 rounded-lg p-2 my-2 text-gray-900 dark:text-slate-100 dark:text-opacity-70 text-opacity-70")}
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
                        className="md:text-base text-sm text-gray-900 text-opacity-70 dark:text-white dark:text-opacity-70 text-center bottom-0 hover:text-opacity-100 transition-all my-5"
                    >
                        Already have an account? Sign in
                    </Link>

                    <div
                        className={classNames(
                            isLoading ? "" : "hidden",
                            "bg-indigo-600 w-fit h-fit rounded flex p-2 items-center font-medium z-50 mx-auto mt-2"
                        )}
                    >
                        <FaCircleNotch className="animate-spin text-white mr-2" />
                        Processing...
                    </div>

                    {/* OTP popup */}
                    <ReactModal
                        className="fixed inset-0 mx-2 sm:mx-auto my-auto sm:max-w-lg h-fit bg-zinc-300 dark:bg-zinc-800 p-4 flex flex-col items-left gap-4 rounded shadow-xl"
                        isOpen={otpFormPopover}
                        onRequestClose={() => setOtpFormPopover(false)}
                        style={{
                            overlay: {
                                backgroundColor: "rgba(0, 0, 0, 0.75)",
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
