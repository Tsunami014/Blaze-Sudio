// Require the necessary discord.js classes
const { Client, Events, GatewayIntentBits } = require('discord.js');

const { token } = process.env.DISCORD_TOKEN;

// Create a new client instance
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.MessageContent] });

function processMessage(message, user) {
  if (message.includes(`@${user}`)) {
      return 'very';
  } else {
      return `hard.\n@${user} is working`;
  }
}

let previousMessage = null;

client.once(Events.ClientReady, (readyClient) => {
  console.log(`Ready! Logged in as ${readyClient.user.tag}`);

  const channel = readyClient.channels.cache.get('1181875066280091688'); // Replace with your channel ID

  if (channel) {
    console.log(`We gots a channel :)`);
    channel.messages.fetch({ limit: 10 })
      .then(messages => {
        var msg = '';
        messages.forEach(message => {
          console.log(message);
          if (message.content.contains('@') && msg == '') {
            msg = message.content;
          }
        })
        console.log(`Previous message: ${msg}`);
        // Send a new message in the same channel
        const oldMsg = msg;
        const githubActor = process.env.GITHUB_ACTOR;
        console.log(`GitHub actor: ${githubActor}`);
        const newMsg = processMessage(oldMsg, githubActor)
        channel.send(newMsg)
          .then(() => {
            console.log(`Sent message: ${newMsg}`)
            process.exit(); // Exit the process after sending the message
          })
          .catch(error => {
            console.error(`Error sending message: ${error}`);
            process.exit(); // Exit the process after sending the message
          });
      })
      .catch(error => {
        console.error(`Error fetching messages: ${error}`)
        process.exit(); // Exit the process after sending the message
      });
  }
});

client.login(token);
