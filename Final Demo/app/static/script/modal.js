$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    

// Click event for the "Add airline" button
$('#add-airline-button').click(function () {
    // Set the modal title and clear the form inputs
    $('#Label').text('Add Airline');
    $('#airlineID-input').val('');
    $('#name-input').val('');
    $('#task-modal').removeData('airlineID');
});

// Click event for the "Edit" buttons (use event delegation)
$('body').on('click', '.edit', function () {
    const airlineID = $(this).data('source');
    const name = $(this).data('content');
    $('#Label').text('Edit Airline');
    $('#airlineID-input').val(airlineID);
    $('#name-input').val(name);
    $('#task-modal').data('airlineID', airlineID);
});

// Click event for the "Submit" button
$('#submit-task').click(function () {
    const airlineID = $('#task-modal').data('airlineID');
    const new_airlineID = $('#airlineID-input').val();
    const new_name = $('#name-input').val();

    let url;
    let data;

    if (airlineID) {
        url = '/edit/' + airlineID;
        data = { 'old_airlineID': airlineID, 'airlineID': new_airlineID, 'name': new_name };
    } else {
        url = '/create';
        data = { 'airlineID': new_airlineID, 'name': new_name };
    }

    $.ajax({
        type: 'POST',
        url: url,
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(data),
        success: function (res) {
            console.log(res.response);
            if (res.success) {
                location.reload();
            } else {
                alert(res.response);
            }
        },
        error: function () {
            console.log('Error');
        }
    });
    
    
});

    
    
    
    
    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    
    // $('.state').click(function () {
    //     const state = $(this)
    //     const tID = state.data('source')
    //     const new_state
    //     if (state.text() === "In Progress") {
    //         new_state = "Complete"
    //     } else if (state.text() === "Complete") {
    //         new_state = "Todo"
    //     } else if (state.text() === "Todo") {
    //         new_state = "In Progress"
    //     }

    //     $.ajax({
    //         type: 'POST',
    //         url: '/edit/' + tID,
    //         contentType: 'application/json;charset=UTF-8',
    //         data: JSON.stringify({
    //             'status': new_state
    //         }),
    //         success: function (res) {
    //             console.log(res)
    //             location.reload();
    //         },
    //         error: function () {
    //             console.log('Error');
    //         }
    //     });
    // });

});




