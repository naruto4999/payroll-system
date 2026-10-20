const classNames = (...classes) => {
    // console.log(classes)
    return classes.filter(Boolean).join(" ");
};

const SwitchToggle = (props) => {
    // const [enabled, setEnabled] = useState(false);

    return (
        <button
            type="button"
            role="switch"
            aria-label="Dark mode"
            aria-checked={props.theme === "dark"}
            onClick={() => props.switch()}
            className={classNames(
                props.theme == "dark" ? "bg-teal-600" : "bg-gray-200",
                props.compact ? "h-[18px] w-8" : "h-4.5 sm:h-6 sm:w-11 w-8",
                "relative inline-flex flex-shrink-0 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 dark:focus:ring-offset-zinc-900"
            )}
        >
            <span
                aria-hidden="true"
                className={classNames(
                    props.theme == "dark" ? (props.compact ? "translate-x-3.5" : "sm:translate-x-5 translate-x-3.5") : "translate-x-0",
                    props.compact ? "h-3.5 w-3.5" : "h-3.5 w-3.5 sm:h-5 sm:w-5",
                    "pointer-events-none inline-block rounded-full bg-slate-100 shadow transform ring-0 transition ease-in-out duration-200"
                )}
            />
        </button>
    );
};

export default SwitchToggle;
