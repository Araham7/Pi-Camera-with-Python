import React, { useEffect, useRef } from "react";
import io from "socket.io-client";

function App() {
    const imgRef = useRef(null); // <img> tag ke liye ref

    useEffect(() => {
        // WebSocket se connect karo
        const socket = io("http://localhost:3000"); // 

        // Connection status check karo
        socket.on("connect", () => {
            console.log("Connected to WebSocket server");
        });

        // Server se video frame receive karo
        socket.on("video_frame", (data) => {
            console.log("Received video frame");
            // Binary data ko Blob mein convert karo
            const blob = new Blob([data], { type: "image/jpeg" });
            const url = URL.createObjectURL(blob);

            // <img> tag ka src update karo
            if (imgRef.current) {
                imgRef.current.src = url;
            }
        });

        // Disconnect event handle karo
        socket.on("disconnect", () => {
            console.log("Disconnected from WebSocket server");
        });

        // Cleanup: Component unmount hone par WebSocket disconnect karo
        return () => {
            socket.disconnect();
        };
    }, []); // Empty dependency array, sirf component mount aur unmount par chalega

    return (
        <div>
            <h1>Live Video Stream</h1>
            <img ref={imgRef} alt="Live Stream" style={{ width: "640px", height: "480px" }} /> {/* <img> tag ka use karo */}
        </div>
    );
}

export default App;