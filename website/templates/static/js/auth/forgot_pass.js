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

    // verification submit
    $('#forgot_form').on('submit', function (e) {
        e.preventDefault();

        Swal.fire({
            title: 'Processing...',
            allowOutsideClick: false,
            didOpen: () => Swal.showLoading()
        });

        const email = $('#email').val();

        submit_reset(email);
    });
    function submit_reset(email) {
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
 
});
