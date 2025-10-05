import toast from 'react-hot-toast';

export const handleApiError = (err: any, fallback = 'Something went wrong') => {
  const message =
    err.response?.data?.error ||
    err.response?.data?.info ||
    err.message ||
    fallback;
  toast.error(message);
  return message;
};
