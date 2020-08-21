require('dotenv').config();

const Discord = require('discord.js');

const mongoose = require("mongoose");
const mongoUrl = 'mongodb://localhost:27017/DiscordBot';
require('./models/reminder.model');
const Reminder = mongoose.model('Reminder');
const reminderCheckFreq = 1 * (1000 * 60);
mongoose.connect(mongoUrl);


// Set up a task that will check for reminders every 1 minute
setInterval(function() {
    console.log('checking db for reminders');
    const now = Math.floor(new Date().getTime() / 1000);
    // look through reminders

    // if reminder is now 

    // Display reminder message

    // Delete reminder from DB

}, reminderCheckFreq);





const client = new Discord.Client();
client.on('ready', () => {client.user.setActivity(`Russian Roulette`);});


client.on("message", async message => {
    if (message.author.bot) return;
    if (message.content.indexOf(process.env.prefix) !== 0) return;
    const args = message.content.slice(process.env.prefix.length).trim().split(/ +/g);
    const command = args.shift().toLowerCase();


    if(command === "remindme"){
        
        if(args[0] === "help"){
            message.channel.send('This commands set a reminder for you. Pass an amount of minutes until you should be reminded and a message for yourself. Example:');
            message.channel.send(process.env.prefix  + 'remindme 15 Check the oven');
            return;
        }

        const userToRemind = message.author;
        const msg = args.slice(1).join(" ");
        const now = Math.floor(new Date().getTime() / 1000);
        const minutesFromNowInMillisec = Math.floor(args[0] * 60000); //1 min => 60,000 milliseconds
        const remindTime = now + minutesFromNowInMillisec;

        // message.channel.send('user to remind : ' + userToRemind);
        message.channel.send('now: ' + now);
        message.channel.send('time to remind: ' + remindTime);
        // message.channel.send('message to remember : ' + msg);

        const reminder = new Reminder({
            _id: mongoose.Types.ObjectId(),
            reminder: true,
            eventType: "remindme",
            remindWho: userToRemind,
            dateToRemind: remindTime,
            message: msg
        });

        reminder.save()
        .then(result => console.log(result))
        .catch(err => console.log(err));

        message.reply('Reminder saved.. you wont be reminded yet though..');

    }






});
client.login(process.env.DISCORD_TOKEN);