function showErrorMessage(details) {
    const message = document.getElementById('message')
    message.innerText = `failure ${details}`
    message.className = 'js-failure'
}

function showSuccessMessage(details) {
    const message = document.getElementById('message')
    message.innerText = `success ${details}`
    message.className = 'js-success'
}

async function sendLoginData() {
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

    if (response.status === 200) {
        json = await response.json()
        showSuccessMessage(json.access_token)
    } else (
        showErrorMessage(response.status)
    )
}

function handleClick(event) {
    console.log('sending data')
    event.preventDefault()
    sendLoginData()
}

document.getElementById('send-button').addEventListener('click', (e) => handleClick(e))