$(document).ready(function(){

    const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    axios.defaults.headers.common['X-CSRFToken'] = csrf_token;

    $('.login-nav-btn').hide();

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

    //----
    //login submit
    $('#login_form').on('submit', function (e) {
        e.preventDefault();
        
        Swal.fire({
            title: 'Validating...',
            allowOutsideClick: false,
            didOpen: () => Swal.showLoading()
        });

        const email = $('#email').val();
        const password = $('#password').val();

        submit_login( email, password);
    });

    function submit_login(email, password) {
        axios.post('/auth/login_submit', { 
                email:email, 
                password:password 
            })
            
            .then(function (response) {
                if (response.data.success) {
                    swal.close();
                    customSwal('',`${response.data.message}`,'success',3000)

                } else {
                    swal.close();
                    customSwal('',`${response.data.message}`,'error',5000)

                }
            })
            .catch(function (error) {
                swal.close();
                const message = error.response?.data?.message || error.message || "Unknown error";
                customSwal('', `${message}`, 'error', 5000);
            });
    }
 
})