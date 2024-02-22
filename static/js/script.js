
const BASE_BACKEND_URL = "http://localhost:5000/"
let flag = "join-room"

async function sendRequest() {
    try {
        const username = document.getElementById("input-name").value
        const requestType = flag

        let payload = {}
        if (flag == "join-room") {
            const roomCode = document.getElementById("input-room").value
            payload = {
                username,
                requestType,
                roomCode
            }
        } else {
            payload = {
                username,
                requestType
            }
        }    

        const response = await fetch(BASE_BACKEND_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        })

        const data = await response.json()

        return {data: data, status: response.status}
    } catch (error) {
        console.error(error)
    }
}

function getFormHtml() {
    if (flag == "join-room") {
        formUI = `
        <div id="user-inputs-div" class="container p-4 ">
            <input id="input-name" class="text-white font-bold bg-slate-800 flex-grow outline-none px-2 py-2 my-2 w-80 rounded-lg" type="text" placeholder="Enter Name" />
            <br>
            <input id="input-room" class="text-white font-bold bg-slate-800 flex-grow outline-none px-2 py-2 my-2 w-80 rounded-lg" type="text" placeholder="Enter Room Code" />
        </div>`
    } else {
        formUI = `
        <div id="user-inputs-div" class="container p-4 ">
            <input id="input-name" class="text-white font-bold bg-slate-800 flex-grow outline-none px-2 py-2 my-2 w-80 rounded-lg" type="text" placeholder="Enter Name" />
        </div>`
    }
    return formUI
}

function renderFormUI() {
    formDiv = document.getElementById("parent-input-div")
    formDiv.innerHTML = ""
    formDiv.innerHTML = getFormHtml()
}

function renderSubmitBtn() {
    btn = document.getElementById("btn-submit")
    btn.innerHTML = ""
    if (flag == "join-room") {
        btn.innerHTML = "Join"
    } else {
        btn.innerHTML = "Create"
    }
}

function buttonSelect(buttonId) {
    btn = document.getElementById(buttonId)
    let classValue = btn.classList.value
    newClassValue = classValue.replace("bg-slate-500", "bg-slate-900")
    btn.classList.remove('class')
    btn.setAttribute("class", newClassValue)
}

function buttonUnselect(buttonId) {
    btn = document.getElementById(buttonId)
    let classValue = btn.classList.value
    newClassValue = classValue.replace("bg-slate-900", "bg-slate-500")
    btn.classList.remove('class')
    btn.setAttribute("class", newClassValue)
}


document.addEventListener('DOMContentLoaded', function() {
    renderFormUI()
    buttonSelect("join-button")
    document.getElementById("create-button").addEventListener("click", function() {
        flag = "create-room"
        renderFormUI()
        renderSubmitBtn()
        buttonUnselect("join-button")
        buttonSelect("create-button")
    })
    document.getElementById("join-button").addEventListener("click", function() {
        flag = "join-room"
        renderFormUI()
        renderSubmitBtn()
        buttonUnselect("create-button")
        buttonSelect("join-button")
    })
    document.getElementById("btn-submit").addEventListener("click", async function() {
        resp = await sendRequest()
        if (resp.status === 200){
            window.location.href = BASE_BACKEND_URL + "room"
        } else {
            alert("Something Went Wrong.")
        }
    })
})

