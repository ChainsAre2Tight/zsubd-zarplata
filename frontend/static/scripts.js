let TOKEN = null;

function getLogin() {
    const params = `scrollbars=no,resizable=no,status=no,location=no,toolbar=no,menubar=no,
width=300,height=200,left=100,top=100`;
    const popup = window.open('/login', 'popup', params)
}

function updateToken(newToken) {
    TOKEN = newToken;
    console.log('Got new access token')
}

async function checkToken() {
    if (TOKEN === null) {
        getLogin()
    }

    // if token expiry gets implemented, check time
}

window.addEventListener('load', checkToken)

async function sendRequest(request, callback) {
    await checkToken()

    response = await fetch(...request)

    if (response.status === 401 || response.status === 403) {
        alert('Token expired')
        getLogin()
    } else {
        await callback(response)
    }
}
