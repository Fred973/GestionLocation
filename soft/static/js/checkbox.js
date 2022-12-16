function ShowHideDayDiv(byDay) {
    var dayDiv = document.getElementById('dayDiv');
    var monthDiv = document.getElementById('monthDiv');
    dayDiv.style.display = byDay.checked ? "block" : "none"
    monthDiv.style.display = byDay.checked ? "none" : "block"
  }

  
  function ShowHideMonthDiv(byMonth) {
      var dayDiv = document.getElementById('dayDiv');
      var monthDiv = document.getElementById('monthDiv');
      dayDiv.style.display = byMonth.checked ? "none" : "block"
      monthDiv.style.display = byMonth.checked ? "block" : "none"
    }