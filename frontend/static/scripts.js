const TOKEN = null

const getAuthHeader = () => {
    return 'Bearer ' + TOKEN
}

function showUserData(user) {
    console.log(`Вы вошли как ${user.fio}`)
    document.getElementById('pay-method').innerText = user.payment_method
    document.getElementById("pay-address").innerText = user.receipt_address
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

    // TODO call request wrapper
}

async function sendUserData() {
    paymentMethod = document.getElementById('pay-method').innerText
    receiptAddress = document.getElementById("pay-address").innerText

    const request = async () => await fetch('/api/v1/employee/me', {
        method: 'patch',
        headers: {'Authorization': getAuthHeader()},
        body: JSON.stringify({
            payment_method: paymentMethod,
            receipt_address: receiptAddress,
        })
    })

    const callback = async (response) => {
        const success = (response.status === 204)
        const message = success ? 'Данные обновлены' : 'ошибка'

        displayMessage(
            message,
            success,
        )
    }

    // TODO call request wrapper
}

