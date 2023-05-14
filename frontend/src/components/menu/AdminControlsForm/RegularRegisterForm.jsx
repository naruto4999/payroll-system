import React, { useState, useEffect } from "react";
// import authSlice from "./store/slices/auth";
import { useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import {
    useGetRegularsQuery,
    useRegularRegisterMutation,
    useDeleteRegularMutation,
} from "../../authentication/api/employeeRegisterApiSlice";
import { Formik } from "formik";
import { registerSchema } from "../../authentication/AuthSchema";
import { useOutletContext } from "react-router-dom";
import { FaCircleNotch } from "react-icons/fa";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const RegularRegisterForm = () => {
    const {
        data: fetchedData,
        isLoading,
        isSuccess,
        isError,
        error,
        isFetching,
    } = useGetRegularsQuery();
    const [
        regularRegister,
        {
            isLoading: isRegisteringRegular,
            isError: errorRegisteringRegular,
            isSuccess: successRegisteringRegular,
        },
    ] = useRegularRegisterMutation(); //use the isLoading later
    const [msg, setMsg] = useState("");
    const [showLoadingBar, setShowLoadingBar] = useOutletContext();
    const [deleteRegular, { isLoading: isDeletingRegular }] =
        useDeleteRegularMutation();

    // console.log(fetchedData);

    const deleteButtonClicked = async (resetForm) => {
        setMsg("");
        console.log(resetForm);
        resetForm({
            values: {
                email: "",
                password: "",
                passConfirm: "",
                username: "",
                phone_no: "",
            },
        });
        try {
            const data = await deleteRegular().unwrap();
            console.log(data);
        } catch (err) {
            console.log(err);
        }
        
    };
    const submitButtonClicked = async (values, formikBag) => {
        // e.preventDefault();
        console.log(values);
        try {
            const data = await regularRegister({
                email: values.email,
                password: values.password,
                username: values.username,
                phone_no: values.phone_no,
            }).unwrap();
            console.log(data);
            setMsg(data.detail);
        } catch (err) {
            console.log(err);
            setMsg(err.data.detail);
        }
        
    };

    useEffect(() => {
        setShowLoadingBar(isRegisteringRegular || isLoading || isDeletingRegular);
    }, [isRegisteringRegular, isLoading, isDeletingRegular]);

    if (isLoading) {
        return (
            <div className="fixed inset-0 mx-auto my-auto bg-indigo-600 w-fit h-fit rounded flex p-2 items-center font-medium z-50">
                <FaCircleNotch className="animate-spin text-white mr-2" />
                Processing...
            </div>
        );
    } else {
        return (
            <section className="mx-5 mt-2">
                <div className="flex flex-row place-content-between flex-wrap">
                    <div className="mr-4">
                        <h1 className="text-3xl font-medium">Sub User</h1>
                        <p className="text-sm my-2">
                            {isSuccess
                                ? "Sub user already exists, below are the details."
                                : "Create Sub User Here"}
                        </p>
                    </div>
                   
                    {/* <button
                    className="dark:bg-teal-700 my-auto rounded p-2 text-base font-medium bg-teal-500 hover:bg-teal-600 dark:hover:bg-teal-600 whitespace-nowrap"
                    onClick={() => setAddDepartmentPopover(true)}
                >
                    Add Department
                </button> */}
                </div>

                {/* Formik Implementation */}
                <Formik
                    initialValues={
                        isSuccess
                            ? {
                                  email: fetchedData.email,
                                  username: fetchedData.username,
                                  phone_no: fetchedData.phone_no,
                              }
                            : {
                                  email: "",
                                  password: "",
                                  passConfirm: "",
                                  username: "",
                                  phone_no: "",
                              }
                    }
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
                        isValid,
                        resetForm,
                    }) => (
                        <form id="" className="mt-2" onSubmit={handleSubmit}>
                            <div className="flex flex-col w-full gap-2">
                                <div>
                                    <label
                                        htmlFor="username"
                                        className="my-auto dark:text-blueAccent-400 text-blueAccent-700 font-medium block"
                                    >
                                        Username
                                    </label>
                                    <input
                                        type="text"
                                        name="username"
                                        id="username"
                                        className="dark:bg-zinc-800 bg-slate-200 dark:text-slate-400 text-slate-500 rounded p-2 w-full lg:w-1/3"
                                        onChange={handleChange}
                                        onBlur={handleBlur}
                                        value={values.username}
                                        disabled={isSuccess ? true : false}
                                    />
                                    {errors.username && touched.username && (
                                        <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                            {errors.username}
                                        </div>
                                    )}
                                </div>
                                <div>
                                    <label
                                        htmlFor="email"
                                        className="my-auto dark:text-blueAccent-400 text-blueAccent-700 font-medium block"
                                    >
                                        Email
                                    </label>
                                    <input
                                        type="text"
                                        name="email"
                                        id="email"
                                        className="dark:bg-zinc-800 bg-slate-200 dark:text-slate-400 text-slate-500 rounded p-2 w-full lg:w-1/2"
                                        onChange={handleChange}
                                        onBlur={handleBlur}
                                        value={values.email}
                                        disabled={isSuccess ? true : false}
                                    />
                                    {errors.email && touched.email && (
                                        <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                            {errors.email}
                                        </div>
                                    )}
                                </div>
                                <div>
                                    <label
                                        htmlFor="phone_no"
                                        className="my-auto dark:text-blueAccent-400 text-blueAccent-700 font-medium block"
                                    >
                                        Phone Number
                                    </label>
                                    <input
                                        type="tel"
                                        name="phone_no"
                                        id="phone_no"
                                        className="dark:bg-zinc-800 bg-slate-200 dark:text-slate-400 text-slate-500 rounded p-2"
                                        maxLength="10"
                                        size="10"
                                        onChange={handleChange}
                                        onBlur={handleBlur}
                                        value={values.phone_no}
                                        disabled={isSuccess ? true : false}
                                    />
                                    {errors.phone_no && touched.phone_no && (
                                        <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                            {errors.phone_no}
                                        </div>
                                    )}
                                </div>
                                {!isSuccess && (
                                    <div>
                                        <label
                                            htmlFor="password"
                                            className="my-auto dark:text-blueAccent-400 text-blueAccent-700 font-medium block"
                                        >
                                            Password
                                        </label>
                                        <input
                                            type="password"
                                            name="password"
                                            id="password"
                                            className="dark:bg-zinc-800 bg-slate-200 dark:text-slate-400 text-slate-500 rounded p-2 w-full lg:w-fit"
                                            onChange={handleChange}
                                            onBlur={handleBlur}
                                            value={values.name}
                                        />
                                        {errors.password &&
                                            touched.password && (
                                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                                    {errors.password}
                                                </div>
                                            )}
                                    </div>
                                )}
                                {!isSuccess && (
                                    <div>
                                        <label
                                            htmlFor="passConfirm"
                                            className="my-auto dark:text-blueAccent-400 text-blueAccent-700 font-medium block"
                                        >
                                            Confirm Password
                                        </label>
                                        <input
                                            type="password"
                                            name="passConfirm"
                                            id="passConfirm"
                                            className="dark:bg-zinc-800 bg-slate-200 dark:text-slate-400 text-slate-500 rounded p-2 w-full lg:w-fit"
                                            onChange={handleChange}
                                            onBlur={handleBlur}
                                            value={values.name}
                                        />
                                        {errors.passConfirm &&
                                            touched.passConfirm && (
                                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                                    {errors.passConfirm}
                                                </div>
                                            )}
                                    </div>
                                )}
                                {errorRegisteringRegular ||
                                successRegisteringRegular ? (
                                    <p
                                        className={classNames(
                                            errorRegisteringRegular
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
                                {!isSuccess && (
                                    <div>
                                        <button
                                            className="dark:bg-teal-700 mt-4 rounded py-2 px-6 text-base font-medium bg-teal-500 hover:bg-teal-600 dark:hover:bg-teal-600 whitespace-nowrap"
                                            type="submit"
                                        >
                                            Create
                                        </button>
                                    </div>
                                )}
                                {isSuccess && (
                                    <div>
                                        <button
                                            className="mt-4 rounded py-2 px-6 text-base font-medium dark:bg-redAccent-700 bg-redAccent-500 dark:hover:bg-redAccent-500 hover:bg-redAccent-700 whitespace-nowrap"
                                            type="button"
                                            onClick={() => {
                                                deleteButtonClicked(resetForm);
                                            }}
                                        >
                                            Delete
                                        </button>
                                    </div>
                                )}
                            </div>
                        </form>
                    )}
                </Formik>
            </section>
        );
    }
};
export default RegularRegisterForm;
