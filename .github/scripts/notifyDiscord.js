const { Client, GatewayIntentBits, Events } = require('discord.js');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

let previousMessage = null;

client.once(Events.ClientReady, async (readyClient) => {
  console.log(`Ready! Logged in as ${readyClient.user.tag}`);

  // Get the previous message in a certain channel
  const channel = readyClient.channels.cache.get('1181875066280091688'); // Replace with your channel ID
  if (channel) {
    const messages = await channel.messages.fetch({ limit: 1 });
    previousMessage = messages.last(); // Get the second-to-last message
  }

  const commitAuthor = process.env.GITHUB_ACTOR;

  // Check if the previous message contains '{0} is working'
  if (previousMessage && previousMessage.content.includes(`${commitAuthor} is working`)) {
    if (previousMessage.author.username === commitAuthor) {
      // If the previous message contains the commit author and it's the same person, reply with 'really'
      message.reply('really');
    } else {
      // If the previous message contains the commit author but it's a different person, reply with 'hard.\n{0} is working'
      const newPerson = previousMessage.author.username;
      message.reply(`hard.\n${newPerson} is working`);
    }
  }

  // Update the previous message for the next check
  previousMessage = message;
});

client.login(process.env.DISCORD_TOKEN);
