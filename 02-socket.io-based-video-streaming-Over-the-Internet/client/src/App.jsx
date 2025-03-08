import React, { useEffect, useRef, useState } from "react";
import io from "socket.io-client";

function App() {
    const imgRef = useRef(null); // Image element ke liye ref
    const [socket, setSocket] = useState(null); // Socket connection ko store karne ke liye state

    useEffect(() => {
        // Socket connection establish karo
        const newSocket = io("https://pi-video-streaming-server.onrender.com", { // http://localhost:3000
            reconnection: true,
            reconnectionAttempts: 5,
            reconnectionDelay: 1000,
        });

        setSocket(newSocket); // Socket ko state mein store karo

        // Debugging ke liye connection events
        newSocket.on("connect", () => {
            console.log("Connected to Express.js server");
        });

        newSocket.on("connect_error", (err) => {
            console.error("Connection error:", err);
        });

        newSocket.on("disconnect", () => {
            console.log("Disconnected from Express.js server");
        });

        // Server se video frame receive karo
        newSocket.on("video_frame", (data) => {
            console.log("Received video frame data:", data);
            console.log("Data type:", typeof data);
            console.log("Data length:", data.length);

            // Agar data binary hai
            if (data instanceof ArrayBuffer || data instanceof Blob) {
                const blob = new Blob([data], { type: "image/jpeg" });
                const url = URL.createObjectURL(blob);
                if (imgRef.current) {
                    imgRef.current.src = url; // img tag ka src update karo
                }
            }
            // Agar data base64 string hai
            else if (typeof data === "string") {
                const base64Data = data.split(",")[1]; // Agar data URL format mein hai
                const url = `data:image/jpeg;base64,${base64Data}`; // Base64 URL banayein
                if (imgRef.current) {
                    imgRef.current.src = url; // img tag ka src update karo
                }
            }
        });

        // Cleanup function: Component unmount hone par socket disconnect karo
        return () => {
            newSocket.disconnect();
        };
    }, []); // Empty dependency array, sirf component mount aur unmount par chalega

    return (
        <div>
            <h1>Live Video Stream</h1>
            <img ref={imgRef} alt="Live Stream" /> {/* img tag ka use karo */}
            {/* <video ref={videoRef} autoPlay muted controls /> */}
        </div>
    );
}

export default App;