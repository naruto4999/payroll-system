import React, { useState, useEffect } from "react";
import { authActions } from "./store/slices/auth";
import { useDispatch, useSelector } from "react-redux";
import jwt_decode from "jwt-decode";
import { Link, useNavigate } from "react-router-dom";

//After using createApi from Redux toolkit
import { useLoginMutation } from "./api/loginApiSlice";

const LoginForm = () => {
    const navigate = useNavigate();
    const auth = useSelector((state) => state.auth);
    const [login, { isLoading }] = useLoginMutation(); //use the isLoading later
    const [userDetails, setUserDetails] = useState({
        email: "",
        password: "",
        username: "",
    });
    console.log(auth)
    useEffect(() => {
        if (auth.account != null) {
            navigate("/home");
        }
    }, []);

    console.log(userDetails);

    const changeHandler = (event) => {
        setUserDetails((prevState) => {
            return { ...prevState, [event.target.name]: event.target.value };
        });
    };
    const dispatch = useDispatch();

    const submitButtonClicked = async (e) => {
        e.preventDefault();
        console.log(userDetails);
        try {
            const data = await login({
                email: userDetails.email,
                password: userDetails.password,
                username: userDetails.username,
            }).unwrap();
            console.log(data);
            dispatch(
                authActions.setAuthTokens({
                    token: data.access,
                    refreshToken: data.refresh,
                })
            );
            let decoded = jwt_decode(data.access);
            const user = {
                id: decoded.user_id,
                email: decoded.email,
                username: decoded.username,
            };
            dispatch(authActions.setAccount(user));
            navigate("/home");
            setUserDetails({
                email: "",
                password: "",
                username: "",
            });
        } catch (err) {
            console.log(err);
        }
    };

    return (
        <main className="mx-auto max-w-md h-screen ">
            <section className="top-0 z-10 sticky p-2">
                <img src="../../../public/logo_dark.png" alt="LOGO" className="w-auto h-16 object-center mx-auto" />
            </section>

            <section id="login" className="flex flex-col h-[calc(100vh-80px)] md:justify-center">
                <div
                    className="box-border shadow-xl rounded-lg p-6 bg-zinc-50
                bg-opacity-60 dark:bg-black dark:bg-opacity-50 flex mt-2 md:mt-0 flex-col md:mx-6"
                >
                    <h1 className="text-gray-900 text-opacity-70 dark:text-opacity-70 dark:text-slate-100 text-4xl text-center mb-8 font-medium">
                        Sign in
                    </h1>
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
                        <button className="w-full bg-teal-500 hover:bg-teal-600 active:bg-teal-700 dark:bg-teal-700 dark:hover:bg-teal-600 dark:active:bg-teal-500 rounded-lg p-2 my-2 text-gray-900 dark:text-slate-100 dark:text-opacity-70 text-opacity-70">
                            Sign in
                        </button>
                    </form>
                    <a
                        href=""
                        className="my-5 md:text-base text-sm text-gray-900 text-opacity-70 dark:text-white dark:text-opacity-70 text-center hover:text-opacity-100 dark:hover:text-opacity-100 transition-all"
                    >
                        Forgot Pasword?
                    </a>

                    <Link
                        to="/register"
                        className="md:text-base text-sm text-gray-900 text-opacity-70 dark:text-white dark:text-opacity-70 text-center bottom-0 hover:text-opacity-100 dark:hover:text-opacity-100 transition-all"
                    >
                        Don't have an account? Register Now
                    </Link>
                </div>
            </section>
        </main>
    );
};

export default LoginForm;
