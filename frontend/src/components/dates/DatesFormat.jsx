function GetWeekDays() {

  const daysOfWeek = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
  
  const today = new Date()
  
  let weekDates = [];
  
  for (let i = 1; i < 7; i++) {
      const nd = new Date(today);
      nd.setDate(today.getDate() - i);
      weekDates.push(nd.getDay());
    }
  weekDates = weekDates.reverse();
  weekDates.push(today.getDay())
  
  const mappedWeek = weekDates.map(index => daysOfWeek[index]) 
  
    return mappedWeek
};

export default GetWeekDays;



export function GetDates() {
  const today = new Date();

  const weekDates = Array.from({ length: 7 }, (_, i) => {
    const date = new Date(today);
    date.setDate(today.getDate() - i);
    return formatDate(date);
  }).reverse();

  return weekDates;
}


export function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0'); // Add leading zero if needed
  const day = String(date.getDate()).padStart(2, '0'); // Add leading zero if needed
  return `${year}-${month}-${day}`;
}

