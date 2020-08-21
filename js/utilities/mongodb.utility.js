
const MongoClient = require('mongodb').MongoClient;
const mongoUrl = 'mongodb://localhost:27017/DiscordBot';

let _db;

const connectDB = async (callback) => {
    try {
        MongoClient.connect(mongoUrl, {
                    useNewUrlParser: true,
                    useUnifiedTopology: true
                }, (err, client) => {
            _db = client.db;
            return callback(err);
        })
    } catch (e) {
        throw e
    }
};

const getDB = () => _db;

const disconnectDB = () => _db.close();



module.exports = {connectDB, getDB, disconnectDB};







// module.exports = {

//     connectToServer: function (errCallback) {
//         MongoClient.connect(mongoUrl, {
//             useNewUrlParser: true,
//             useUnifiedTopology: true
//         }, function (err, client) {
//             _db = client.db('DiscordBot');
//             return errCallback(err);
//         });
//     },
    

//     getDb: function () {
//         return _db;
//     }
// };