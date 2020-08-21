
require('dotenv').config();
const Discord = require('discord.js');
const mongoUtil = require('./utilities/mongodb.utility');
const reminderModel = require('./models/reminder.model');

const DiscordClient = new Discord.Client();



 const seedReminder = {
     name: 'Bob Alice',
     email: 'test@dev.null',
     bonusSetting: true
 };


// Connect to MongoDB and put server instantiation code inside
// because we start the connection first
mongoUtil.connectDB(async (err) => {
    if (err) throw err;
    // Load db & collections
    const db = mongoUtil.getDB();
    const reminders = db.collection('reminders');

    try {
        // Run some sample operations
        // and pass reminders collection into models
        const newReminder = await Reminders.createReminder(reminders, seedReminder);
        const listReminders = await Reminders.getReminders(reminders);
        // const findReminder = await Reminders.findReminderById(reminders, newReminder._id);

        console.log('CREATE USER');
        console.log(newReminder);
        console.log('GET ALL USERS');
        console.log(listReminders);
        // console.log('FIND USER');
        // console.log(findReminder);
    } catch (err) {
        throw err;
    }



    // Server code anywhere above here inside connectDB()
})




DiscordClient.on('ready', () => {DiscordClient.user.setActivity(`Russian Roulette`);});
DiscordClient.on("message", async message => {
    if (message.author.bot) return;
    if (message.content.indexOf(process.env.prefix) !== 0) return;
    const args = message.content.slice(process.env.prefix.length).trim().split(/ +/g);
    const command = args.shift().toLowerCase();

    if(command === 'reminders'){
        // console.log(DB);
        // message.channel.send(reminderCollection);
    }


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
        message.channel.send('now : ' + now);
        message.channel.send('remind: ' + remindTime);
        // message.channel.send('message to remember : ' + msg);

        const reminder = {
            "reminder": true,
            "eventType": "remindme",
            "remindWho": userToRemind,
            "dateToRemind": remindTime,
            "message": msg
        };

        reminder.save()
        .then(result => console.log(result))
        .catch(err => console.log(err));

        message.reply('Reminder saved.. you wont be reminded yet though..');

    }






});
DiscordClient.login(process.env.DISCORD_TOKEN);