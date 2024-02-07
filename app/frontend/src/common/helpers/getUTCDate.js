export function getUTCDate(dateString) {
    if (typeof dateString === 'undefined') return;
    if (!dateString.includes('-')) return;
    const parsedDateString = dateString.split('-').map(dateValue => parseInt(dateValue));
    const year = parsedDateString[0];
    const month = parsedDateString[1];
    const day = parsedDateString[2];
    return new Date(Date.UTC(year, month, day)).getTime();
}
