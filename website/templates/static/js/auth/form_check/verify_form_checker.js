$(document).ready(function () {

    //check email format
    $('#email').on('input', function () {
        const email = $(this).val();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (email === '') {
            $('#email-format').addClass('d-none').text('');   
         } else if (!emailRegex.test(email)) {
            $('#email-format')
                .removeClass('d-none text-success')
                .addClass('text-danger')
                .text('Enter a valid email address (e.g. user@example.com).✘')
        } else {
            $('#email-format')
                .removeClass('d-none text-danger')
                .addClass('text-success')
                .text('Email format is Valid✔');
        }
    });
    
    //check input if empty disable the button
    $('#email').on('input', function () {
        toggleResendButton()
    });
    toggleResendButton()
    function toggleResendButton() {
        const email = $('#email').val().trim();
        if (email) {
            $('#resend-btn').prop('disabled', false);
        } else {
            $('#resend-btn').prop('disabled', true);
        }
    }

});
