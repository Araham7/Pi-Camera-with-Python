const dgram = require('dgram');
const udpServer = dgram.createSocket('udp4');
const io = require('socket.io')(3000, {
    cors: {
        origin: "*", // React app ka URL
        methods: ["GET", "POST"]
    }
});

// UDP server port 5005 par data receive karega
udpServer.on('message', (message, remote) => {
    console.log(`Received video frame from ${remote.address}:${remote.port}`);
    // WebSocket ke through data bhejo
    io.emit('video_frame', message);
});

udpServer.bind(5005); // UDP server port 5005 par