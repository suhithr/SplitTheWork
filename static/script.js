function updateDocument(receivedData) {
    console.log("Updating in browser");
    $("#documentText").val(receivedData);
}

$(document).ready(function() {

    var namespace = '/doc';
    var socket = io.connect($SCRIPT_ROOT + namespace);
    var room = "default";


    socket.on('connect', function() {
        console.log("Connected");
        socket.emit('create or join', room);
    });

    socket.on('update', function(message) {
        var receivedData = message.data;
        updateDocument(receivedData);
    });

    socket.on('initial data', function(message) {
        var receivedData = message.data;
        updateDocument(receivedData);
    });
    socket.on('in_room', function(room) {
        console.log("Now in the room : " + room);
    });


    //It allows for changes in the input including mouse presses
    $("#documentText").on('input propertychange', function() {
        var changedData = $('#documentText').val();
        socket.emit('edited', {"data": changedData, "room": room});
    });

});
