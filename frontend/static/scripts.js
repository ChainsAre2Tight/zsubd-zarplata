let TOKEN = null;
let popup = null;
let update = (token) => {}

function updateToken(token) {
    update(token)
}

function updateProgressBar(max, remaining) {
    bar = document.getElementById('filled-progress-bar')
    const width = (1 - remaining / max) * 100 + '%'
    bar.style.width = width
}

async function getLogin() {
    const params = `scrollbars=no,resizable=no,status=no,location=no,toolbar=no,menubar=no,
width=300,height=200,left=100,top=100`;
    popup = window.open('/login', 'popup', params)
    popup.focus()

    var promiseResolve

    update = (newToken) => {
        TOKEN = newToken;
        console.log('Got new access token')
        setTimeout(() => popup.close(), 500) // close login window
        promiseResolve()
        update = (token) => {}
    }

    let promise = new Promise((resolve, reject) => {
        promiseResolve = resolve
    })
    
    await promise
    console.log('got login')
}

async function checkToken() {
    if (TOKEN === null) {
        await getLogin()
    }

    // if token expiry gets implemented, check time
}

// window.addEventListener('load', checkToken)

async function sendRequest(request, callback) {
    await checkToken()

    const response = await request()

    if (response.status === 401 || response.status === 403) {
        alert('Token expired')
        getLogin()
    } else {
        await callback(response)
    }
}

const getAuthHeader = () => {
    return 'Bearer ' + TOKEN
}

function showUserData(user) {
    console.log(`Вы вошли как ${user.fio}`)
    document.getElementById('pay-method').value = user.payment_method
    document.getElementById("pay-address").value = user.receipt_address
}

function displayMessage(message, success) {
    const display = document.getElementById('message')
    display.innerText = message
    display.className = success ? 'js-success' : 'js-failure'
}

async function getUserData() {
    const request = async () => await fetch('/api/v1/employee/me', {
        method: 'GET', 
        headers: {'Authorization': getAuthHeader()}
    }
    )
    const callback = async (response) => {
        const json = await response.json()
        showUserData(json)
    }

    await sendRequest(request, callback)
}

async function sendUserData() {
    const paymentMethod = document.getElementById('pay-method').value
    const receiptAddress = document.getElementById("pay-address").value
    const obj = {payment_method: paymentMethod, receipt_address: receiptAddress}

    const request = async () => await fetch('/api/v1/employee/me', {
        method: 'PATCH',
        headers: {
            'Authorization': getAuthHeader(),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(obj)
    })

    const callback = async (response) => {
        const success = (response.status === 204)
        const message = success ? 'Данные обновлены' : 'ошибка'

        displayMessage(
            message,
            success,
        )
    }

    await sendRequest(request, callback)
}

function handleEmployeePatchClick (event) {
    console.log('Sending employee data...')
    sendUserData()
}

async function sendOrderData() {
    const amount = document.getElementById('order-volume').value

    const request = async () => fetch('/api/v1/order/', {
        method: 'POST',
        headers: {
            'Authorization': getAuthHeader(),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({amount: amount})
    })

    const callback = async (response) => {
        const json = await response.json()

        const success = (response.status === 201)
        const message = success ? `Заказ внесен, его id: ${json.uuid}` : JSON.stringify(json.detail)

        displayMessage(
            message,
            success,
        )
    }

    await sendRequest(request, callback)
}

async function sendVacationData() {
    const start = document.getElementById('start-day').value
    const end = document.getElementById('finish-day').value

    const request = async () => fetch('/api/v1/vacation/', {
        method: 'POST',
        headers: {
            'Authorization': getAuthHeader(),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            begin_date: start,
            end_date: end,
        })
    })

    const callback = async (response) => {
        const json = await response.json()

        const success = (response.status === 201)
        const message = success ? `Отпуск зарезервирован: ${json.vacation_id}` : JSON.stringify(json.detail)

        displayMessage(
            message,
            success,
        )

        updateProgressBar(
            json.max_duration,
            json.remaining_duration,
        )
    }

    await sendRequest(request, callback)
}

function displayVacations(vacations) {
    console.log(vacations); return; // TODO remove

    const display = document.getElementById('vacation-table')
    for (const vacation of vacations) {
        const row = document.createElement('tr')
        const begin = document.createElement('td')
        const end = document.createElement('td')

        begin.appendChild(document.createTextNode(vacation.begin_date))
        end.appendChild(document.createTextNode(vacation.end_date))

        row.appendChild(begin)
        row.appendChild(end)
        display.appendChild(row)
    }
} 

async function getVacationData() {
    const request = async () => await fetch('/api/v1/vacation/', {
        method: 'GET',
        headers: {'Authorization': getAuthHeader()},
    })

    const callback = async (response) => {
        json = await response.json()

        displayVacations(json)
    }

    await sendRequest(request, callback)
}

async function loadUserData() {
    await checkToken();
    getUserData();
    getVacationData();
}

window.addEventListener('load', async () => await loadUserData())
document.querySelector("#self-parameters button").addEventListener(
    'click', (e) => handleEmployeePatchClick()
)
document.querySelector("#order button").addEventListener(
    'click', async (e) => {
        console.log('Sending order data...'),
        await sendOrderData()
    }
)
document.querySelector("#vacation button").addEventListener(
    'click', async (e) => {
        console.log('Sending vacation data...'),
        await sendVacationData()
    }
)