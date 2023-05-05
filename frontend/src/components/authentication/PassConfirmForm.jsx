import React, { useState, useEffect } from "react";
import { authActions } from "./store/slices/auth";
import { useDispatch, useSelector } from "react-redux";
import jwt_decode from "jwt-decode";
import { Link, useNavigate, useParams } from "react-router-dom";
import { FaCircleNotch } from "react-icons/fa";
//After using createApi from Redux toolkit
import { useConfirmPasswordMutation } from "./api/confirmPassFormApiSlice";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};
const currentDomain = window.location.hostname;
const currentPort = window.location.port;
const frontend_url = "http://" + currentDomain + ":" + currentPort;

const PassConfirmForm = (props) => {
    const navigate = useNavigate();
    const auth = useSelector((state) => state.auth);
    const [confirmPassword, { isLoading, isSuccess, isError }] =
        useConfirmPasswordMutation(); //use the isLoading later
    const [newPass, setNewPass] = useState({
        new_password1: "",
        new_password2: "",
    });
    const [msg, setMsg] = useState("");
    const { uid } = useParams();
    const { token } = useParams();
    console.log(uid);
    console.log(token);
    console.log(newPass);

    useEffect(() => {
        if (auth.account != null) {
            navigate("/home");
        }
    }, []);

    console.log(isError);
    console.log(isSuccess);
    console.log(msg);
    const changeHandler = (event) => {
        setNewPass((prevState) => {
            return { ...prevState, [event.target.name]: event.target.value };
        });
    };
    const dispatch = useDispatch();

    const submitButtonClicked = async (e) => {
        e.preventDefault();
        // console.log(username);
        const details = {
            new_password1: newPass.new_password1,
            new_password2: newPass.new_password2,
            uidb64 : uid,
            token : token,
        }
        console.log(details)
        try {
            const data = await confirmPassword(details).unwrap();
            console.log(data);
            setMsg(data.detail);
            // dispatch(
            //     authActions.setAuthTokens({
            //         token: data.access,
            //         refreshToken: data.refresh,
            //     })
            // );
            // let decoded = jwt_decode(data.access);
            // const user = {
            //     id: decoded.user_id,
            //     // email: decoded.email,
            //     username: decoded.username,
            // };
            // dispatch(authActions.setAccount(user));
            // navigate("/home");
            setNewPass({
                new_password1: "",
                new_password2: "",
            });
        } catch (err) {
            console.log(err);
            setMsg(err.data.detail);
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
                id="forgot-password"
                className="flex flex-col h-[calc(100vh-80px)] md:justify-center"
            >
                <div
                    className="box-border shadow-xl rounded-lg p-6 bg-zinc-50
                bg-opacity-60 dark:bg-black dark:bg-opacity-50 flex mt-2 md:mt-0 flex-col md:mx-6"
                >
                    <h1 className="text-gray-900 text-opacity-70 dark:text-opacity-70 dark:text-slate-100 text-4xl text-center mb-8 font-medium">
                        Set New Password
                    </h1>
                    <form
                        action=""
                        className="flex flex-col mx-6 md:text-base text-sm gap-4 justify-center"
                        onSubmit={submitButtonClicked}
                    >
                        {/* using an empty space as a placeholder so when placeholder
                    dissapears if user enter something then the label stays on top
                    we are using 'placeholder-shown' pseudo class butt it's not available in taiwind */}
                        <div className="relative">
                            <input
                                className="bg-transparent  border-b-2 border-gray-800 border-opacity-25 dark:border-opacity-25 dark:border-slate-100 md:p-2 p-1 outline-none focus:border-opacity-75 transition w-full peer"
                                type="password"
                                id="new_password1"
                                name="new_password1"
                                placeholder=" "
                                onChange={changeHandler}
                            />
                            <label
                                htmlFor="new_password1"
                                className="text-gray-900 text-opacity-70 dark:text-white dark:text-opacity-70 absolute left-0 top-1 cursor-text peer-focus:text-xs peer-focus:-top-4 peer-[&:not(:placeholder-shown)]:text-xs peer-[&:not(:placeholder-shown)]:-top-4 transition-all italic"
                            >
                                New Password
                            </label>
                        </div>

                        <div className="relative">
                            <input
                                className="bg-transparent  border-b-2 border-gray-800 border-opacity-25 dark:border-opacity-25 dark:border-slate-100 md:p-2 p-1 outline-none focus:border-opacity-75 transition w-full peer"
                                type="password"
                                id="new_password2"
                                name="new_password2"
                                placeholder=" "
                                onChange={changeHandler}
                            />
                            <label
                                htmlFor="new_password2"
                                className="text-gray-900 text-opacity-70 dark:text-white dark:text-opacity-70 absolute left-0 top-1 cursor-text peer-focus:text-xs peer-focus:-top-4 peer-[&:not(:placeholder-shown)]:text-xs peer-[&:not(:placeholder-shown)]:-top-4 transition-all italic"
                            >
                                Confirm New Password
                            </label>
                        </div>
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

                        <button className="w-full bg-teal-500 hover:bg-teal-600 active:bg-teal-700 dark:bg-teal-700 dark:hover:bg-teal-600 dark:active:bg-teal-500 rounded-lg p-2 my-2 text-gray-900 dark:text-slate-100 dark:text-opacity-70 text-opacity-70">
                            Reset
                        </button>
                    </form>

                    <Link
                        to="/register"
                        className="md:text-base text-sm text-gray-900 text-opacity-70 dark:text-white dark:text-opacity-70 text-center bottom-0 hover:text-opacity-100 dark:hover:text-opacity-100 transition-all"
                    >
                        Don't have an account? Register Now
                    </Link>
                </div>
                <div
                    className={classNames(
                        isLoading ? "" : "hidden",
                        "bg-indigo-600 w-fit h-fit rounded flex p-2 items-center font-medium z-50 mx-auto mt-2"
                    )}
                >
                    <FaCircleNotch className="animate-spin text-white mr-2" />
                    Processing...
                </div>
            </section>
        </main>
    );
};

export default PassConfirmForm;
