var $dripRate = $('#dripRate');
var $startDrip = $('#startDrip');
var $stopDrip = $('#stopDrip');
var $hook = $('#truckHook');
var $div = $('<div id="lastTruck">');
var dripInterval = setInterval(console.log("Let's make some trucks!"), 100000000)

function getDripRate() {
    if ($dripRate.val() < 5){
        return 5000;
    } else if ($dripRate.val() == "") {
        return 5000;
    } else {
        return ($dripRate.val() * 1000)
    }
}

$startDrip.click(function() {
    data = {'dripRate': getDripRate()};
    $('.dripText').remove();
    $('.dripRateText').remove();
    $('<p class="dripRateText">').text("Dripping every " + (data['dripRate'] / 1000) + " seconds.").appendTo($('body'));

    $.get('', data);
    console.log('DRIP!');
    $('<span class="dripText">').text('Drip... ').appendTo($('body'))

    dripInterval = setInterval(function () {
        $.get('', data);
        console.log('Drip!');
        // Uncomment the next line to prevent multiple text instances
        // $('#dripText').remove();
        $('<span class="dripText">').text('Drip... ').appendTo($('body'))
    }, getDripRate());

    return false;
});

$stopDrip.click(function() {
    clearInterval(dripInterval);
    console.log('Drip plugged')
});
