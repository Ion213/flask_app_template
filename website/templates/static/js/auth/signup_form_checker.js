$(document).ready(function(){
    

    // Toggle Password Visibility
    $("#togglePassword").click(function () {
        let passwordField = $("#password");
        let icon = $(this).find("i");
        passwordField.attr("type", passwordField.attr("type") === "password" ? "text" : "password");
        icon.toggleClass("fa-eye fa-eye-slash");
    });
    $("#toggleConfirmPassword").click(function () {
        let confirmPasswordField = $("#confirm_password");
        let icon = $(this).find("i");
        confirmPasswordField.attr("type", confirmPasswordField.attr("type") === "password" ? "text" : "password");
        icon.toggleClass("fa-eye fa-eye-slash");
    });

    //check password stregnth
    $('#password').on('input', function () {
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
    $('#confirm_password, #password').on('input', function () {
        const password = $('#password').val().trim();
        const confirm_password = $('#confirm_password').val().trim();
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


    // Student ID Format Validation
    $('#user_id').on('input', function () {
        const user_id = $(this).val();
        const userIdRegex = /^\d+(?:-\d+)+$/;

        if (user_id === '') {
            $('#id-format').addClass('d-none').text('');   
         } else if (!userIdRegex.test(user_id)) {
            $('#id-format')
                .removeClass('d-none text-success')
                .addClass('text-danger')
                .text('User ID must contain numbers separated by hyphens (e.g., 2017-21-00062).✘')
        } else {
            $('#id-format')
                .removeClass('d-none text-danger')
                .addClass('text-success')
                .text('ID format is Valid✔');
        }
    });


    //check input if empty disable the button
    $('#email, #password, #first_name, #last_name').on('input', function () {
        toggleSignupButton();
    });
    toggleSignupButton();
    function toggleSignupButton() {
        const email = $('#email').val().trim();
        const password = $('#password').val().trim();
        const first_name = $('#first_name').val().trim();
        const last_name = $('#last_name').val().trim();

        if (email && password && first_name && last_name) {
            $('#signup-btn').prop('disabled', false);
        } else {
            $('#signup-btn').prop('disabled', true);
        }
    }
})