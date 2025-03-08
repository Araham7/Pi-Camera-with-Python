import { useEffect, useRef, useState } from "react";
import { io } from "socket.io-client";
import "./VideoStream.css";

const VideoStream = () => {
  const [imageSrc, setImageSrc] = useState("");
  const socketRef = useRef(null);

  useEffect(() => {
    // Connect to the Socket.IO server
    socketRef.current = io("http://localhost:8765");

    // Listen for the /video-send event
    socketRef.current.on("/video-send", (data) => {
      // Convert the binary data to a Blob
      const blob = new Blob([data], { type: "image/jpeg" });
      const url = URL.createObjectURL(blob);

      // Update the image source
      setImageSrc(url);

      // Send an acknowledge event
      socketRef.current.emit("/video-receive", { status: "OK" });
    });

    // Cleanup on component unmount
    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, []);

  return (
    <div>
      <h1>Video Stream</h1>
      <img
        src={imageSrc}
        alt="Video Stream"
        width="640"
        height="480"
        style={{ border: "1px solid black" }}
      />
    </div>
  );
};

export default VideoStream;