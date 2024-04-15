/* This code shows and hides password in login page */
function togglePassword1() {
        var confirm_passwordInput = document.getElementById("confirm_password-input");
        if (confirm_passwordInput.type === "password") {
            confirm_passwordInput.type = "text";
        } else {
            confirm_passwordInput.type = "password";
        }
    }


 function showDiv(divId) {
    var div = document.getElementById(divId);
    div.style.display = "block"; // Show the div

    // Hide the content of the other buttons
    var sidebarLinks = document.querySelectorAll(".sidebar a");
    for (var i = 0; i < sidebarLinks.length; i++) {
      var link = sidebarLinks[i];
      if (link.getAttribute("href") !== "#" + divId) {
        var contentId = link.getAttribute("href").substring(1);
        var contentDiv = document.getElementById(contentId);
        contentDiv.style.display = "none";
      }
    }
  }

  // Show the content of the "Dashboard" button by default
//  window.onload = function() {
//    showDiv('dashboard');
//  };





// script code for connection type select options
function showHideBlock() {
      var selectBox = document.getElementById("connection");
      var selectedValue = selectBox.options[selectBox.selectedIndex].value;


      // Get all the block elements
      var blocks = document.getElementsByClassName("myBlock");

      // Hide all blocks
      for (var i = 0; i < blocks.length; i++) {
        blocks[i].style.display = "none";
      }

      // Show the selected block based on the selected value
      if (selectedValue !== "") {
        var selectedBlock = document.getElementById(selectedValue);
        if (selectedBlock) {
          selectedBlock.style.display = "block";
        }
      }
    }



/* script for Monitor Block*/
var isRunning = false;

    function start() {
      isRunning = true;
      document.getElementById("startButton").style.display = "none";
      document.getElementById("stopButton").style.display = "inline";
      document.getElementById("status").textContent = "RF Module Status: Running";
    }

    function stop() {
      isRunning = false;
      document.getElementById("startButton").style.display = "inline";
      document.getElementById("stopButton").style.display = "none";
      document.getElementById("status").textContent = "RF Module Status: Stopped";
    }


/* JS code for getting dashboard block on loading main url starts here*/

  window.addEventListener('DOMContentLoaded', function() {
      // Get the URL fragment identifier (the part after the # symbol)
      var fragment = window.location.hash.substr(1);

      // Show the block with the corresponding ID
      if (fragment) {
        var block = document.getElementById(fragment);
        if (block) {
          block.style.display = 'block';

        }
      } else {
        // If no fragment identifier, show the first block by removing the "display: none" style
        var firstBlock = document.querySelector('#users');
        if (firstBlock) {
          firstBlock.style.display = 'block';
        }
      }
    });


/* JS code for api integration page*/

// Get the checkbox and related block elements
const toggleCheckbox = document.getElementById("toggle_input5");
const relatedBlock = document.getElementById("myDIV");

// Add an event listener to the checkbox
//toggleCheckbox.addEventListener("change", function() {
//  // If the checkbox is checked, show the related block; otherwise, hide it
//  if (toggleCheckbox.checked) {
//    relatedBlock.style.display = "block";
//  } else {
//    relatedBlock.style.display = "none";
//  }
//});

/*  Js code for password input tag in login page starts here */
/* This code shows and hides password in login page */
function togglePassword() {
        var passwordInput = document.getElementById("password-input");
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
        } else {
            passwordInput.type = "password";
        }
    }

/* JS code for tabs on User Config page  */
const triggerTabList = document.querySelectorAll('#myTab button')
triggerTabList.forEach(triggerEl => {
  const tabTrigger = new bootstrap.Tab(triggerEl)

  triggerEl.addEventListener('click', event => {
    event.preventDefault()
    tabTrigger.show()
  })
})



