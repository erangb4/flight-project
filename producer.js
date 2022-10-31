const amqp = require("amqplib");

async function sendMsg(queue, msg) {
  const msgBuffer = Buffer.from(JSON.stringify(msg));
  try {
    const connection = await amqp.connect("amqp://localhost:5672");
    const channel = await connection.createChannel();
    await channel.assertQueue(queue);
    channel.sendToQueue(queue, msgBuffer);
    console.log(`Sending message to queue: ${queue}`);
    await channel.close();
    await connection.close();
  } catch (err) {
    console.error(err);
  }
}

module.exports.sendMsg = sendMsg
