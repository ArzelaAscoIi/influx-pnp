var mqtt = require('mqtt')
var client = mqtt.connect('mqtt://localhost');

let value = 0

client.on('connect', async function () {
    for (let i = 0; i < 1000; i++) {
        await new Promise(resolve => setTimeout(resolve, 100));
        value += (Math.random() - 0.5)
        client.publish("test", JSON.stringify({ value }))
        console.log(`Successfully published ${value}`)
    }
    client.end()
})
