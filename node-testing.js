// mongod --port 27017 --dbpath C:\mongodb\data\db


const mongo = require('mongodb').MongoClient;
const url = 'mongodb://localhost:27017';

mongo.connect(url, {
    useNewUrlParser: true,
    useUnifiedTopology: true
}, (err, client) => {
    if (err) {
        console.error(err)
        return
    }
    const db = client.db('newTest');
    const collection = db.collection('amIHere');

    collection.insertOne({name: 'Roger'}, (err, result) => {});

    console.log(collection);


});







console.log('no errors??');