function showTab(tabId) {
      // Hide all tab content blocks
      var tabContent = document.getElementsByClassName('tab-content');
      for (var i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = 'none';
      }

      // Show the selected tab content block
      var selectedTabContent = document.getElementById(tabId);
      selectedTabContent.style.display = 'block';
    }

function showTab1(tabId) {
      // Hide all tab content blocks
      var tabContent = document.getElementsByClassName('tab-content1');
      for (var i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = 'none';
      }

      // Show the selected tab content block
      var selectedTabContent = document.getElementById(tabId);
      selectedTabContent.style.display = 'block';
    }


/* Js Code for checking password and confirm password are matched or not */
$(document).ready(function() {
  // Function to check if password and confirm_password fields match
  function validatePassword() {
    var password = $("#password").val();
    var confirm_password = $("#confirm_password").val();

    if (password !== confirm_password) {
      $("#password_error").text("Password and Confirm Password do not match!!!");
    } else {
      $("#password_error").text("");
    }
  }

  // Call the validatePassword function whenever the fields are changed
  $("#password, #confirm_password").on("keyup", validatePassword);
});

/* JS Code for date pickers in data report tab */
 $(function() {
    $("#fromDate").datepicker({
      dateFormat: "yy-mm-dd",
      onSelect: function(selectedDate) {
        $("#toDate").datepicker("option", "minDate", selectedDate);
      }
    });

    $("#toDate").datepicker({
      dateFormat: "yy-mm-dd",
      onSelect: function(selectedDate) {
        $("#fromDate").datepicker("option", "maxDate", selectedDate);
      }
    });

  });




