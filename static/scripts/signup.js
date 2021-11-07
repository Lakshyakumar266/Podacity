const username_validate = document.getElementById('username-validate')
const textArea_words = document.getElementById('textArea-words')
const password_signup = document.getElementById('password_signup')
const signupform = document.getElementById('signupform')
const signupsubmit = document.getElementById('signupsubmit')

formValidate = () => {
    var textarea, username, password

    textArea_words.addEventListener('blur', () => {
        const describe_warning = document.getElementById('describe-warning')
        var words = textArea_words.value.split(' ')
        if (words.length < 25) {
            textArea_words.classList.remove('is-valid')
            textArea_words.classList.add('is-invalid')

            describe_warning.classList.add('d-block')
            describe_warning.classList.remove('d-none')

            textarea = false
        } else {
            textArea_words.classList.remove('is-invalid')
            textArea_words.classList.add('is-valid')

            describe_warning.classList.add('d-none')
            describe_warning.classList.remove('d-block')

            textarea = true
        }
    })

    username_validate.addEventListener('blur', () => {
        var Uname = username_validate.value.split(' ').length
        if (Uname === 1 && username_validate.value != '') {
            username_validate.classList.remove('is-invalid')
            username_validate.classList.add('is-valid')
            username = true
        } else {
            username_validate.classList.remove('is-valid')
            username_validate.classList.add('is-invalid')
            username = false
        }
    })

    password_signup.addEventListener('blur', () => {
        const password_warning = document.getElementById('password-warning')
        password_warning.classList.add('text-muted')

        if (password_signup.value.length >= 8) {
            password_signup.classList.remove('is-invalid')
            password_signup.classList.add('is-valid')

            password_warning.classList.add('d-none')
            password_warning.classList.remove('d-block')

            password = true
        } else {
            password_signup.classList.remove('is-valid')
            password_signup.classList.add('is-invalid')

            password_warning.classList.add('d-block')
            password_warning.classList.add('text-danger')
            password_warning.classList.remove('text-muted')
            password_warning.classList.remove('d-none')

            password = false
        }
    })

    signupform.addEventListener('mousemove', () => {
        if (username == true && textarea == true && password == true) {
            signupsubmit.removeAttribute("disabled");
        } else {
            signupsubmit.setAttribute("disabled", "true");
        }
    })


}
formValidate()