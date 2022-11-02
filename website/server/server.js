
const mqtt = require('mqtt')
// import mqtt from 'mqtt'
WebSocket = require('ws')


const options = {
    // clean: true, // retain session
    // Authentication information
    clientId: 'test',
    // keepalive: 60,
    protocolId: 'MQTT',
    // protocolVersion: 4,
    // reconnectPeriod: 1000,
    connectTimeout: 1000,
}

// Connect string, and specify the connection method by the protocol
// ws Unencrypted WebSocket connection
// wss Encrypted WebSocket connection
// mqtt Unencrypted TCP connection
// mqtts Encrypted TCP connection
// wxs WeChat applet connection
// alis Alipay applet connection
const connectUrl = 'mqtt://test.mosquitto.org'
// const connectUrl = "ws://194.157.71.11:8883/mqtt"

const client = mqtt.connect(connectUrl, options)



const PORT = 5000;

const wsServer = new WebSocket.Server({port: PORT});

wsServer.on("connection", function(socket) {
    console.log("A client just connected")

    socket.on('message', function(msg) {
        console.log("Received message from client: " + msg);

        
        wsServer.clients.forEach(function (client) {
            // client.send("Someone said: " + msg);
            client.send(`{"topic": "connection", "message": "${msg}"}`)
        });
    });
});

console.log((new Date()) + " Server is listening on port " + PORT);

console.log("test")
client.on('connect', function () {
client.subscribe('test', function (err) {
    if(!err)  {
        console.log("not err")
        // client.publish('test', "message")
    }
})
})

client.on('reconnect', (error) => {
console.log('MQTT reconnecting:', error)
})

client.on('error', (error) => {
console.log('MQTT Connection failed:', error)
})


client.on('message', function (topic, message) {
// message is Buffer
console.log(message.toString(), topic)
wsServer.clients.forEach(function (client) {
    // client.send("topic="+topic+"message="+message)
    client.send(`{"topic": "${topic}", "message": "${message}"}`)
})
// client.end()
})



