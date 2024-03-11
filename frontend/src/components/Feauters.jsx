import { format, subHours } from 'date-fns';

export function DateFormatting(date) {
  // const dateString = "2024-01-10T00:40:15+03:00";
  const dateTimeObject = new Date(date);
  
  // Subtract 3 hours
  const subtractedDate = subHours(dateTimeObject, 3);
  
  // Format the result
  const formattedSubtractedDate = format(subtractedDate, 'dd.MM.yyyy HH:mm:ss');
  
  return formattedSubtractedDate
};


export function CustomMap(currentDay, yesterday) {
    const result = [currentDay, yesterday, Persents(currentDay, yesterday)]
    return result
};

export function Persents(today, yesterday) {

    let percent = ((today-yesterday)/yesterday*100).toFixed(1)
    percent = percent.toString() + '%'
    percent = percent.replace('-', '');
    return percent
};

export const extractProperty = (dataList, key) => {
    return dataList.map(item => item[key]);
};
  
export function ensureArrayLength(array, desiredLength) {
  if (array.length !== desiredLength) {
    const numberOfTimesToInsert = desiredLength - array.length;

    for (let i = 0; i < numberOfTimesToInsert; i++) {
      array.unshift(null);
    }
  }
};

export function DeadTableProcess(dataset) {
  // Using map to transform each item in the dataset
  const modifiedObjects = dataset.map(item => {
    return {
      'ФИО': item.pat_fio,
      '№ ИБ': item.ib_num,
      'Пол': item.sex,
      'Возраст': item.age,
      'Дата поступления': DateFormatting(item.arriving_dt),
      'Состояние при поступлении': item.state,
      'Кол-во койко дней': item.days,
      'Дигноз при поступлении': item.diag_arr,
      'Дигноз при выписке': item.diag_dead
    };
  });

  // Returning the array of modified objects
  return modifiedObjects;
};

export function ArrivedOarTable(dataset) {

  const modifiedObjects = dataset.map(item => {
    return {
      'ФИО': item.pat_fio,
      '№ ИБ': item.ib_num,
      'Возраст': item.age,
      'Отделение': item.dept,
      'Лечащий врач': item.doc_fio,
      'Дигноз при поступлении': item.diag_start,

    };
  });

  return modifiedObjects;
};


export function MovedOarTable(dataset) {

  const modifiedObjects = dataset.map(item => {
    return {
      'ФИО': item.pat_fio,
      '№ ИБ': item.ib_num,
      'Возраст': item.age,
      'Отделение': item.dept,
      'Лечащий врач': item.doc_fio,
      'Дигноз при поступлении': item.diag_start,
      'Дата перевода': item.move_date,
      'Переведен из': item.from_dept
    };
  });

  return modifiedObjects;
};

export function CurrentOarTable(dataset) {

  const modifiedObjects = dataset.map(item => {
    return {
      'ФИО': item.pat_fio,
      '№ ИБ': item.ib_num,
      'Возраст': item.age,
      'Отделение': item.dept,
      'Койко дней': item.days,
      'Лечащий врач': item.doc_fio,
      'Дигноз при поступлении': item.diag_start
    };
  });

  return modifiedObjects;
};


