// Require the necessary discord.js classes
const { Client, Events, GatewayIntentBits } = require('discord.js');

const { token } = process.env.DISCORD_TOKEN;

// Create a new client instance
const client = new Client({ intents: [GatewayIntentBits.Guilds] });

let previousMessage = null;

client.once(Events.ClientReady, (readyClient) => {
  console.log(`Ready! Logged in as ${readyClient.user.tag}`);

  const channel = readyClient.channels.cache.get('1181875066280091688'); // Replace with your channel ID

  if (channel) {
    console.log(`We gots a channel :)`);
    channel.messages.fetch({ limit: 1 })
      .then(messages => {
        previousMessage = messages.last(); // Get the second-to-last message
        console.log(`Previous message: ${previousMessage.content}`);
        // Send a new message in the same channel
        const newMessageContent = previousMessage.content;
        channel.send(initialMessageContent)
          .then(() => {
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

/*client.on('messageCreate', (message) => {
  const commitAuthor = process.env.GITHUB_ACTOR;

  if (message.content.includes(`${commitAuthor} is working`)) {
    if (message.author.username === commitAuthor) {
      // If the message contains the commit author and it's the same person, reply with 'really'
      message.reply('really');
    } else {
      // If the message contains the commit author but it's a different person, reply with 'hard.\n{0} is working'
      const newPerson = message.author.username;
      message.reply(`hard.\n${newPerson} is working`);
    }
  }
});*/

client.login(token);
