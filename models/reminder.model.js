 const ObjectID = require('mongodb').ObjectID

 // Notice how the reminders collection is passed into the models
 const createReminder = async (remindersCollection, reminder) => {
     try {
         const results = await remindersCollection.insertOne(reminder)
         return results.ops[0]
     } catch (err) {
         throw err
     }
 }

 const getReminders = async (remindersCollection) => {
     try {
         const results = await remindersCollection.find().toArray()
         return results
     } catch (err) {
         throw err
     }
 }

 const findReminderById = async (remindersCollection, id) => {
     try {
         if (!ObjectID.isValid(id)) throw 'Invalid MongoDB ID.'
         const results = await remindersCollection.findOne(ObjectID(id))
         return results
     } catch (err) {
         throw err
     }
 }

 // Export garbage as methods on the Reminders object
 module.exports = { createReminder, getReminders, findReminderById }