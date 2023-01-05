import React, { useState } from "react";
import authSlice from "./store/slices/auth";
import { useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import { useRegisterMutation } from "./api/registerApiSlice";

const RegisterForm = () => {
    const [register, { isLoading }] = useRegisterMutation(); //use the isLoading later
    const [userDetails, setUserDetails] = useState({
        email: "",
        password: "",
        passConfirm: "",
        username: "",
    });

    console.log(userDetails);

    const changeHandler = (event) => {
        setUserDetails((prevState) => {
            return { ...prevState, [event.target.name]: event.target.value };
        });
    };

    const submitButtonClicked = async (e) => {
        e.preventDefault();
        if (userDetails.password == userDetails.passConfirm) {
            try {
                const data = await register({
                    email: userDetails.email,
                    password: userDetails.password,
                    username: userDetails.username,
                }).unwrap();
                console.log(data);
                
                setUserDetails({
                    email: "",
                    password: "",
                    passConfirm: "",
                    username: "",
                });
            } catch (err) {
                console.log(err);
            }
           
        } else console.log("Password don't match");
    };

    return (
        <main className="mx-auto max-w-md h-screen ">
            <section className="top-0 z-10 sticky p-2">
                <img src="../../../public/logo_dark.png" alt="LOGO" className="w-auto h-16 object-center mx-auto" />
                
            </section>

            <section id="login" className="flex flex-col h-[calc(100vh-80px)] justify-center">
                <div className="box-border shadow-xl rounded-lg p-6 bg-zinc-50
                bg-opacity-70 dark:bg-black dark:bg-opacity-50 flex flex-col md:mx-6">
                    <h1 className="text-gray-900 text-opacity-70 dark:text-opacity-70 dark:text-slate-100 text-4xl text-center mb-8">Register</h1>
                    <form
                        action=""
                        className="flex flex-col mx-6 md:text-base text-sm gap-8 justify-center"
                        onSubmit={submitButtonClicked}
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
                                onChange={changeHandler}
                            />
                            <label
                                htmlFor="username"
                                className="text-gray-900 text-opacity-70 dark:text-white dark:text-opacity-70 absolute left-0 top-1 cursor-text peer-focus:text-xs peer-focus:-top-4 peer-[&:not(:placeholder-shown)]:text-xs peer-[&:not(:placeholder-shown)]:-top-4 transition-all italic"
                            >
                                Username
                            </label>
                        </div>

                        <div className="relative">
                            <input
                                className="bg-transparent  border-b-2 border-gray-800 border-opacity-25 dark:border-opacity-25 dark:border-slate-100 md:p-2 p-1 outline-none focus:border-opacity-75 transition w-full peer"
                                type="email"
                                id="email"
                                name="email"
                                placeholder=" "
                                onChange={changeHandler}
                            />
                            <label
                                htmlFor="email"
                                className="text-gray-900 text-opacity-70 dark:text-white dark:text-opacity-70 absolute left-0 top-1 cursor-text peer-focus:text-xs peer-focus:-top-4 peer-[&:not(:placeholder-shown)]:text-xs peer-[&:not(:placeholder-shown)]:-top-4 transition-all italic"
                            >
                                Email
                            </label>
                        </div>

                        <div className="relative">
                            <input
                                className="bg-transparent  border-b-2 border-gray-800 border-opacity-25 dark:border-opacity-25 dark:border-slate-100 md:p-2 p-1 outline-none focus:border-opacity-75 transition w-full peer"
                                type="password"
                                id="password"
                                name="password"
                                placeholder=" "
                                onChange={changeHandler}
                            />
                            <label
                                htmlFor="password"
                                className="text-gray-900 text-opacity-70 dark:text-white dark:text-opacity-70 absolute left-0 top-1 cursor-text peer-focus:text-xs peer-focus:-top-4 peer-[&:not(:placeholder-shown)]:text-xs peer-[&:not(:placeholder-shown)]:-top-4 transition-all italic"
                            >
                                Password
                            </label>
                        </div>

                        <div className="relative">
                            <input
                                className="bg-transparent  border-b-2 border-gray-800 border-opacity-25 dark:border-opacity-25 dark:border-slate-100 md:p-2 p-1 outline-none focus:border-opacity-75 transition w-full peer"
                                type="password"
                                id="passConfirm"
                                name="passConfirm"
                                placeholder=" "
                                onChange={changeHandler}
                            />
                            <label
                                htmlFor="passConfirm"
                                className="text-gray-900 text-opacity-70 dark:text-white dark:text-opacity-70 absolute left-0 top-1 cursor-text peer-focus:text-xs peer-focus:-top-4 peer-[&:not(:placeholder-shown)]:text-xs peer-[&:not(:placeholder-shown)]:-top-4 transition-all italic"
                            >
                                Confirm Password
                            </label>
                        </div>
                        <button className="w-full bg-teal-500 hover:bg-teal-600 active:bg-teal-700 dark:bg-teal-700 dark:hover:bg-teal-600 dark:active:bg-teal-500 rounded-lg p-2 my-2 text-gray-900 dark:text-slate-100 dark:text-opacity-70 text-opacity-70">
                            Register
                        </button>
                    </form>
                    
                    <Link
                        to="/login"
                        className="md:text-base text-sm text-gray-900 text-opacity-70 dark:text-white dark:text-opacity-70 text-center bottom-0 hover:text-opacity-100 transition-all my-5"
                    >
                        Already have an account? Sign in
                    </Link>
                </div>
            </section>
        </main>
    );
};

export default RegisterForm;
