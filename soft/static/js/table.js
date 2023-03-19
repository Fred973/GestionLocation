function searchTable() {
    var input, filter, table, tr, td, i;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    var rows = table.getElementsByTagName("tr");
    for (i = 1; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName("td");
        var j;
        var rowContainsFilter = false;
        for (j = 0; j < cells.length; j++) {
            if (cells[j]) {
                if (cells[j].innerHTML.toUpperCase().indexOf(filter) > -1) {
                    rowContainsFilter = true;
                    continue;
                }
            }
        }

        if (!rowContainsFilter) {
            rows[i].style.display = "none";
        } else {
            rows[i].style.display = "";
        }
    }
}

function sortTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("myTable");
    switching = true;
    //Set the sorting direction to ascending:
    dir = "asc";
    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
        //start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        /*Loop through all table rows (except the
        first, which contains table headers):*/
        for (i = 1; i < (rows.length - 1); i++) {
            //start by saying there should be no switching:
            shouldSwitch = false;
            /*Get the two elements you want to compare,
            one from current row and one from the next:*/
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            /*check if the two rows should switch place,
            based on the direction, asc or desc:*/
            if (dir == "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    //if so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    //if so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            /*If a switch has been marked, make the switch
            and mark that a switch has been done:*/
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            //Each time a switch is done, increase this count by 1:
            switchcount++;
        } else {
            /*If no switching has been done AND the direction is "asc",
            set the direction to "desc" and run the while loop again.*/
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}

$(document).ready(function () {
    $('#maxRows').on('change', function () {
        getPagination('#myTable', $(this).val());
    });
    getPagination('#myTable', 20); // the no of rows default you want to show
});

function getPagination(table, noRows) {

    $('.pagination').html(''); // reset pagination 
    var trnum = 0; // reset tr counter 
    var maxRows = noRows; // get Max Rows from select option
    var totalRows = $(table + ' tbody tr').length; // numbers of rows 
    $(table + ' tr:gt(0)').each(function () { // each TR in  table and not the header
        trnum++; // Start Counter 
        if (trnum > maxRows) { // if tr number gt maxRows

            $(this).hide(); // fade it out 
        }
        if (trnum <= maxRows) {
            $(this).show();
        } // else fade in Important in case if it ..
    }); //  was fade out to fade it in 
    if (totalRows > maxRows) { // if tr total rows gt max rows option
        var pagenum = Math.ceil(totalRows / maxRows); // ceil total(rows/maxrows) to get ..  
        //    numbers of pages 
        for (var i = 1; i <= pagenum;) { // for each page append pagination li 
            $('.pagination').append('<li class"wp" data-page="' + i + '">\
                                  <span>' + i++ + '<span class="sr-only">(current)</span></span>\
                                </li>').show();
        } // end for i 
    } // end if row count > max rows
    $('.pagination li:first-child').addClass('active'); // add active class to the first li 
    $('.pagination li').on('click', function () { // on click each page
        var pageNum = $(this).attr('data-page'); // get it's number
        var trIndex = 0; // reset tr counter
        $('.pagination li').removeClass('active'); // remove active class from all li 
        $(this).addClass('active'); // add active class to the clicked 
        $(table + ' tr:gt(0)').each(function () { // each tr in table not the header
            trIndex++; // tr index counter 
            // if tr index gt maxRows*pageNum or lt maxRows*pageNum-maxRows fade if out
            if (trIndex > (maxRows * pageNum) || trIndex <= ((maxRows * pageNum) - maxRows)) {
                $(this).hide();
            } else {
                $(this).show();
            } //else fade in 
        }); // end of for each tr in table
    }); // end of on click pagination list
}
