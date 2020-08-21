
const mongoose = require("mongoose");

const ReminderSchema = mongoose.Schema({
    _id: mongoose.Schema.Types.ObjectId,
    reminder: Boolean,
    eventType: String,
    remindWho: String,
    dateToRemind: String,
    message: String
})


module.exports = mongoose.model("Reminder", ReminderSchema);
