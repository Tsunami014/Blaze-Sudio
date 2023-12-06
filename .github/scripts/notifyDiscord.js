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

client.once(Events.ClientReady, async (readyClient) => {
  console.log(`Ready! Logged in as ${readyClient.user.tag}`);

  const channel = readyClient.channels.cache.get('1181875066280091688'); // Replace with your channel ID

  if (channel) {
    console.log(`We got a channel :)`);

    try {
      const messages = await channel.messages.fetch({ limit: 20 }); // Fetch up to 10 previous messages

      // Iterate through the fetched messages
      for (const [, message] of messages) {
        if (message.content.includes('@')) {
          // Check if the message contains an '@' mention
          const githubActor = process.env.GITHUB_ACTOR;
          console.log(`GitHub actor: ${githubActor}`);
          const newMsg = processMessage(message.content, githubActor);
          console.log(`Message: ${newMsg}`);
          channel.send(newMsg)
            .then(() => {
              console.log(`Sent message: ${newMsg}`);
              process.exit(); // Exit the process after sending the message
            })
            .catch(error => {
              console.error(`Error sending message: ${error}`);
              process.exit(); // Exit the process after sending the message
            });
        }
      }

      // If no message with an '@' mention is found
      console.log('No message with an "@" mention found.');
      process.exit(); // Exit the process

    } catch (error) {
      console.error(`Error fetching messages: ${error}`);
      process.exit(); // Exit the process after sending the message
    }
  }
});

client.login(token);
