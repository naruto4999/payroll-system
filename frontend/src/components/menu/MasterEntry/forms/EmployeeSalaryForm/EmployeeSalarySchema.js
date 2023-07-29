import * as yup from "yup";

export const generateEmployeeSalarySchema = (fetchedEarningsHeads) => {
    const months = [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
    ];

    if (fetchedEarningsHeads) {
        const salarySchema = yup.object().shape({
            earnings: yup.object().shape(
                fetchedEarningsHeads.reduce((schema, key) => {
                    return {
                        ...schema,
                        [key.name]: yup.object().shape(
                            months.reduce((monthSchema, month) => {
                                return {
                                    ...monthSchema,
                                    [month]: yup.number().required(`Required`),
                                };
                            }, {})
                        ),
                    };
                }, {})
            ),
        });

        return salarySchema;
    } else {
        return {};
    }
};
