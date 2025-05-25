$(document).ready(function () {

    // Toggle Password Visibility
    $("#togglePassword").click(function () {
        let passwordField = $("#password");
        let icon = $(this).find("i");
        passwordField.attr("type", passwordField.attr("type") === "password" ? "text" : "password");
        icon.toggleClass("fa-eye fa-eye-slash");
    });
    
    /*
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
    */

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
    $('#email, #password').on('input', function () {
        toggleLoginButton();
    });
    toggleLoginButton();
    function toggleLoginButton() {
        const email = $('#email').val().trim();
        const password = $('#password').val().trim();

        if (email && password) {
            $('#login-btn').prop('disabled', false);
        } else {
            $('#login-btn').prop('disabled', true);
        }
    }

});
