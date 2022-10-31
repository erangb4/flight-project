const amqp = require("amqplib");

async function recieveMsg(queue, res) {
  try {
    const connection = await amqp.connect("amqp://localhost:5672");
    const channel = await connection.createChannel();
    await channel.assertQueue(queue);
    channel.consume(queue, (msg) => {
      const input = JSON.parse(msg.content.toString());
      console.log(`Received from ${queue}: ${JSON.stringify(input)}`);
      channel.ack(msg);
      res.status(201).json({
        res: "success",
        url: `/customers/`,
      });
    });
    console.log(`Waiting for messages...`);
  } catch (err) {
    console.error(err);
  }
}

module.exports.recieveMsg = recieveMsg;
