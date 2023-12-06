// Require the necessary discord.js classes
const { Client, Intents, Events } = require('discord.js');

const { token } = process.env.DISCORD_TOKEN;

// Create a new client instance
const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES] });

function processMessage(message, user) {
  if (message.mentions.users.has(user.id)) {
      return 'very';
  } else {
      return `hard.\n@${user.tag} is working`;
  }
}

client.once(Events.Ready, async () => {
  console.log(`Ready! Logged in as ${client.user.tag}`);

  const channel = client.channels.cache.get('1181875066280091688'); // Replace with your channel ID

  if (channel) {
    console.log(`We got a channel :)`);

    try {
      const messages = await channel.messages.fetch({ limit: 10 }); // Fetch up to 10 previous messages

      // Iterate through the fetched messages
      messages.forEach(message => {
        if (message.mentions.users.size > 0) {
          // Check if the message contains any user mentions
          const githubActor = process.env.GITHUB_ACTOR;
          console.log(`GitHub actor: ${githubActor}`);
          // Find the first mentioned user whose username matches the github actor
          const mentionedUser = message.mentions.users.find(user => user.username === githubActor);
          if (mentionedUser) {
            // If a matching user is found, process the message
            const newMsg = processMessage(message, mentionedUser);
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
      });

      // If no message with a user mention is found
      console.log('No message with a user mention found.');
      process.exit(); // Exit the process

    } catch (error) {
      console.error(`Error fetching messages: ${error}`);
      process.exit(); // Exit the process after sending the message
    }
  }
});

client.login(token);
