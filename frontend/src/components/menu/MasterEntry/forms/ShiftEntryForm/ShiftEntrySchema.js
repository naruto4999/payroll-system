import * as yup from "yup";

export const ShiftSchema = yup.object().shape({
    shiftName: yup
        .string()
        .matches(/^\S*$/, "Field must not contain spaces")
        .min(1, "Shift name must be atleast 1 characters long")
        .required("Required"),
    shiftBeginningTime: yup.string().required("Required"),
    shiftEndTime: yup.string().required("Required"),
    lunchTime: yup
        .number()
        .positive("Input must be a positive number")
        .integer("Input must be an integer")
        .min(0, "Input must be greater than or equal to 0")
        .max(1440, "Input must be less than or equal to 1440")
        .required("Required"),
    teaTime: yup
        .number()
        .positive("Input must be a positive number")
        .integer("Input must be an integer")
        .min(0, "Input must be greater than or equal to 0")
        .max(1440, "Input must be less than or equal to 1440")
        .required("Required"),
    lateGrace: yup
        .number()
        .positive("Input must be a positive number")
        .integer("Input must be an integer")
        .min(0, "Input must be greater than or equal to 0")
        .max(1440, "Input must be less than or equal to 1440")
        .required("Required"),
    otBeginAfter: yup
        .number()
        .positive("Input must be a positive number")
        .integer("Input must be an integer")
        .min(0, "Input must be greater than or equal to 0")
        .max(1440, "Input must be less than or equal to 1440")
        .required("Required"),
    nextShiftDelay: yup
        .number()
        .positive("Input must be a positive number")
        .integer("Input must be an integer")
        .min(0, "Input must be greater than or equal to 0")
        .max(1440, "Input must be less than or equal to 1440")
        .required("Required"),
    accidentalPunchBuffer: yup
        .number()
        .positive("Input must be a positive number")
        .integer("Input must be an integer")
        .min(0, "Input must be greater than or equal to 0")
        .max(1440, "Input must be less than or equal to 1440")
        .required("Required"),
    halfDayMinimumMinutes: yup
        .number()
        .positive("Input must be a positive number")
        .integer("Input must be an integer")
        .min(0, "Input must be greater than or equal to 0")
        .max(1440, "Input must be less than or equal to 1440")
        .required("Required"),
    fullDayMinimumMinutes: yup
        .number()
        .positive("Input must be a positive number")
        .integer("Input must be an integer")
        .min(0, "Input must be greater than or equal to 0")
        .max(1440, "Input must be less than or equal to 1440")
        .required("Required"),
    shortLeaves: yup
        .number()
        .positive("Input must be a positive number")
        .integer("Input must be an integer")
        .min(0, "Input must be greater than or equal to 0")
        .max(365, "Input must be less than or equal to 365")
        .required("Required"),
});

// export const editLeaveGradeSchema = yup.object().shape({
//     updatedLeaveGrade: yup
//         .string()
//         .min(1, "Leave Grade name must be atleast 1 characters long")
//         .required("Required"),
// });
