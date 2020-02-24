// mongod --port 27017 --dbpath C:\mongodb\data\db


require('dotenv').config();
// Load up the discord.js library
const Discord = require('discord.js');

// require MongnDB to use a database
const mongodb = require('mongodb').MongoClient;
// define the url to the DB server
const mongoUrl = 'mongodb://localhost:27017';
// define the Database to use
const db = client.db('DiscordBot');
const collection = db.collection('reminders');


mongodb.connect(mongoUrl, {
    useNewUrlParser: true,
    useUnifiedTopology: true
}, (err, client) => {
    if (err) {console.error(err);return}


    collection.insertOne(
        {
            "reminder": true,
            "dateToRemind": "10/10/2020",
            "eventType": "birthday",
            "remindWho": "all",
            "message": "Happy Birthday!"
    }, (err, result) => {});

    console.log(collection);


});







console.log('no errors??');