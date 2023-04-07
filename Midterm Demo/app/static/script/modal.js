$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#task-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget); // Button that triggered the modal
        const airlineID = button.data('source'); // Extract info from data-* attributes
        const content = button.data('content'); // Extract info from data-* attributes
    
        const modal = $(this);
    
        if (airlineID) {
            modal.find('.modal-title').text('Edit name ' + airlineID);
            $('#task-form-display').data('airlineID', airlineID);
            modal.find('#airlineID-input').val(airlineID);
            modal.find('#name-input').val(content);
        } else {
            modal.find('.modal-title').text('New Name');
            $('#task-form-display').removeData('airlineID');
            modal.find('#airlineID-input').val('');
            modal.find('#name-input').val('');
        }
    });

    
    $('#submit-task').click(function () {
        const tID = $('#task-form-display').data('airlineID');
        const new_airlineID = $('#airlineID-input').val(); // Get the new airlineID from the form input
        const new_name = $('#name-input').val(); // Get the new name from the form input
    
        const url = tID ? '/edit/' + tID : '/create';
        const data = tID ? { 'old_airlineID': tID, 'airlineID': new_airlineID, 'name': new_name } : { 'airlineID': new_airlineID, 'name': new_name };
    
    
        $.ajax({
            type: 'POST',
            url: url,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify(data),
            success: function (res) {
                console.log(res.response)
                location.reload();
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




