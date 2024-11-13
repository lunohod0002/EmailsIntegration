var socket = new WebSocket('ws://localhost:8000/ws/emails/');
socket.onmessage=function(event){
    var messageData =e.data;
    console.log(messageData);
    document.querySelector('#app').innerText=messageData.value;
}