/*  Js code for geting data between two dates */
$(document).ready(function() {
    // Function to send a request to start RFID reading
    function startReading() {
        var fromdate = $('#fromDate').val(); // Get the from date from an input field
        var todate = $('#toDate').val(); // Get the to date from an input field

        $.ajax({
            type: 'GET',
            url: '/get_report',
            data: {
                fromdate: fromdate,
                todate: todate
            },
            success: function(response) {
                // Parse the JSON response into an array of objects
                var data = JSON.parse(response);
//                console.log(data);

                // Generate the table structure
                var table = '<table class="table table-bordered"><thead class="table-dark"><tr><th>Sr.No</th><th>Tag Data</th><th>Date & Time</th><th>Status</th><th>Store ID</th><th>Reader No.</th></tr></thead><tbody>';

                for (var i = 0; i < data.length; i++) {
                    var row = data[i];
                    var srno = row.id; // Assuming 'id' is the key for the Sr.No column
                    var tag_data = row.tag_data; // Assuming 'tag_data' is the key for the Tag Data column
                    var datetime = row.datetime; // Assuming 'datetime' is the key for the Date & Time column
                    var status = row.status; // Assuming 'status' is the key for the Status column
                    var storeid = row.storeid; // Assuming 'storeid' is the key for the Store ID column
                    var reader_no = row.reader_no; // Assuming 'reader_no' is the key for the Reader No. column

                    table += '<tr><td>' + srno + '</td><td>' + tag_data + '</td><td>' + datetime + '</td><td>' + status + '</td><td>' + storeid + '</td><td>' + reader_no + '</td></tr>';
                }
                table += '</tbody></table>';

                // Display the table
                $('#response-content').html(table);
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    }

    // Event listener for the Generate Report button click
    $('#generateReport').click(function() {
        startReading();
    });
});


/* JS code for exporting table data into csv file format*/
$(document).ready(function() {
    // Function to send a request to start RFID reading
    function startExport() {
        var fromdate = $('#fromDate').val(); // Get the from date from an input field
        var todate = $('#toDate').val(); // Get the to date from an input field
        console.log(fromdate, todate);
        $.ajax({
            type: 'POST',
            url: '/export_report',
            data: { 'fromdate': fromdate, 'todate': todate },
            success: function(response) {
                console.log(response);
                if (response.filePath) {
                    // Redirect to the download link
                    window.location.href = '/' + response.filePath;

                } else {
                    alert('Export failed!');
                }
            },
            error: function() {
                alert('Export failed!');
            }
        });
    }

    // Event listener for the Generate Report button click
    $('#exportReport').click(function() {
        startExport();
    });
});



/* JS code for  showing rfid tag info*/
//$(document).ready(function() {
//    // Handle click event on RFID tag number
//    $('.rfidNumber').click(function() {
//        var tagNumber = $(this).text().trim();
//        console.log(tagNumber)
//        // Make an AJAX request to Flask route to retrieve RFID tag information
//        $.ajax({
//            url: '/rfid_info/' + encodeURIComponent(tagNumber),
//            type: 'GET',
//            success: function(response) {
//            console.log(response)
//            var html = '<p>Date and Time: ' + response.datetime + '</p>' +
//               '<p>ID: ' + response.id + '</p>' +
//               '<p>Reader Number: ' + response.reader_no + '</p>' +
//               '<p>Status: ' + response.status + '</p>' +
//               '<p>Store ID: ' + response.storeid + '</p>';
//               //'<p>Product Image: ' + response.product_image + '</p>';
//                // Update the div with the retrieved RFID tag information
//            // Display the binary image on the UI
////            var blob = new Blob([response.product_image], { type: 'image/jpeg' });
////            var imageURL = URL.createObjectURL(blob);
////            html += '<p>Product Image: <img src="' + imageURL + '"/></p>';
//            $('#rfidInfoDiv').html(html);
//            }
//        });
//    });
//});
//$(document).ready(function() {
//    // Handle click event on RFID tag number
//    $('.rfidNumber').click(function() {
//        var tagNumber = $(this).text().trim();
//        console.log(tagNumber);
//        // Make an AJAX request to Flask route to retrieve RFID tag information
//        $.ajax({
//            url: '/rfid_info/' + encodeURIComponent(tagNumber),
//            type: 'GET',
//            //dataType: 'blob',
//            success: function(response) {
//            console.log(response)
//            console.log(response.product_image)
//                var html = '<p>Date and Time: ' + response.datetime + '</p>' +
//                           '<p>ID: ' + response.id + '</p>' +
//                           '<p>Reader Number: ' + response.reader_no + '</p>' +
//                           '<p>Status: ' + response.status + '</p>' +
//                           '<p>Store ID: ' + response.storeid + '</p>';
////                           '<p>Image: <img src="' + response.product_image + '" alt="Image" /></p>';
//
//                // Update the div with the retrieved RFID tag information
//                $('#rfidInfoDiv').html(html);
//                // Set the image source in the "opencv_image" div
//                $('#opencv_image').html('<img style="height:100%;" src="' + response.product_image + '" alt="Image" />');
//
//            }
//        });
//    });
//});

//$(document).ready(function() {
//    // Handle click event on table row
//    $('tbody').on('click', 'tr', function() {
//        var tagNumber = $(this).find('.rfidNumber button').text().trim();
//        console.log(tagNumber);
//        // Make an AJAX request to Flask route to retrieve RFID tag information
//        $.ajax({
//            url: '/rfid_info/' + encodeURIComponent(tagNumber),
//            type: 'GET',
//            success: function(response) {
//                console.log(response);
//                console.log(response.product_image);
//                var html = '<p>Date and Time: ' + response.datetime + '</p>' +
//                           '<p>ID: ' + response.id + '</p>' +
//                           '<p>Reader Number: ' + response.reader_no + '</p>' +
//                           '<p>Status: ' + response.status + '</p>' +
//                           '<p>Store ID: ' + response.storeid + '</p>';
//
//                // Update the div with the retrieved RFID tag information
//                $('#rfidInfoDiv').html(html);
//                // Set the image source in the "opencv_image" div
//                $('#opencv_image').html('<img style="height:100%;" src="' + response.product_image + '" alt="Image" />');
//            }
//        });
//    });
//});
/* js code for showing rfid tag info in rfid description box under the rfid tag data table, also it gives current row id of table*/
//$(document).ready(function() {
//    // Handle click event on table row
//    $('tbody').on('click', 'tr', function() {
//        var tagNumber = $(this).find('.rfidNumber button').text().trim();
//        console.log(tagNumber);
//
//        // Get the ID of the parent row
//        var rowId = $(this).attr('class').split('-')[1];
//        console.log(rowId);
//
//        // Make an AJAX request to Flask route to retrieve RFID tag information
//        $.ajax({
//            url: '/rfid_info/' + encodeURIComponent(tagNumber) + '/' + rowId,
//            type: 'GET',
//            success: function(response) {
//                console.log(response);
//                console.log(response.product_image);
//                var html = '<p>Date and Time: ' + response.datetime + '</p>' +
//                           '<p>ID: ' + rowId + '</p>' +
//                           '<p>Reader Number: ' + response.reader_no + '</p>' +
//                           '<p>Status: ' + response.status + '</p>' +
//                           '<p>Store ID: ' + response.storeid + '</p>';
//
//                // Update the div with the retrieved RFID tag information
//                $('#rfidInfoDiv').html(html);
//                // Set the image source in the "opencv_image" div
//                $('#opencv_image').html('<img style="height:100%;" src="' + response.product_image + '" alt="Image" />');
//            }
//        });
//    });
//});

$(document).ready(function() {
    // Handle click event on table row
    $('tbody').on('click', 'tr', function() {
        // Get the ID of the parent row
//        var rowId = $(this).attr('class').split('-')[1];
        var rowId = $(this).closest('tr').data('row-id');
        console.log(rowId);

        // Make an AJAX request to Flask route to retrieve RFID tag information
        $.ajax({
            url: '/rfid_info/' + rowId,
            type: 'GET',
            success: function(response) {
                console.log(response);
//                console.log(response.product_image);
                var html = '<p>Date and Time: ' + response.datetime + '</p>' +
                           '<p>ID: ' + rowId + '</p>' +
                           '<p>Tag Number: ' + response.tag_data + '</p>' +
                           '<p>Reader Number: ' + response.reader_no + '</p>' +
                           '<p>Status: ' + response.status + '</p>' +
                           '<p>Store Code: ' + response.storecode + '</p>';

                // Update the div with the retrieved RFID tag information
                $('#rfidInfoDiv').html(html);
                // Set the image source in the "opencv_image" div
                $('#opencv_image').html('<img style="height:100%;" src="' + response.product_image + '" alt="Image" onclick="openImageInNewWindow(this)"/>');
            }
        });
    });
});


/* JS code for pagination for tag data table in dashboard page */
$(function(){
  $('#response-content').createTablePagination({
    rowPerPage: 10,
    paginationColor: '#6f7ad7',
    fontColor: '#555555',
    paginationStyle: 'borderless', // or 'bordered'
  });
});


/* JS code for pagination for tag data table in index page for users table */
$(function(){
  $('#users_table').createTablePagination({
    rowPerPage: 10,
    paginationColor: '#6f7ad7',
    fontColor: '#555555',
    paginationStyle: 'borderless', // or 'bordered'
  });
});

/* JS code for pagination for tag data table in index page for stores table */
$(function(){
  $('#stores_table').createTablePagination({
    rowPerPage: 10,
    paginationColor: '#6f7ad7',
    fontColor: '#555555',
    paginationStyle: 'borderless', // or 'bordered'
  });
});

/* JS code for pagination for event table in index page for event table */
$(function(){
  $('#event-table').createTablePagination({
    rowPerPage: 10,
    paginationColor: '#6f7ad7',
    fontColor: '#555555',
    paginationStyle: 'borderless', // or 'bordered'
  });
});

/* JS code for searching store list based on store name in search input */

jQuery(document).ready(function($){

$('.store_names li').each(function(){
$(this).attr('data-search-term', $(this).text().toLowerCase());
});

$('#search_store_input').on('keyup', function(){

var searchTerm = $(this).val().toLowerCase();

    $('.store_names li').each(function(){

        if ($(this).filter('[data-search-term *= ' + searchTerm + ']').length > 0 || searchTerm.length < 1) {
            $(this).show();
        } else {
            $(this).hide();
        }

    });

});

});


/* JS ajax code for printing table data from fromdate to todate */

//$(document).ready(function() {
//    // Function to send a request to print data
//    function printData() {
//        var fromdate = $('#fromDate').val(); // Get the from date from an input field
//        var todate = $('#toDate').val(); // Get the to date from an input field
//        console.log(fromdate, todate);
//        $.ajax({
//            type: 'POST',
//            url: '/print_data',
//            data: { 'fromdate': fromdate, 'todate': todate },
//            success: function(response) {
//                console.log(response);
//                if (response.data) {
//                    // Open a new window with the data for printing
//                    var printWindow = window.open('', '_blank');
//                    printWindow.document.open();
//                    printWindow.document.write('<html><head><title>Print Data</title></head><body>');
//                    printWindow.document.write('<pre>' + JSON.stringify(response.data, null, 2) + '</pre>');
//                    printWindow.document.write('</body></html>');
//                    printWindow.document.close();
//                    printWindow.print();
//                    printWindow.close();
//
//                    alert('Printing Completed');
//                } else {
//                    alert('Printing failed!');
//                }
//            },
//            error: function() {
//                alert('Printing failed!');
//            }
//        });
//    }
//
//    // Event listener for the Print Data button click
//    $('#printReport').click(function() {
//        printData();
//    });
//});


/* JS ajax code for printing table data from fromdate to todate  in borderless table format*/
//$(document).ready(function() {
//    // Function to send a request to print data
//    function printData() {
//        var fromdate = $('#fromDate').val(); // Get the from date from an input field
//        var todate = $('#toDate').val(); // Get the to date from an input field
//        console.log(fromdate, todate);
//        $.ajax({
//            type: 'POST',
//            url: '/print_data',
//            data: { 'fromdate': fromdate, 'todate': todate },
//            success: function(response) {
//                console.log(response);
//                if (response.data) {
//                    // Open a new window with the data for printing
//                    var printWindow = window.open('', '_blank');
//                    printWindow.document.open();
//                    printWindow.document.write('<html><head><title>Print Data</title></head><body>');
//                    printWindow.document.write('<table>');
//                    printWindow.document.write('<tr>');
//                    for (var key in response.data[0]) {
//                        printWindow.document.write('<th>' + key + '</th>');
//                    }
//                    printWindow.document.write('</tr>');
//                    for (var i = 0; i < response.data.length; i++) {
//                        printWindow.document.write('<tr>');
//                        for (var key in response.data[i]) {
//                            printWindow.document.write('<td>' + response.data[i][key] + '</td>');
//                        }
//                        printWindow.document.write('</tr>');
//                    }
//                    printWindow.document.write('</table>');
//                    printWindow.document.write('</body></html>');
//                    printWindow.document.close();
//                    printWindow.print();
//                    printWindow.close();
//
//                    alert('Printing Completed');
//                } else {
//                    alert('Printing failed!');
//                }
//            },
//            error: function() {
//                alert('Printing failed!');
//            }
//        });
//    }
//
//    // Event listener for the Print Data button click
//    $('#printReport').click(function() {
//        printData();
//    });
//});

/* JS ajax code for printing table data from fromdate to todate  in bordered table format*/
$(document).ready(function() {
    // Function to send a request to print data
    function printData() {
        var fromdate = $('#fromDate').val(); // Get the from date from an input field
        var todate = $('#toDate').val(); // Get the to date from an input field
        console.log(fromdate, todate);
        $.ajax({
            type: 'POST',
            url: '/print_data',
            data: { 'fromdate': fromdate, 'todate': todate },
            success: function(response) {
                console.log(response);
                if (response.data) {
                    // Open a new window with the data for printing
                    var printWindow = window.open('', '_blank');
//                    printWindow.document.open();
                    printWindow.document.write('<html><head><title>Print Data</title>');
                    printWindow.document.write('<style>');
                    printWindow.document.write('table { border-collapse: collapse; width: 100%; }');
                    printWindow.document.write('th, td { border: 1px solid black; padding: 8px; }');
                    printWindow.document.write('</style>');
                    printWindow.document.write('</head><body>');
                    printWindow.document.write('<table>');
                    printWindow.document.write('<tr>');
                    for (var key in response.data[0]) {
                        printWindow.document.write('<th>' + key + '</th>');
                    }
                    printWindow.document.write('</tr>');
                    for (var i = 0; i < response.data.length; i++) {
                        printWindow.document.write('<tr>');
                        for (var key in response.data[i]) {
                            printWindow.document.write('<td>' + response.data[i][key] + '</td>');
                        }
                        printWindow.document.write('</tr>');
                    }
                    printWindow.document.write('</table>');
                    printWindow.document.write('</body></html>');
                    printWindow.document.close();
                    printWindow.print();
                    printWindow.close();

                    alert('Printing Completed');
                } else {
                    alert('Printing failed! Please select From Date and To Date.');
                }
            },
            error: function() {
                alert('Printing failed! ');
            }
        });
    }

    // Event listener for the Print Data button click
    $('#printReport').click(function() {
        printData();
    });
});

/* JS code for getting table data based on store name*/

$(document).ready(function() {
        $('.storebtn').click(function() {
            var storeName = $(this).text();
//            console.log(storeName)
            $.ajax({
                url: '/get_table_data',
                type: 'POST',
                data: { store_name: storeName },
                success: function(response) {
//                console.log(response)
                    updateTable(response);
                },
                error: function(xhr) {
//                    console.log(xhr.responseText);
                }
            });
        });

        function updateTable(data) {
            var tableBody = $('#response-content tbody');
            tableBody.empty();

            $.each(data, function(index, row) {
            var statusColorClass = row.status === 'Unbilled' ? 'red' : 'green';
                var rowData = '<tr>' +
                    '<td>' + row.id + '</td>' +
                    '<td>' + row.tag_data + '</td>' +
                    '<td>' + row.datetime + '</td>' +
                    '<td class="' + statusColorClass + '">' + row.status + '</td>' +
                    '<td>' + row.storecode + '</td>' +
                    '<td>' + row.reader_no + '</td>' +
                    '<td>' + row.gate_no + '</td>' +
                    '<td>' + row.bill_no + '</td>' +
                    '</tr>';

                tableBody.append(rowData);
            });
        }
    });


/* JS code for showing image in full size in new browser window */
function openImageInNewWindow(imageElement) {
    // Get the image source from the clicked element
    var imageUrl = imageElement.src;

    // Open the image in a new window
    var newWindow = window.open(imageUrl, '_blank');

    // Ensure that the new window is not null
    if (newWindow !== null) {
        newWindow.focus();
    } else {
        alert("Your browser blocked opening a new window. Please allow pop-ups for this site.");
    }
}

/* JS code for adding input box on clicking + button on email config modal*/

$("#add_input").click(function () {
            newRowAdd =
                '<br/> ' +
                '<div class="from-group" id="cc_input" style="display:flex;">' +
                '<input type="text" placeholder="Enter CC Email" name="ccmails[]" class="form-control m-input">' +
                '<button class="btn btn-danger" id="DeleteRow" type="button"> ' +
                '<i class="bi bi-trash"></i> - </button></div><br/>';

            $('#newinput').append(newRowAdd);
        });
        $("body").on("click", "#DeleteRow", function () {
            $(this).parents("#cc_input").remove();
        })