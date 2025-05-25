$(document).ready(function () {

    const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    axios.defaults.headers.common['X-CSRFToken'] = csrf_token;
    // Reusable SweetAlert2 dialog
    function customSwal(title, message, icon = 'info', timer = 3000) {
        return Swal.fire({
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
    // resend reset link submit
    $('#resend_reset_link_form').on('submit', function (e) {
        e.preventDefault();

        Swal.fire({
            title: 'Processing...',
            allowOutsideClick: false,
            didOpen: () => Swal.showLoading()
        });

        const email = $('#email').val();
        resend_reset_link(email);
    });
    //resend the reset link function
    function resend_reset_link(email) {
        axios.post('/auth/send_reset_link', {email: email })
            .then(function (response) {
                if (response.data.success) {
                    Swal.close()
                    customSwal('',`${response.data.message}`,'success',5000)
                } else {
                    swal.close()
                    customSwal('',`${response.data.message}`,'error',5000)

                }
            })
            .catch(function (error) {
                swal.close()
                const message = error.response?.data?.message || error.message || "Unknown error";
                customSwal('', `${message}`, 'error', 5000);
            });
    }

    //-----
    // change password submit
    $('#change_pass_form').on('submit', function (e) {
        e.preventDefault();

        Swal.fire({
            title: 'Processing...',
            allowOutsideClick: false,
            didOpen: () => Swal.showLoading()
        });
        const link_token = $('#change_pass_form').data('link_token');
        const password = $('#new_password').val();
        const confirm_password = $('#confirm_new_password').val();
        change_password(password, confirm_password,link_token)
    });
    //change the password function
    function change_password(password,confirm_password,link_token) {
        axios.post(`/auth/change_pass_page/${link_token}`, {password: password, confirm_password: confirm_password})
            .then(function (response) {
                if (response.data.success) {
                    Swal.close()
                    customSwal('',`${response.data.message}`,'success',5000)
                } else {
                    swal.close()
                    customSwal('',`${response.data.message}`,'error',5000)

                }
            })
            .catch(function (error) {
                swal.close()
                const message = error.response?.data?.message || error.message || "Unknown error";
                customSwal('', `${message}`, 'error', 5000);
            });
    }


 
});
