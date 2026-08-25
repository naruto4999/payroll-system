const humanizeKey = (key) => {
	const label = key.replace(/([a-z])([A-Z])/g, '$1 $2').replaceAll('_', ' ');
	return label.charAt(0).toUpperCase() + label.slice(1);
};

const isUnsafeResponse = (value) =>
	typeof value === 'string' && /<(?:!doctype|html|body|script)\b/i.test(value);

const collectMessages = (value, path = '') => {
	if (typeof value === 'string') {
		if (isUnsafeResponse(value)) return [];
		return [path ? `${path}: ${value}` : value];
	}
	if ((typeof value === 'number' || typeof value === 'boolean') && path) {
		return [`${path}: ${value}`];
	}
	if (Array.isArray(value)) {
		if (path && value.every((item) => !item || typeof item !== 'object')) {
			return value.flatMap((item) => collectMessages(item, path));
		}
		return value.flatMap((item, index) =>
			collectMessages(item, path ? `${path}, row ${index + 1}` : `Row ${index + 1}`)
		);
	}
	if (!value || typeof value !== 'object') return [];

	return Object.entries(value).flatMap(([key, item]) => {
		if (key === 'code') return [];
		const label = /^\d+$/.test(key) ? `Row ${Number(key) + 1}` : humanizeKey(key);
		return collectMessages(item, path ? `${path}, ${label}` : label);
	});
};

export const getApiErrorMessage = (error, fallback = 'Error Occurred') => {
	const data = error?.data;
	if (typeof data?.detail === 'string' && !isUnsafeResponse(data.detail)) return data.detail;

	const messages = collectMessages(data);
	if (messages.length > 0) {
		return `${data?.code ? `${humanizeKey(data.code)}: ` : ''}${messages.join('; ')}`;
	}
	if (data?.code) return humanizeKey(data.code);
	if (typeof error?.error === 'string' && !isUnsafeResponse(error.error)) return error.error;
	if (error?.status) return `Request failed (${error.status})`;
	return fallback;
};
