let host = "127.0.0.1";
let port = 5000;

let websocket = new WebSocket("ws://127.0.0.1:5000", "protocol");

websocket.onopen = (event) => {
  websocket.send("onopen is successful");
};

websocket.onmessage = (event) => {
  addElement(event.data);
  console.log("got message", event.data);
};


/**
 * Creates a div with paragraphs to main_content div with data from the server.
 * @param {{topic: string; message: string}} data
 */
 /*const addElement = (data) => {
    console.log(data)
    console.log(data)
    let o = JSON.parse(data)
    //let test = o.god.data
    // let i = JSON.parse(o)
    let { topic, host, sensor, message, deviceObject, valid} = o.god.data;
    const newDiv = document.createElement("div");
    const newTopic = document.createElement("p")
    const newHost = document.createElement("p")
    const newSensor = document.createElement("p")
    const newMessage = document.createElement("p")
    const devDiv = document.createElement("div");
    console.log(deviceObject)

    newDiv.className="main_content-messages-message"
    newTopic.appendChild(document.createTextNode(`topic: ${topic}`));
    newHost.appendChild(document.createTextNode(`hostname: ${host}`));
    newSensor.appendChild(document.createTextNode(`sensor: ${sensor}`));
    newMessage.appendChild(document.createTextNode(`message: ${message}`));

    newDiv.appendChild(newTopic);
    newDiv.appendChild(newHost);
    newDiv.appendChild(newSensor);
    newDiv.appendChild(newMessage);


    if (!devices.find(item => item === deviceObject)){
        devices.push(deviceObject)
        devDiv.appendChild(document.createTextNode(`device:${deviceObject}; valid:${valid}`));
    }
    if (devices.find(item => item === deviceObject)){
        document.getElementById("main_content-devices").innerHTML=`device:${deviceObject}; valid:${valid}`;
    }

    document.getElementById("main_content").prepend(newDiv);
    document.getElementById("main_content-devices").innerHTML=`device:${deviceObject}; valid:${valid}`;

}*/

let devices = []
let count = 0;
const addElement = async (data) => {
  console.log(data)
  let o = JSON.parse(data)
  //let test = o.god.data
  // let i = JSON.parse(o)
  let { hostname, sensor, message, timestamp, deviceObject, valid} = o.god.data;
  let { valdate } = o.god;
  const newDiv = document.createElement("tr");
  const newTimestamp = document.createElement("td");
  const newHost = document.createElement("td");
  const newSensor = document.createElement("td");
  const newMessage = document.createElement("td");
  console.log(deviceObject);
  

  if (!devices.find(item => item.hostname === deviceObject)){
    let x = {
        hostname: deviceObject,
        valid: valid,
         
        valdate:""
         }
     //if (m.event==="validation ok"){
     //  x.valdate=m.timestamp
     //}
     devices.push(x)
     s = devices[devices.length]
 }
 let k = devices.find(item => item.hostname === deviceObject)
 if (devices.find(item => item.hostname === deviceObject)){
    //s = devices[devices.length]
    console.log("komlmas iffi"+valdate)
    s = devices.indexOf(k)
    devices[s].valdate=valdate
    devices[s].valid=valid
    console.log("valdate: " + devices[s].valdate)
  }
    //  s.valdate=m.timestamp
    //}
 //}

  //   newDiv.className = "main_content-messages-message";
  newTimestamp.appendChild(document.createTextNode(`${timestamp}`));
  newHost.appendChild(document.createTextNode(`${hostname}`));
  newSensor.appendChild(document.createTextNode(`${sensor}`));
  newMessage.appendChild(document.createTextNode(`${message}`));

  
  newDiv.appendChild(newHost);
  newDiv.appendChild(newSensor);
  newDiv.appendChild(newMessage);
  newDiv.appendChild(newTimestamp);

  newDiv.classList.add("active-box", "new-box");

  count++;
  if (count % 2 === 0) newDiv.classList.add("new-new-box");
  document.getElementById("main_content").prepend(newDiv);

  document.getElementById("main_content-devices").innerHTML="";

  for (let i = 0; i < devices.length; i++){
    let elem = document.createElement("div");
    let node = document.createTextNode("hostname: " + devices[i].hostname + " --- valid: " + devices[i].valid + " --- validated on: " + devices[i].valdate);
    elem.appendChild(node);
    document.getElementById(
      "main_content-devices"
    ).appendChild(elem) // = `device:${deviceObject}; valid:${valid}`;
  }
};
