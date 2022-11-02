let host = "127.0.0.1"
let port = 5000

let websocket = new WebSocket("ws://127.0.0.1:5000", "protocol" )

websocket.onopen = (event) => {
    websocket.send("onopen is successful")
}

websocket.onmessage = (event) => {
    addElement(event.data);
    console.log("got message", event.data);
}


/**
 * Creates a div with paragraphs to main_content div with data from the server.
 * @param {{topic: string; message: string}} data 
 */
const addElement = (data) => {
    let { topic, message} = JSON.parse(data);
    const newDiv = document.createElement("div");
    const newTopic = document.createElement("p")
    const newMessage = document.createElement("p")

    newTopic.appendChild(document.createTextNode(`topic: ${topic}`));
    newMessage.appendChild(document.createTextNode(`message: ${message}`));

    newDiv.appendChild(newTopic);
    newDiv.appendChild(newMessage);

    document.getElementById("main_content").prepend(newDiv);
}