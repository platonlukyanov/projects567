function switch_password_visibility(btn, input) {
            var status = "text";
            btn.addEventListener('click', ()=> {

                input.setAttribute("type", status);
                if (status === "password") {
                    btn.classList.remove("bi-eye");
                    btn.classList.add("bi-eye-slash");
                    console.log('text');
                    status = "text";
                }
                else if (status === "text") {
                    btn.classList.add("bi-eye");
                    btn.classList.remove("bi-eye-slash");
                    console.log('password');
                    status = "password";
                }
            })
        }

        var btn1 = document.getElementById('eye');
        var btn2 = document.getElementById('eye2');
        var inp1 = document.getElementById('password-inp');
        var inp2 = document.getElementById('password2-inp');
        switch_password_visibility(btn1, inp1);
        switch_password_visibility(btn2, inp2);