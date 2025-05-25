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
            toggle_SendLink_Button()
        });
        toggle_SendLink_Button()
        function toggle_SendLink_Button() {
            const email = $('#email').val().trim();
            if (email) {
                $('#resend_reset_link-btn').prop('disabled', false);
            } else {
                $('#resend_reset_link-btn').prop('disabled', true);
            }
        }

    //-----------------------

    // Toggle Password Visibility
    $("#togglePassword").click(function () {
        let passwordField = $("#new_password");
        let icon = $(this).find("i");
        passwordField.attr("type", passwordField.attr("type") === "password" ? "text" : "password");
        icon.toggleClass("fa-eye fa-eye-slash");
    });
    $("#toggleConfirmPassword").click(function () {
        let confirmPasswordField = $("#confirm_new_password");
        let icon = $(this).find("i");
        confirmPasswordField.attr("type", confirmPasswordField.attr("type") === "password" ? "text" : "password");
        icon.toggleClass("fa-eye fa-eye-slash");
    });

    //check password stregnth
    $('#new_password').on('input', function () {
        const password = $(this).val().trim();
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{6,20}$/;
        if (password === '') {
            $('#password-strength').addClass('d-none').text('');
        } else if (!passwordRegex.test(password)) {
            $('#password-strength')
                .removeClass('d-none text-success')
                .addClass('text-danger')
                .text('Password must be 6–20 chars, includes: A-Z, a-z, 0-9, and symbol (e.g. @, #, $).✘');
        } else {
            $('#password-strength')
                .removeClass('d-none text-danger')
                .addClass('text-success')
                .text('Password is Valid✔');
        }
    });

    //check confirm  password matched
    $('#confirm_new_password, #new_password').on('input', function () {
        const password = $('#new_password').val().trim();
        const confirm_password = $('#confirm_new_password').val().trim();
        if (confirm_password === '') {
            $('#password-match').addClass('d-none').text('');
        } else if (password!==confirm_password) {
            $('#password-match')
                .removeClass('d-none text-success')
                .addClass('text-danger')
                .text('Passwords do not match.✘');
        } else {
            $('#password-match')
                .removeClass('d-none text-danger')
                .addClass('text-success')
                .text('Passwords match.✔');
        }
    });

    //check if password inputs are empty
    $('#new_password, #confirm_new_password').on('input', function () {
        toggle_ChangePass_Button()
    });
    toggle_ChangePass_Button()
    function toggle_ChangePass_Button() {
        const password = $('#new_password').val().trim();
        const confirm_password = $('#confirm_new_password').val().trim();
        if (password && confirm_password) {
            $('#change_pass-btn').prop('disabled', false);
        } else {
            $('#change_pass-btn').prop('disabled', true);
        }
    }

});
