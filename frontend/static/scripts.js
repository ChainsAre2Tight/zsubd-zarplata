let TOKEN = null;

function getLogin() {
    const params = `scrollbars=no,resizable=no,status=no,location=no,toolbar=no,menubar=no,
width=600,height=300,left=100,top=100`;
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
}

window.addEventListener('load', checkToken)
