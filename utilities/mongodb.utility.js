
const MongoClient = require('mongodb').MongoClient;
const mongoUrl = 'mongodb://localhost:27017/DiscordBot';
// const reminderCheckFreq = 1 * (1000 * 60);

let _db;

module.exports = {

    connectToServer: function (callback) {
        MongoClient.connect(url, {
            useNewUrlParser: true,
            useUnifiedTopology: true
        }, function (err, client) {
            _db = client.db('DiscordBot');
            return callback(err);
        });
    },

    getDb: function () {
        return _db;
    }
};