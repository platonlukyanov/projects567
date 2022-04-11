function decOfNum(number, titles)
    {
        var decCache = [],
        decCases = [2, 0, 1, 1, 1, 2];
        if(!decCache[number]) decCache[number] = number % 100 > 4 && number % 100 < 20 ? 2 : decCases[Math.min(number % 10, 5)];
        return titles[decCache[number]];
    }
function format_date(datestring) {
    var date = new Date(datestring);
    var delta = Math.floor((new Date() - date) / 1000);
    var minute = 60,
        hour = minute * 60,
        day = hour * 24,
        week = day * 7;
        month = day * 30;
        year = month * 12;


    var datestring;

    if (delta < 30) {
        datestring = 'только что';
    } else if (delta < minute) {
        datestring = delta + " " + decOfNum(delta, ['секунду', 'секунды', 'секунд']) + " назад";
    } else if (delta < 2 * minute) {
        datestring = 'минуту назад'
    } else if (delta < hour) {
        datestring = Math.floor(delta / minute) + " " + decOfNum(Math.floor(delta / minute), ["минуту", "минуты", "минут"]) + ' назад';
    } else if (Math.floor(delta / hour) == 1) {
        datestring = 'час назад'
    } else if (delta < day) {
        datestring = Math.floor(delta / hour) + " " + decOfNum(Math.floor(delta / hour), ["час", "часа", "часов"]) + ' назад';
    } else if (delta < day * 2) {
        datestring = 'вчера';
    }
    else if (delta < week) {
        datestring = Math.floor(delta / day) + " " + decOfNum(Math.floor(delta / day), ["день", "дня", "дней"]) + ' назад';
    }
    else if (delta < week * 2) {
        datestring = "неделю назад";
    }
    else if (delta < month) {
        datestring = Math.floor(delta / week) + " " + decOfNum(Math.floor(delta / week), ["неделю", "недели", "недель"]) + ' назад';
    }
    else if (delta < year) {
        datestring = Math.floor(delta / month) + " " + decOfNum(Math.floor(delta / month), ["месяц", "месяца", "месяцев"]) + ' назад';
    }
    else if (delta < year * 2) {
        datestring = "год назад";
    }
    else if (delta > year) {
        datestring = Math.floor(delta / year) + " " + decOfNum(Math.floor(delta / year), ["год", "года", "лет"]) + ' назад';
    }
    return datestring;
}