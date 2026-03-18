import CONFIG from "./config.js"

let ws
let mediaRecorder

const output = document.getElementById("output")

document.getElementById("start").onclick = async () => {

    ws = new WebSocket(CONFIG.WS_URL)

    ws.onmessage = (event) => {
        output.innerText += event.data + "\n"
    }

    const stream = await navigator.mediaDevices.getUserMedia({
        audio: true
    })

    mediaRecorder = new MediaRecorder(stream, {
        mimeType: "audio/webm"
    })

    mediaRecorder.ondataavailable = async (event) => {
        if (event.data.size > 0 && ws.readyState === 1) {
            const buffer = await event.data.arrayBuffer()
            ws.send(buffer)
        }
    }

    mediaRecorder.start(CONFIG.CHUNK_INTERVAL)
}

document.getElementById("stop").onclick = () => {
    mediaRecorder.stop()
    ws.close()
}