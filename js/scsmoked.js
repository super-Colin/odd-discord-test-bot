
// how many cigarettes do I smoke a day:
const cigsSmokedDaily = 13;

// how much does a pack cost?
const costOfAPack = 7.53;

// how much do I spend on cigarettes a day?
const moneySpentDaily = cigsSmokedDaily/20 * costOfAPack;

// how much of my life am I killing by smoking? (In minutes)
const lifeLostPerCig = 7;
const lifeLostPerDay = lifeLostPerCig * cigsSmokedDaily;



let smokingCostsString = `
Smoking ${+(cigsSmokedDaily).toFixed(2)} cigs per day at $${+(costOfAPack).toFixed(2)} a pack is costing you: \n
$${+(moneySpentDaily).toFixed(2)} every single day, $${+(moneySpentDaily * 7).toFixed(2)} per week and ~$${+(moneySpentDaily * 29).toFixed(2)} per month. \n
And if one cig takes 7 minutes off your life, it's also costing you: \n
${+(lifeLostPerDay).toFixed(2)} minutes of your life everyday, ${+((lifeLostPerDay * 7) / 60).toFixed(2)} hours every week and ${+(((lifeLostPerDay * 29) / 60) / 24).toFixed(2)} days of your life every month
`;

console.log(smokingCostsString);

