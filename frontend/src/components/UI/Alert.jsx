import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";

const Alert = () => {
    const { alerts } = useSelector((state) => state.alert);
    const [alert, setAlert] = useState({ type: "", message: "" });
    const [show, setShow] = useState(false);
    // const [visible, setVisible] = useState(true);
    const getBackgroundColor = () => {
        if (alert.type.toLowerCase() === "success") {
            return "bg-green-500";
        } else if (alert.type.toLowerCase() === "error") {
            return "bg-red-500";
        } else if (alert.type.toLowerCase() === "warning") {
            return "bg-yellow-500";
        } else {
            return "";
        }
    };

    useEffect(() => {
        if (alerts.length > 0) {
          setAlert(alerts[alerts.length - 1]);
          setShow(true);
          setTimeout(() => {
            setShow(false);
          }, alerts[alerts.length - 1].duration);
        }
      }, [alerts]);

    // useEffect(() => {
    //     const timer = setTimeout(() => {
    //         setVisible(false);
    //     }, duration);

    //     return () => {
    //         clearTimeout(timer);
    //     };
    // }, [duration]);

    return (
        <div className={`fixed z-50 right-0 ${show ? "" : "hidden"}`}>
            <div
                className={`shadow-md p-4 flex flex-row rounded-lg bg-slate-500 bg-opacity-50 m-2`}
            >
                <div
                    className={
                        getBackgroundColor() +
                        " inline-block rounded-lg p-1 mr-1"
                    }
                ></div>
                <b className="p-1">{alert.type}</b>
                <p className="p-1">{alert.message}</p>
                <a
                    className="h-5 w-5 inline-block p-1"
                    onClick={() => setShow(false)}
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-5 w-5"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                    >
                        <path
                            fillRule="evenodd"
                            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                            clipRule="evenodd"
                        />
                    </svg>
                </a>
            </div>
        </div>
    );
};

export default Alert;
