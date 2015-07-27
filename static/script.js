'use strict'
var numberofFields = new Number();

function updateDocument(receivedData) {
    console.log("Updating in browser");
    $("#documentText").val(receivedData);
}

function updateFields(receivedFields) {
    console.log("Presently the number of children is : " + $("form").children().length);
    //Set the number of fields, it gets reflected to all windows, then type
    //Setting the number while typing will cause issues
    var temp = numberofFields;
    while(temp <= receivedFields - numberofFields) {
        $("form").append("<div class='field"+temp+"'><input type='text' class='field' id='field"+temp+"'></input></div>");
        temp = parseInt(temp) + 1;
    }
}

$(document).ready(function() {

    var namespace = '/doc';
    var socket = io.connect($SCRIPT_ROOT + namespace);
    var room = "default";
    var pickFields = new Number();
    var receivedFields = "";


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

    socket.on('updateFields', function(message) {
        receivedFields = message.data;
        updateFields(receivedFields);
        listentoElement();
    });

    //It allows for changes in the input including mouse presses
    function listentoElement() {
        $('input.field').on('input propertychange', function() {
            var changedData =$(this).val();
            console.log("THIS is : " + $(this).attr('id').substr(5));
            console.log("The changed data : " + changedData);
            socket.emit('edited', {"data": changedData, "room": room, "field": $(this).attr('id').substr(5) });
        });
    }
    listentoElement();

    $("#pickFields").change(function() {
        console.log("Pick fields fired");
        numberofFields = $("form").children().length;
        pickFields = parseInt($("#pickFields").val());
        console.log("Number of boxes set is : " + pickFields);
        socket.emit('fields change', pickFields);
    })
});
