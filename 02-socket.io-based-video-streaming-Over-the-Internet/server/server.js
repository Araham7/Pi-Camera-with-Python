const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const cors = require("cors");

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: "*", // React.js client URL(http://localhost:5173)
        methods: ["GET", "POST"],
        transports: ["websocket", "polling"], // Allow both WebSocket and polling
    },
});

app.use(cors());

// Handle client connections
io.on("connection", (socket) => {
    console.log("Client connected:", socket.id);

    // Handle video frames from Python
    socket.on("video_frame", (data) => {
        // Broadcast the frame to all clients
        io.emit("video_frame", data);
        // console.log(data);
    });

    // Handle disconnect
    socket.on("disconnect", () => {
        console.log("Client disconnected:", socket.id);
    });
});

// Start the server
const PORT = 3000;
server.listen(PORT, () => {
    console.log(`Express server running at http://localhost:${PORT}`);
});