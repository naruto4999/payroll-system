import * as yup from "yup";

export const LeaveGradeSchema =
    yup.object().shape({
        leaveGradeName: yup
            .string()
            .matches(/^\S*$/, "Field must not contain spaces")
            .min(1, "Leave Grade name must be atleast 1 characters long")
            .required("Required"),
        leaveGradeLimit: yup
            .number()
            .typeError("Field must be a number")
            .min(0, "Field must be greater than or equal to 0")
            .max(365, "Field must be less than or equal to 365")
            .required("Field is required"),
    });
