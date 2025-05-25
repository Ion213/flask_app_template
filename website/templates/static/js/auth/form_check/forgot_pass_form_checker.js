$(document).ready(function(){

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
            toggle_SendLink_Button()
        });
        toggle_SendLink_Button()
        function toggle_SendLink_Button() {
            const email = $('#email').val().trim();
            if (email) {
                $('#send_link-btn').prop('disabled', false);
            } else {
                $('#send_link-btn').prop('disabled', true);
            }
        }
        
})