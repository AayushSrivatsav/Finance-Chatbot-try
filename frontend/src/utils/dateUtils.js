import { format, formatDistanceToNow } from 'date-fns';

export const formatTimestamp = (timestamp) => {
  if (!timestamp) return '';
  
  try {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = (now - date) / (1000 * 60 * 60);
    
    if (diffInHours < 24) {
      return formatDistanceToNow(date, { addSuffix: true });
    } else {
      return format(date, 'MMM d, yyyy HH:mm');
    }
  } catch (error) {
    console.error('Error formatting timestamp:', error);
    return '';
  }
};

export const formatDate = (date, formatString = 'yyyy-MM-dd') => {
  if (!date) return '';
  
  try {
    return format(new Date(date), formatString);
  } catch (error) {
    console.error('Error formatting date:', error);
    return '';
  }
};

export const formatDateTime = (date) => {
  return formatDate(date, 'yyyy-MM-dd HH:mm:ss');
}; 