var login_btn = document.getElementById('login-btn')
    var loginform = document.getElementById('loginform')
    var username_validate = document.getElementById('username-validate')
    var password_login = document.getElementById('password_login')
    var username, password = false
    loginform.addEventListener('mousemove', () => {

        if (username_validate.value.length > 0) {
            username = true
        } else {
            username = false
        }

        if (password_login.value.length > 0) {
            password = true
        } else {
            password = false
        }

        if (username === true && password === true) {
            login_btn.removeAttribute("disabled");
        } else {
            login_btn.setAttribute("disabled", "true");
        }
    })