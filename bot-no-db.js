// gist.github.com/eslachance/3349734a98d30011bb202f47342601d3#file-index-js

// Run dotenv for sepration between code and config
// ... and so we can deploy it on Heroku
require('dotenv').config();
// require MongnDB to use a database



// Load up the discord.js library
const Discord = require('discord.js');

// This is your client. Some people call it `bot`, some people call it `self`, 
// this is what we're refering to. Your client.
const client = new Discord.Client();

client.on('ready', () => {
    // This event will run if the bot starts, and logs in, successfully.
    console.log(`Test Bot logged in as: ${client.user.tag}`);

    console.log(`Bot has started, with ${client.users.size} users, in ${client.channels.size} channels of ${client.guilds.size} guilds.`);

    // Example of changing the bot's playing game to something useful. `client.user` is what the docs refer to as the "ClientUser".
    // client.user.setActivity(`Serving ${client.guilds.size} servers`);
    client.user.setActivity(`Basic ABC's`);
});



// ----------------------------
// on every message
// ----------------------------
client.on("message", async message => {
  // This event will run on every single message received, from any channel or DM.
  
  // It's good practice to ignore other bots. This also makes your bot ignore itself
  // and not get into a spam loop (we call that "botception").
  if(message.author.bot) return;
  
  // Also good practice to ignore any message that does not start with our prefix, 
  // which is set in the configuration file.
  if(message.content.indexOf(process.env.prefix) !== 0) return;
  
  // Here we separate our "command" name, and our "arguments" for the command. 
  // e.g. if we have the message "~say Is this the real life?" , we'll get the following:
  // command = say
  // args = ["Is", "this", "the", "real", "life?"]
  const args = message.content.slice(process.env.prefix.length).trim().split(/ +/g);
  const command = args.shift().toLowerCase();
  
  if(command === "ping") {
    // Calculates ping between sending a message and editing it, giving a nice round-trip latency.
    // The second ping is an average latency between the bot and the websocket server (one-way, not round-trip)
    const m = await message.channel.send("Ping?");
    m.edit(`Pong! Latency is ${m.createdTimestamp - message.createdTimestamp}ms. API Latency is ${Math.round(client.ping)}ms`);
  }
  
  if(command === "say") {
    // makes the bot say something and delete the message. As an example, it's open to anyone to use. 
    // To get the "message" itself we join the `args` back into a string with spaces: 
    const sayMessage = args.join(" ");
    // And we get the bot to say the thing: 
    message.channel.send(sayMessage);
  }

  if(command==="calc"){
    // smash all input characters after (cmd) into a string with no whitespace
    const inputEquation = args.join("").toString(); // 2 + 2 => 2+2
    
    // digitRegex = /\d+/; // one or more digits per match
    // operatorRegex = /[+-/*]/; // one math operator per match
    const digitArray = [... inputEquation.matchAll(/\d+/g)];
    const operatorArray = [... inputEquation.matchAll(/[+-/*]/g)];
    if(! digitArray[0] || ! operatorArray[0] || ! digitArray[1]){
    message.channel.send('Try using the format: "number" "logic[+-*/]" "number" *(repeatable)');
    return;
    }

    // define our equation a formated string
    let outputEquation = digitArray[0] + operatorArray[0] + digitArray[1];

    let i =1;
    while(operatorArray[i]){
      if( operatorArray[i] && digitArray[(i+1)]){
      outputEquation = outputEquation + operatorArray[i] + digitArray[i+1];
      }
      i++;
    }
    // pre-defining as an empty string just for extra safety
    let result =0;

    // the eval() command is extremely dangerous!!!
    result = eval(outputEquation);
    // the eval() command is extremely dangerous!!!
    message.channel.send('My limited knowledge tells me that equals: ' + result);

    // the eval() command is extremely dangerous!!!
    if(typeof result != Number){return null;}
    // the eval() command is extremely dangerous!!!
  }












  // ----------------------------------------------
  
  if(command === "kick") {
      return;
    // This command must be limited to mods and admins. In this example we just hardcode the role names.
    // Please read on Array.some() to understand this bit: 
    // https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/Array/some?
    if(!message.member.roles.some(r=>["Administrator", "Moderator"].includes(r.name)) )
      return message.reply("Sorry, you don't have permissions to use this!");
    
    // Let's first check if we have a member and if we can kick them!
    // message.mentions.members is a collection of people that have been mentioned, as GuildMembers.
    // We can also support getting the member by ID, which would be args[0]
    let member = message.mentions.members.first() || message.guild.members.get(args[0]);
    if(!member)
      return message.reply("Please mention a valid member of this server");
    if(!member.kickable) 
      return message.reply("I cannot kick this user! Do they have a higher role? Do I have kick permissions?");
    
    // slice(1) removes the first part, which here should be the user mention or ID
    // join(' ') takes all the various parts to make it a single string.
    let reason = args.slice(1).join(' ');
    if(!reason) reason = "No reason provided";
    
    // Now, time for a swift kick in the nuts!
    await member.kick(reason)
      .catch(error => message.reply(`Sorry ${message.author} I couldn't kick because of : ${error}`));
    message.reply(`${member.user.tag} has been kicked by ${message.author.tag} because: ${reason}`);

  }
  
  if(command === "ban") {
      return;
    // Most of this command is identical to kick, except that here we'll only let admins do it.
    // In the real world mods could ban too, but this is just an example, right? ;)
    if(!message.member.roles.some(r=>["Administrator"].includes(r.name)) )
      return message.reply("Sorry, you don't have permissions to use this!");
    
    let member = message.mentions.members.first();
    if(!member)
      return message.reply("Please mention a valid member of this server");
    if(!member.bannable) 
      return message.reply("I cannot ban this user! Do they have a higher role? Do I have ban permissions?");

    let reason = args.slice(1).join(' ');
    if(!reason) reason = "No reason provided";
    
    await member.ban(reason)
      .catch(error => message.reply(`Sorry ${message.author} I couldn't ban because of : ${error}`));
    message.reply(`${member.user.tag} has been banned by ${message.author.tag} because: ${reason}`);
  }
  
  if(command === "purge") {
      return;
    // This command removes all messages from all users in the channel, up to 100.
    
    // get the delete count, as an actual number.
    // [in base 10, as opposed to binary or hexadecimal etc.]
    const deleteCount = parseInt(args[0], 10);
    
    // Ooooh nice, combined conditions. <3
    if(!deleteCount || deleteCount < 2 || deleteCount > 5)
      return message.reply("Please provide a number between 2 and 5 for the number of messages to delete");
    
    // So we get our messages, and delete them. Simple enough, right?
    const fetched = await message.channel.fetchMessages({limit: deleteCount});
    message.channel.bulkDelete(fetched)
      .catch(error => message.reply(`Couldn't delete messages because of: ${error}`));
  }
});

client.login(process.env.DISCORD_TOKEN);