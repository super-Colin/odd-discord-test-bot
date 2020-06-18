
var fs = require('fs');
var INTERVAL = 1000;

var cycle_stop = false;
var daemon = false;
var timer;


process.argv.forEach(function (arg) {
    if (arg === '-d') daemon = true;
});

process.on('SIGTERM', function () {
    console.log('Got SIGTERM signal.');
    stop();
});


(function cycle() {
    timer = setTimeout(function () {
        runTask();
        if (!cycle_stop) cycle();
    }, INTERVAL);
})();


function runTask() {
    var data = new Date().getTime() + ": OK\n";
    fs.appendFileSync('./tmp/daemon-test.txt', data);
}


function stop() {
    cycle_stop = true;
    clearTimeout(timer);
}



if (daemon) require('daemon')();



