const mqtt = require("mqtt");
// import mqtt from 'mqtt'
WebSocket = require("ws");

const options = {
  // clean: true, // retain session
  // Authentication information
  clientId: "test",
  // keepalive: 60,
  protocolId: "MQTT",
  // protocolVersion: 4,
  // reconnectPeriod: 1000,
  connectTimeout: 1000,
};

// Connect string, and specify the connection method by the protocol
// ws Unencrypted WebSocket connection
// wss Encrypted WebSocket connection
// mqtt Unencrypted TCP connection
// mqtts Encrypted TCP connection
// wxs WeChat applet connection
// alis Alipay applet connection
//const connectUrl = 'mqtt://test.mosquitto.org'
const connectUrl = "mqtt://192.168.11.79:1883";

const client = mqtt.connect(connectUrl);

const PORT = 5000;

const wsServer = new WebSocket.Server({ port: PORT });

wsServer.on("connection", function (socket) {
  console.log("A client just connected");

  socket.on("message", function (msg) {
    console.log("Received message from client: " + msg);

    wsServer.clients.forEach(function (item) {
      // client.send("Someone said: " + msg);
      item.send(`{"topic": "connection", "message": "${msg}"}`);
    });
  });
});

console.log(new Date() + " Server is listening on port " + PORT);

console.log("test");
client.on("connect", function () {
  //client.subscribe('test', function (err) {
  //    if(!err)  {
  //        console.log("not err")
  // client.publish('test', "message")
  //    }
  //})
  client.subscribe("management", function (err) {
    if (!err) {
      console.log("not err");
      //client.publish('management', "message")
    }
  });
});

client.on("reconnect", (error) => {
  console.log("MQTT reconnecting:", error);
});

client.on("error", (error) => {
  console.log("MQTT Connection failed:", error);
});

let devices = [];

client.on("message", function (topic, message) {
  // message is Buffer
  console.log(message.toString(), topic);
  let m = JSON.parse(message);
  let s;
  if (!devices.find((item) => item.hostname === m.hostname)) {
    try{
      let x = {
        itemid: m.itemid,
        hostname: m.hostname,
        ip: m.ip,
        message: m.message,
        event: m.event,
        device: {
          valid: m.device.valid,
          timestamp: m.device.timestamp,
        },
        sensor: {
          name: m.sensor.name,
          timestamp: m.sensor.timestamp,
        },
        timestamp: m.timestamp,
        client: {
          host: "192.168.11.79",
          port: 1883,
          keepalive: 60,
        },
        valdate: "",
      };
      if (m.event === "validation ok") {
        console.log("eka iffi");
        x.valdate = m.timestamp;
      }
  }catch{
    console.log("Something went wrog with putting data into array")
  }
    devices.push(x);
    s = devices[devices.length];
  }
  let k = devices.find((item) => item.hostname === m.hostname);
  if (devices.find((item) => item.hostname === m.hostname)) {
    //s = devices[devices.length]
    s = devices.indexOf(k);
    devices[s].device.valid = m.device.valid;
    if (m.event === "validation ok") {
      console.log("toka iffi");
      console.log(m.timestamp);
      devices[s].device.valid = m.device.valid;
      console.log(m.device.valid);
      devices[s].valdate = m.timestamp;
      console.log(devices[s].valdate);
    }
  }

  wsServer.clients.forEach(function (item) {
    // client.send("topic="+topic+"message="+message)
    console.log(topic, "message:", m);
    console.log(s.toString());

    // let iitemmm =`"god":
    //               {
    //                 "data":
    //                     {
    //                       "topic": "${topic}",
    //                       "host": "${m.hostname}",
    //                       "sensor": "${m.sensor.name}",
    //                       "message": "${m.message}",
    //                       "deviceObject": "${devices[s].hostname}",
    //                       "valid": "${devices[s].device.valid}"
    //                       },
    //                 "devs":
    //                   "${JSON.stringify(...devices)}"

    //                 }`
    let iitemmm = `{"god": {"data": { "hostname": "${m.hostname}", "timestamp": "${m.timestamp}", "sensor": "${m.sensor.name}", "message": "${m.message}", "deviceObject": "${devices[s].hostname}", "valid": "${devices[s].device.valid}"}, "valdate": "${devices[s].valdate}"}}`;

    console.log(iitemmm);

    item.send(iitemmm);
  });
  // client.end()
});
