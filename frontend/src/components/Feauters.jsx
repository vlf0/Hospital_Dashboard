import { format, subHours } from 'date-fns';
import { formatDate } from './dates/DatesFormat';

export const currentDatetime = new Date().toLocaleDateString('ru-RU');


export function DateFormatting(date) {
  const dateTimeObject = new Date(date);
  const subtractedDate = subHours(dateTimeObject, 3);
  const formattedSubtractedDate = format(subtractedDate, 'dd.MM.yyyy HH:mm:ss');
  return formattedSubtractedDate
};


export function CustomMap(currentDay, yesterday, branch) {

  let result;

  if (currentDay[branch] === null || yesterday[branch] === null) {
    result = ['null', 'null', 'null']
  } else {
    result = [currentDay[branch], yesterday[branch], Persents(currentDay[branch], yesterday[branch])]
  }
  return result
};


export function Persents(today, yesterday) {
    const result = today-yesterday;
    yesterday = (yesterday === 0) ? today : yesterday;
    let percent = (result/yesterday*100).toFixed(1);
    percent = percent.toString() + '%';
    percent = percent.replace('-', '');
    return percent
};


export const extractProperty = (dataList, key) => {
    return dataList.map(item => item[key]);
};


export const extractProperties = (dataList, propertyKey) => {
  return dataList.map(item => ({ dates: item.dates, [propertyKey]: item[propertyKey] }));
};


export const extractDetailsProperties = (dataList, propertyKey) => {
  return dataList.map(item => {
    const propertyValue = item[propertyKey];
    const registeredPatients = propertyValue && propertyValue['registered_patients'] ? propertyValue['registered_patients'] : null;
    
    return { dates: item.dates, [propertyKey]: registeredPatients };
  });
};


export function mapArrivedValues(data, dateArray, propertyKey) {
  const result = Array(dateArray.length).fill(null);

  data.forEach(item => {
    const index = dateArray.indexOf(item.dates);
    if (index !== -1) {
      result[index] = item[propertyKey];
    }
  });

  return result;
}

  
export function ensureArrayLength(array, desiredLength) {
  if (array.length !== desiredLength) {
    const numberOfTimesToInsert = desiredLength - array.length;

    for (let i = 0; i < numberOfTimesToInsert; i++) {
      array.unshift(null);
    }
  }
};

export function RefuseDetailTableProcess(dataset) {

  const modifiedObjects = dataset.map(item => {
    return {
      'ФИО пациента': item.pat_fio,
      '№ ИБ': item.ib_num,
      'ФИО врача': item.doc_fio,
      'Диагноз': item.diag,
      'Причина отказа': item.refuse_reason,
      'Дата отказа': DateFormatting(item.refuse_date)
    };
  });  
  
  return modifiedObjects;
};

export function TotalRefuseTableProcess(dataset) {

  const modifiedObjects = dataset.map(item => {
    return {
      'ФИО врача': item.doc_fio,
      'кол-во отказов': item.refuses_amount
    };
  });  
  
  return modifiedObjects;
};

export function EmergencyTableProcess(dataset) {

  const modifiedObjects = dataset.map(item => {
    return {
      'ФИО пациента': item.pat_fio,
      '№ ИБ': item.ib_num,
      'Отделение': item.dept,
      'Время ожидания': item.waiting_time,
      'ФИО врача': item.doc_fio
    };
  });  
  
  return modifiedObjects;
};

export function DeadTableProcess(dataset) {
  // Using map to transform each item in the dataset
  const modifiedObjects = dataset.map(item => {
    return {
      'ФИО': item.pat_fio,
      '№ ИБ': item.ib_num,
      'Пол': item.sex,
      'Возраст': item.age,
      'Отделение': item.dept,
      'Дата поступления': DateFormatting(item.arriving_dt),
      'Состояние при поступлении': item.state,
      'Кол-во койко дней': item.days,
      'Диaгноз при поступлении': item.diag_arr,
      'Диaгноз при выписке': item.diag_dead,
      'Лечащий врач': item.doc_fio
    };
  });

  return modifiedObjects;
};

export function PlanHospProcess(dataset) {
  const modifiedObjects = dataset.map(item => {
    return {
      'Отделение': item.dept,
      'Пн': item.mon,
      'Вт': item.tue,
      'Ср': item.wed,
      'Чт': item.thu,
      'Пт': item.fri,
      'Сб': item.sat,
      'Вс': item.sun,
      'Вне диапазона': item.other
    };
  });

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
      'Диагноз при поступлении': item.diag_start,

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
      'Диагноз при поступлении': item.diag_start,
      'Дата перевода': DateFormatting(item.move_date),
      'Переведён из': item.from_dept
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
      'Диагноз при поступлении': item.diag_start
    };
  });

  return modifiedObjects;
};


export function DeadsOarTable(dataset) {

  const modifiedObjects = dataset.map(item => {
    return {
      'ФИО': item.pat_fio,
      '№ ИБ': item.ib_num,
      'Пол': item.sex,
      'Возраст': item.age,
      'Отделение': item.dept,
      'Дата поступления': DateFormatting(item.arriving_dt),
      'Состояние при поступлении': item.state,
      'Кол-во койко дней': item.days,
      'Диагноз при поступлении': item.diag_arr,
      'Диагноз при выписке': item.diag_dead
    };
  });

  return modifiedObjects;
};


export function GetNameOfDay(dateString) {
  return ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
  [new Date(dateString).getDay()];
}


export function getMainDMK(dmkData, day) {

    let today = new Date();
    let yesterday = new Date();
    yesterday.setDate(today.getDate() - 1)
  
    const currentTime = today.toLocaleTimeString();
    const currentHour = currentTime.split(':')[0];
  
    if (day === 'yesterday') {
      today.setDate(today.getDate() - 1);
      yesterday.setDate(yesterday.getDate() - 1);
    } 
  
    let formattedDate;
    currentHour >= 6 ? formattedDate = formatDate(today) : formattedDate = formatDate(yesterday);
  
    let mainDMK;
    const index = dmkData.findIndex(item => item.dates === formattedDate);
  
    if (index !== -1) {
      mainDMK = dmkData[index];
    } else {
      mainDMK = { dates: formattedDate, arrived: null, hosp: null, refused: null,
                  signout: null, deads: null, reanimation: null };
    }
    
    return mainDMK;
}

export function getOrderedWeekDays() {
  const days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
  const currentDayIndex = (new Date().getDay() + 6) % 7;
  return days.slice(currentDayIndex).concat(days.slice(0, currentDayIndex));
}

