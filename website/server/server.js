const mqtt = require("mqtt");
// import mqtt from 'mqtt'
WebSocket = require("ws");
const path = require("path");
const express = require("express");
const bodyParser = require("body-parser");
const app = express();
const router = express.Router();
const port = 3000;

app.set("view engine", "pug");
app.set("views", "views");
// const index = require("")
app.use(bodyParser.urlencoded({ extended: false }));
// app.use(express.static(path.join(__dirname, "public")));
app.use("/static", express.static("public"));
app.get("/", (req, res) => {
  res.render("index", {
    pageTitle: "Search Hacker News",
  });
});

// app.get("/", (req, res) => {
//   res.send("Hello World!");
// });

// router.get("/", (req, res, next) => {
//   console.log("here");
//   res.render("index");
// });

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});

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
const connectUrl = "mqtt://192.168.0.24:1883";

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
  if (!devices.find((item) => item.device.hostname === m.device.hostname)) {
    try {
      let x = {
        event: m.event,
        message: m.message,
        messagetimestamp: m.messagetimestamp,
        device: {
          itemid: m.device.itemid,
          hostname: m.device.hostname,
          address: m.device.address,
          starttimestamp: m.device.starttimestamp,
          valid: m.device.valid,
          validtimestamp: m.device.validtimestamp,
        },
        sensor: {
          name: m.sensor.name,
          starttimestamp: m.sensor.starttimestamp,
          valid: m.sensor.valid,
          validtimestamp: m.sensor.validtimestamp,
        },
      };
      //if (m.event === "validation ok") {
      //  console.log("eka iffi");
      //  x.valdate = m.timestamp;
      //}

      devices.push(x);
      s = devices[devices.length];
    } catch {
      console.log("Something went wrog with putting data into array");
    }
  }
  let k = devices.find((item) => item.device.hostname === m.device.hostname);
  if (devices.find((item) => item.device.hostname === m.device.hostname)) {
    //s = devices[devices.length]
    s = devices.indexOf(k);
    devices[s].device.valid = m.device.valid;
    if (m.event === "device validation ok") {
      console.log("toka iffi");
      console.log(m.timestamp);
      devices[s].device.valid = m.device.valid;
      console.log(m.device.valid);
      devices[s].device.validtimestamp = m.messagetimestamp;
      console.log(devices[s].device.validtimestamp);
    }
  }

  wsServer.clients.forEach(function (item) {
    // client.send("topic="+topic+"message="+message)
    console.log(topic, "message:", m);
    //console.log(s.toString());

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
    let iitemmm = `{"god": {"data": { "hostname": "${m.device.hostname}", "timestamp": "${m.messagetimestamp}", "sensor": "${m.sensor.name}", "message": "${m.message}", "deviceObject": "${devices[s].device.hostname}", "valid": "${devices[s].device.valid}"}, "valdate": "${devices[s].device.validtimestamp}"}}`;

    console.log(iitemmm);

    item.send(iitemmm);
  });
  // client.end()
});
