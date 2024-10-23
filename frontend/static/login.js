function showErrorMessage(details) {
    alert(`failure ${details}`)
}

function showSuccessMessage(details) {
    alert(`success ${details}`)
}

async function sendLoginData() {
    username = window.getElementById('username-input').value
    password = window.getElementById('password-input').value

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
    event.preventDefault()
}

document.getElementById('send-button').addEventListener('click', (e) => handleClick(e))