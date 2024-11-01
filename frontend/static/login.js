function showErrorMessage(details) {
    const message = document.getElementById('message')
    message.innerText = details
    message.className = 'js-failure'
}

function showSuccessMessage(details) {
    const message = document.getElementById('message')
    message.innerText = details
    message.className = 'js-success'
}

function transferToken(token) {
    window.opener.updateToken(token)
}

async function sendLoginData() {
    console.log('sending data')
    username = document.getElementById('username-input').value
    password = document.getElementById('password-input').value

    if (username == '' || password == '') {
        showErrorMessage('Empty data')
        return
    }

    const data = new FormData()
    data.append('username', username)
    data.append('password', password)

    const response = await fetch(
        '/api/v1/token', {
            method: 'POST',
            body: data
        }
    )
    const json = await response.json()

    if (response.status === 200) {
        showSuccessMessage('Login successfull, window will soon close')
        transferToken(json.access_token)
    } else (
        showErrorMessage(json.detail)
    )
}

function handleClick(event) {
    event.preventDefault()
    sendLoginData()
}

function handlePress(event) {
    if (event.key === 'Enter') {
        event.preventDefault()
        sendLoginData()
    }
}

document.getElementById('send-button').addEventListener('click', (e) => handleClick(e))
window.addEventListener('keypress', (e) => handlePress(e))