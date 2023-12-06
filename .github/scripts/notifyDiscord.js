// Require the necessary discord.js classes
const { Client, Events, GatewayIntentBits } = require('discord.js');

const { token } = process.env.DISCORD_TOKEN;

// Create a new client instance
const client = new Client({ intents: [GatewayIntentBits.Guilds] });

// When the client is ready, run this code (only once).
// The distinction between `client: Client<boolean>` and `readyClient: Client<true>` is important for TypeScript developers.
// It makes some properties non-nullable.
client.once(Events.ClientReady, async readyClient => {
	console.log(`Ready! Logged in as ${readyClient.user.tag}`);
    const channel = readyClient.channels.cache.get('1181875066280091688'); // Replace with your channel ID
    if (channel) {
        const messages = await channel.messages.fetch({ limit: 1 });
        previousMessage = messages.last(); // Get the second-to-last message
    }
    console.log(`Previous message: ${previousMessage}`)
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
