const { Client } = require('discord.js');

const client = new Client();

client.once('ready', () => {
  console.log('Ready!');
});

client.on('messageCreate', (message) => {
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
});

client.login(process.env.DISCORD_TOKEN);
