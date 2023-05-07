const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const OtpForm = ({
    submitOtpButtonCliked,
    otpChangeHandler,
    setOtpFormPopover,
    otpMsg,
    sendOtpError,
}) => {
    console.log(sendOtpError)
    return (
        <div className="text-gray-900 dark:text-slate-100">
            <h1 className="font-medium text-2xl mb-2">Enter OTP</h1>

            <form action="" className="flex flex-col gap-2 justify-center">
                <label
                    htmlFor="comapny-name"
                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                >
                    OTP
                </label>
                <div className="relative">
                    <input
                        className="border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25 rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 border-2 p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                        type="number"
                        id="newDepartment"
                        name="newDepartment"
                        onChange={otpChangeHandler}
                    />
                    {/* {isValid ? "" :<p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">{errors.newDepartment}</p>} */}
                </div>
                {sendOtpError ? (
                    <p
                        className={classNames(
                            sendOtpError
                                ? "text-red-500 dark:text-red-700"
                                : "text-green-500 dark:text-green-700",
                            "mt-1 text-sm font-bold"
                        )}
                    >
                        {otpMsg}
                    </p>
                ) : (
                    ""
                )}
            </form>
            <section className="flex flex-row gap-4 mt-4 mb-2">
                <button
                    className="dark:hover:bg-teal-600  hover:bg-teal-600 dark:bg-teal-700 rounded w-20 p-2 text-base font-medium bg-teal-500"
                    onClick={submitOtpButtonCliked}
                    type="submit"
                >
                    Add
                </button>
                <button
                    className="bg-zinc-400 hover:bg-zinc-500 dark:bg-zinc-600 rounded w-20 p-2 text-base font-medium dark:hover:bg-zinc-700"
                    onClick={() => setOtpFormPopover(false)}
                >
                    Cancel
                </button>
            </section>
        </div>
    );
};
export default OtpForm;
