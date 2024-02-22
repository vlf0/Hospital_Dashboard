
function GetWeekDays() {

const daysOfWeek = ['Вск', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']

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




