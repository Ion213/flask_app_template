$(document).ready(function () {
    
    const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    axios.defaults.headers.common['X-CSRFToken'] = csrf_token;


    $('.signup-nav-btn').hide();

    // Reusable SweetAlert2 dialog
    function customSwal(title, message, icon = 'info', timer = 3000) {
        Swal.fire({
            icon: icon,
            title: `<span style="font-size: 1.5rem;">${title}</span>`,
            html: `<div style="font-size: 1.1rem;">${message}</div>`,
            showConfirmButton: true,
            timer: timer,
            customClass: {
                popup: 'custom-swal-popup'
            }
        });
    }
//--------------

    // signup submit
    $('#signup_form').on('submit', function (e) {
        e.preventDefault();
    
        const first_name = $('#first_name').val();
        const last_name = $('#last_name').val();
        const user_id = $('#user_id').val();
        const email = $('#email').val();
        const password = $('#password').val();
        const confirm_password = $('#confirm_password').val();

        submit_signup(first_name, last_name,user_id, email, password,confirm_password);
    });

    function submit_signup(first_name, last_name,user_id, email, password,confirm_password) {
        axios.post('/auth/signup_submit', { 
                first_name: first_name, 
                last_name: last_name, 
                user_id:user_id,
                email: email, 
                password: password, 
                confirm_password: confirm_password 
            }
        )

            .then(function (response) {
                if (response.data.success) {
                    customSwal('',`${response.data.message}`,'success',3000)

                } else {
                    customSwal('',`${response.data.message}`,'error',5000)

                }
            })
            .catch(function (error) {
                const message = error.response?.data?.message || error.message || "Unknown error";
                customSwal('', `${message}`, 'error', 5000);
            });
    }
 
});
